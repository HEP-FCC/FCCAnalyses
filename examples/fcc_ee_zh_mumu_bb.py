class Datacard:
    def __init__(self):
        # 1. Global framework configurations
        self.autoMCStats = False

        # 2. Path templates for the input shape histograms
        self.shapes = {
            "*": {
                "mumu_bjets_channel": "fcc_ee_zh_shapes.root $CHANNEL/$PROCESS $CHANNEL/$PROCESS_$SYSTEMATIC",
                "mumu_inter_channel": "fcc_ee_zh_shapes.root $CHANNEL/$PROCESS $CHANNEL/$PROCESS_$SYSTEMATIC"
            }
        }

        # 3. Channel definitions based on event selection categories
        # Category 1: High purity b-tagged category
        # Category 2: Intermediate/loose b-tagged category (to constrain backgrounds)
        self.channels = {
            "mumu_bjets_channel": {
                "observation": -1, # -1 instructs Combine to use asymptotic or toy datasets
                "processes": {
                    "ZH_signal":   {"type": "signal",     "rate": -1},
                    "ZZ_bkg":      {"type": "background", "rate": -1},
                    "Zjets_bkg":   {"type": "background", "rate": -1}
                }
            },
            "mumu_inter_channel": {
                "observation": -1,
                "processes": {
                    "ZH_signal":   {"type": "signal",     "rate": -1},
                    "ZZ_bkg":      {"type": "background", "rate": -1},
                    "Zjets_bkg":   {"type": "background", "rate": -1}
                }
            }
        }

        # 4. Systematics Matrix
        # Models how uncertainties affect each process in each distinct channel
        self.systematics = {
            # Integrated luminosity precision at FCC-ee (highly precise, ~0.1% to 0.5%)
            "lumi_FCC": {
                "type": "lnN",
                "apply_to": {
                    "ZH_signal": 1.005,
                    "ZZ_bkg":    1.005,
                    "Zjets_bkg": 1.005
                }
            },
            # Muon tracking and Identification efficiency uncertainty
            "muon_eff": {
                "type": "lnN",
                "apply_to": {
                    "ZH_signal": 1.01,
                    "ZZ_bkg":    1.01,
                    "Zjets_bkg": 1.01
                }
            },
            # B-tagging efficiency uncertainty (highly correlated with signal)
            "btag_eff": {
                "type": "lnN",
                "apply_to": {
                    "ZH_signal": {"mumu_bjets_channel": 1.03, "mumu_inter_channel": 0.98},
                    "ZZ_bkg":    {"mumu_bjets_channel": 1.03, "mumu_inter_channel": 0.98}
                }
            },
            # Mistag rate uncertainty for light/charm jets leaking into the b-jet channel
            "mistag_light": {
                "type": "lnN",
                "apply_to": {
                    "Zjets_bkg": {"mumu_bjets_channel": 1.10, "mumu_inter_channel": 1.04}
                }
            },
            # Theoretical cross-section uncertainty for electroweak backgrounds
            "theory_ZZ_xsec": {
                "type": "lnN",
                "apply_to": {
                    "ZZ_bkg": 1.04
                }
            },
            # Recoil mass resolution shape systematic
            "recoil_res": {
                "type": "shape",
                "apply_to": {
                    "ZH_signal": 1.0,
                    "ZZ_bkg":    1.0
                }
            }
        }
