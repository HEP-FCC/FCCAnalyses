import os
import sys
import logging
import argparse
import importlib.util
from typing import Dict, Any

# Use the standard FCCAnalyses logging hierarchy
LOGGER = logging.getLogger('FCCAnalyses.combine')

class DatacardWriter:
    """Writes the structured OOP configuration out to Combine's standard text format."""
    
    def __init__(self, datacard_obj):
        self.datacard = datacard_obj
        self.channels = getattr(datacard_obj, 'channels', {})
        self.systematics = getattr(datacard_obj, 'systematics', {})
        self.shapes = getattr(datacard_obj, 'shapes', {})
        self.autoMCStats = getattr(datacard_obj, 'autoMCStats', False)
        
        self.metadata = self._get_metadata()
        self.col_w = self._calculate_col_width()

    def _get_metadata(self) -> Dict[str, int]:
        imax = len(self.channels)
        jmax = 0
        if self.channels:
            first_channel = list(self.channels.values())[0]
            processes = first_channel.get('processes', {})
            jmax = sum(1 for p in processes.values() if p.get('type') == 'background')
            
        kmax = len(self.systematics)
        return {'imax': imax, 'jmax': jmax, 'kmax': kmax}

    def _calculate_col_width(self) -> int:
        max_len = 10 
        for ch_name, ch_data in self.channels.items():
            max_len = max(max_len, len(ch_name))
            for proc_name in ch_data.get('processes', {}).keys():
                max_len = max(max_len, len(proc_name))
        for syst_name in self.systematics.keys():
            max_len = max(max_len, len(syst_name))
        return max_len + 4 

    def generate(self, output_path: str):
        with open(output_path, 'w') as f:
            self._write_header(f)
            self._write_shapes(f)
            self._write_observation(f)
            self._write_rates(f)
            self._write_systematics(f)
            self._write_automcstats(f)
        LOGGER.info('Successfully generated production datacard: %s', output_path)

    def _write_header(self, f):
        f.write(f"imax {self.metadata['imax']}  number of channels\n")
        f.write(f"jmax {self.metadata['jmax']}  number of backgrounds\n")
        f.write(f"kmax {self.metadata['kmax']}  number of nuisance parameters\n")
        f.write("-" * 50 + "\n")

    def _write_shapes(self, f):
        if self.shapes:
            for process, channels in self.shapes.items():
                for channel, mapping in channels.items():
                    f.write(f"shapes {process} {channel} {mapping}\n")
            f.write("-" * 50 + "\n")

    def _write_observation(self, f):
        bin_names = "".join([f"{name:<{self.col_w}}" for name in self.channels.keys()])
        obs_values = "".join([f"{str(ch.get('observation', 0)):<{self.col_w}}" for ch in self.channels.values()])
        
        f.write(f"{'bin':<{self.col_w}}{bin_names}\n")
        f.write(f"{'observation':<{self.col_w}}{obs_values}\n")
        f.write("-" * 50 + "\n")

    def _write_rates(self, f):
        bin_line = [f"{'bin':<{self.col_w}}"]
        process_name_line = [f"{'process':<{self.col_w}}"]
        process_id_line = [f"{'process':<{self.col_w}}"]
        rate_line = [f"{'rate':<{self.col_w}}"]

        for bin_name, channel_data in self.channels.items():
            processes = channel_data.get('processes', {})
            sorted_procs = sorted(
                processes.items(), 
                key=lambda item: 0 if item[1].get('type') == 'signal' else 1
            )
            bkg_counter = 1
            for proc_name, proc_data in sorted_procs:
                bin_line.append(f"{bin_name:<{self.col_w}}")
                process_name_line.append(f"{proc_name:<{self.col_w}}")
                if proc_data.get('type') == 'signal':
                    process_id_line.append(f"{'0':<{self.col_w}}")
                else:
                    process_id_line.append(f"{str(bkg_counter):<{self.col_w}}")
                    bkg_counter += 1
                rate_line.append(f"{str(proc_data.get('rate', 0.0)):<{self.col_w}}")

        f.write("".join(bin_line) + "\n")
        f.write("".join(process_name_line) + "\n")
        f.write("".join(process_id_line) + "\n")
        f.write("".join(rate_line) + "\n")
        f.write("-" * 50 + "\n")

    def _write_systematics(self, f):
        for syst_name, syst_info in self.datacard.systematics.items():
            syst_type = syst_info.get("type", "lnN")
            apply_to = syst_info.get("apply_to", {})

            # Start each row with the systematic name and its type
            row_cells = [syst_name, syst_type]

            # Loop over channels
            for ch_name, ch_info in self.datacard.channels.items():
                sorted_procs = sorted(
                    ch_info.get('processes', {}).items(),
                    key=lambda item: 0 if item[1].get('type') == 'signal' else 1
                )

                for proc_name, _ in sorted_procs:
                    # Check if this systematic applies to the current process
                    if proc_name in apply_to:
                        val = apply_to[proc_name]

                        # If it's a channel-dependent dictionary, extract the specific channel value
                        if isinstance(val, dict):
                            val = val.get(ch_name, "-")

                        row_cells.append(str(val))
                    else:
                        row_cells.append("-")

            f.write("\t".join(row_cells) + "\n")

    def _write_automcstats(self, f):
        if self.autoMCStats:
            f.write("-" * 50 + "\n")
            f.write("* autoMCStats 0 1 1\n")


