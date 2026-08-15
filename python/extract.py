import os
import glob
import logging
import argparse

LOGGER = logging.getLogger('FCCAnalyses.extract')

def find_crossing(x_vals, y_vals, target=1.0, left=True, best_fit=0.0):
    """Finds the linearly interpolated x-value where y crosses the target threshold."""
    pairs = sorted(zip(x_vals, y_vals))
    if left:
        filtered = [p for p in pairs if p[0] <= best_fit]
        filtered.reverse()
    else:
        filtered = [p for p in pairs if p[0] >= best_fit]

    for i in range(len(filtered) - 1):
        x1, y1 = filtered[i]
        x2, y2 = filtered[i+1]
        
        if (y1 <= target <= y2) or (y2 <= target <= y1):
            if y2 == y1: return x1
            return x1 + (target - y1) * (x2 - x1) / (y2 - y1)
    return None

def extract_fit_results(target_path):
    """Extracts uncertainties from a specific Combine ROOT file or directory."""
    try:
        import ROOT
        ROOT.gROOT.SetBatch(True)
        ROOT.PyConfig.IgnoreCommandLineOptions = True
    except ImportError:
        LOGGER.error("PyROOT is not available. Cannot extract uncertainties.")
        return

    if os.path.isdir(target_path):
        root_files = glob.glob(os.path.join(target_path, "higgsCombine*.root"))
        if not root_files:
            LOGGER.warning("No higgsCombine output ROOT file found in directory: %s", target_path)
            return
        target_file = max(root_files, key=os.path.getmtime)
    else:
        target_file = target_path

    if not os.path.exists(target_file):
        LOGGER.error("Target file does not exist: %s", target_file)
        return

    LOGGER.info("Extracting fit results from: %s", target_file)
    f_in = ROOT.TFile.Open(target_file, "READ")
    if not f_in or f_in.IsZombie():
        LOGGER.error("Could not open output ROOT file: %s", target_file)
        return

    tree = f_in.Get("limit")
    if not tree:
        LOGGER.error("Could not find 'limit' TTree inside %s", target_file)
        f_in.Close()
        return

    tree.GetEntry(0)
    
    if hasattr(tree, "deltaNLL"):
        x_vals, y_vals = [], []
        
        ignore_branches = {"limit", "limitErr", "syst", "iTheta", "iEta", "quantileExpected", "deltaNLL", "t_cpu", "t_real"}
        branch_names = [b.GetName() for b in tree.GetListOfBranches()]
        candidates = [b for b in branch_names if b not in ignore_branches]
        
        if "r" in candidates:
            poi_name = "r"
        elif candidates:
            poi_name = next((c for c in candidates if c != "mh"), candidates[0])
        else:
            poi_name = "r"

        for i in range(tree.GetEntries()):
            tree.GetEntry(i)
            # Relaxed the deltaNLL filter to 1000 so steep curves aren't deleted
            if tree.quantileExpected < -1.5 or tree.deltaNLL > 1000: continue
            
            val = getattr(tree, poi_name, None)
            if val is not None:
                x_vals.append(val)
                y_vals.append(2.0 * tree.deltaNLL)

        if len(x_vals) > 1:
            sorted_pairs = sorted(zip(x_vals, y_vals))
            x_vals, y_vals = zip(*sorted_pairs)
            min_idx = y_vals.index(min(y_vals))
            best_fit = x_vals[min_idx]

            unc_left = find_crossing(x_vals, y_vals, target=1.0, left=True, best_fit=best_fit)
            unc_right = find_crossing(x_vals, y_vals, target=1.0, left=False, best_fit=best_fit)
            
            err_down = (unc_left - best_fit) if unc_left is not None else float('nan')
            err_up = (unc_right - best_fit) if unc_right is not None else float('nan')

            print("\n" + "="*50)
            print(f"  FIT RESULTS: MultiDimFit ({poi_name})")
            print("="*50)
            print(f"  Best-fit {poi_name} : {best_fit:.6f}")
            print(f"  -1 Sigma (68% CL): {err_down:+.6f} (Value: {unc_left:.6f})" if unc_left else "  -1 Sigma (68% CL): N/A")
            print(f"  +1 Sigma (68% CL): {err_up:+.6f} (Value: {unc_right:.6f})" if unc_right else "  +1 Sigma (68% CL): N/A")
            print("="*50 + "\n")
        else:
            LOGGER.warning("Tree contains only 1 point. Run Combine with a scan (e.g., --algo grid) to extract crossing uncertainties.")

    else:
        limits = {}
        for i in range(tree.GetEntries()):
            tree.GetEntry(i)
            limits[round(tree.quantileExpected, 3)] = tree.limit

        print("\n" + "="*50)
        print("  FIT RESULTS: AsymptoticLimits (95% CL)")
        print("="*50)
        if -1.0 in limits: print(f"  Observed Limit   : r < {limits[-1.0]:.6f}")
        if 0.5 in limits:  print(f"  Expected Median  : r < {limits[0.5]:.6f}")
        if 0.16 in limits and 0.84 in limits: print(f"  Expected 68% Band: {limits[0.16]:.6f} - {limits[0.84]:.6f}")
        if 0.025 in limits and 0.975 in limits: print(f"  Expected 95% Band: {limits[0.025]:.6f} - {limits[0.975]:.6f}")
        print("="*50 + "\n")

    f_in.Close()

def run_extract(parser: argparse.ArgumentParser) -> None:
    """Sub-command entry point for extracting uncertainties."""
    args, _ = parser.parse_known_args()
    extract_fit_results(args.input_path)
