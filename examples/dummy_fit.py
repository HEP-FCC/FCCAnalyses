class Datacard:
    def __init__(self):
        # Global configuration toggles
        self.autoMCStats = True
        
        # Shape file templates
        self.shapes = {
            "*": {
                "electron_channel": "fcc_analysis_shapes.root $CHANNEL/$PROCESS",
                "muon_channel": "fcc_analysis_shapes.root $CHANNEL/$PROCESS"
            }
        }
        
        # Channel-by-channel definitions
        self.channels = {
            "electron_channel": {
                "observation": -1,
                "processes": {
                    "ZH_signal": {"type": "signal", "rate": -1},
                    "Z_background": {"type": "background", "rate": -1}
                }
            },
            "muon_channel": {
                "observation": -1,
                "processes": {
                    "ZH_signal": {"type": "signal", "rate": -1},
                    "Z_background": {"type": "background", "rate": -1}
                }
            }
        }
        
        # Systematics dictionary
        self.systematics = {
            "lumi": {
                "type": "lnN",
                "apply_to": {"ZH_signal": 1.05, "Z_background": 1.05}
            },
            "efficiency": {
                "type": "lnN",
                "apply_to": {"ZH_signal": 1.02}
            }
        }