def sanitize_and_validate_config(user_datacard) -> None:
    """Validates properties and verifies shape histogram existence in ROOT files before backend execution."""
    import ROOT

    channels = getattr(user_datacard, 'channels', {})
    if not channels:
        LOGGER.warning("No channels defined in the datacard object.")

    # 1. Standard structural and rate checks
    for ch_name, ch_data in channels.items():
        obs = ch_data.get('observation', 0)
        if not (isinstance(obs, (int, float)) and (obs >= 0 or obs == -1)):
            raise ValueError(f"Sanitization Error: Invalid observation '{obs}' in channel '{ch_name}'. Must be >= 0 or -1.")
        
        processes = ch_data.get('processes', {})
        for proc_name, proc_data in processes.items():
            p_type = proc_data.get('type')
            if p_type not in ['signal', 'background']:
                raise ValueError(f"Validation Error: Invalid type '{p_type}' for process '{proc_name}' in channel '{ch_name}'. Must be 'signal' or 'background'.")
            
            rate = proc_data.get('rate', 0.0)
            if not (isinstance(rate, (int, float)) and (rate >= 0 or rate == -1)):
                raise ValueError(f"Validation Error: Invalid rate '{rate}' for process '{proc_name}'. Must be >= 0 or -1.")

    valid_syst_types = ['lnN', 'shape', 'gmM', 'gmN']
    systematics = getattr(user_datacard, 'systematics', {})
    shapes_config = getattr(user_datacard, 'shapes', {})

    # 2. Advanced Shape Systematics Check
    for syst_name, syst_data in systematics.items():
        s_type = syst_data.get('type')
        if s_type not in valid_syst_types:
            raise ValueError(f"Validation Error: Invalid systematic type '{s_type}' for '{syst_name}'. Allowed: {valid_syst_types}")

        # If it's a shape systematic, verify the physical histograms exist
        if s_type == 'shape':
            apply_to = syst_data.get('apply_to', {})
            
            for ch_name, ch_info in channels.items():
                # Determine what the shape mapping rule is for this channel
                # Handles wildcard '*' or specific process rules
                mapping_rule = shapes_config.get('*', {}).get(ch_name) or shapes_config.get(proc_name, {}).get(ch_name)
                
                if not mapping_rule:
                    continue
                
                # Extract the ROOT file path (assumes space-separated path and inner structure mapping)
                root_file_path = mapping_rule.split()[0]
                
                if not os.path.isfile(root_file_path):
                    LOGGER.warning("Shape file '%s' not created yet or using relative build path. Skipping deep object check.", root_file_path)
                    continue

                # Open the file via PyROOT to peek inside
                r_file = ROOT.TFile.Open(root_file_path, "READ")
                if not r_file or r_file.IsZombie():
                    raise ValueError(f"Validation Error: Failed to open shape ROOT file: {root_file_path}")

                for proc_name in ch_info.get('processes', {}).keys():
                    if proc_name in apply_to and str(apply_to[proc_name]) != '-':
                        
                        # Resolve the inner path template (e.g., $CHANNEL/$PROCESS -> mumu_bjets_channel/ZH_signal)
                        base_path = mapping_rule.split()[1].replace('$CHANNEL', ch_name).replace('$PROCESS', proc_name)
                        
                        # Combine expects clones with "Up" and "Down" appended to the nominal path/name
                        for variation in ['Up', 'Down']:
                            target_hist_path = f"{base_path}_{syst_name}{variation}"
                            hist = r_file.Get(target_hist_path)
                            
                            if not hist or not hist.InheritsFrom("TH1"):
                                r_file.Close()
                                raise ValueError(
                                    f"Validation Error: Missing required shape histogram!\n"
                                    f"  File: {root_file_path}\n"
                                    f"  Expected Path: {target_hist_path}\n"
                                    f"  Reason: Systematic '{syst_name}' is declared as 'shape' for '{proc_name}' in '{ch_name}'."
                                )
                r_file.Close()

def generate_datacard(anapath: str, output_path: str) -> None:
    """Sub-command engine execution block."""
    
    LOGGER.info('Loading Combine fit script from: %s', anapath)

    if not os.path.isfile(anapath):
        LOGGER.error('Fit script file not found! Aborting...')
        sys.exit(3)

    try:
        spec = importlib.util.spec_from_file_location('user_fit', anapath)
        user_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(user_module)
    except SyntaxError as err:
        LOGGER.error('Syntax error encountered in the fit script:\n%s', err)
        sys.exit(3)
        
    if not hasattr(user_module, "Datacard"):
        LOGGER.error('Fit script must define a class named "Datacard"! Aborting...')
        sys.exit(3)
        
    user_datacard = user_module.Datacard()
    
    try:
        sanitize_and_validate_config(user_datacard)
    except ValueError as err:
        LOGGER.error('%s\nAborting...', err)
        sys.exit(3)
        
    LOGGER.info('Successfully sanitized and verified user input configuration.')
    
    # Run the generator matrix logic
    writer = DatacardWriter(user_datacard)
    writer.generate(output_path)
