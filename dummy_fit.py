class Datacard:
    def __init__(self):
        # 1. Define channels
        self.channels = ["electron_channel", "muon_channel"]
        
        # 2. Define processes (rates are -1 until Phase 2 is done)
        self.processes = {
            "ZH_signal": {"type": "signal", "rate": -1},
            "Z_background": {"type": "background", "rate": -1}
        }
        
        # 3. Define systematics
        self.systematics = {
            "lumi": {"type": "lnN", "value": 1.05},
            "jet_energy_scale": {"type": "shape", "value": 1.0}
        }
