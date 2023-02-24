
import json
import ROOT


class JetFlavourHelper():

    def __init__(self, jsonCfg, onnxCfg, config):
    
        self.jsonCfg = jsonCfg
        self.onnxCfg = onnxCfg
        self.config = config
        

        ## extract input variables/score name and ordering from json file
        self.variables, self.scores = [], []
        f = open(self.jsonCfg)
        data = json.load(f)
        for varname in data["pf_features"]["var_names"]:
            self.variables.append(varname)

        for varname in data["pf_vectors"]["var_names"]:
            self.variables.append(varname)

        for scorename in data["output_names"]:
            self.scores.append(scorename)

        f.close()
        # convert to tuple
        self.variables = tuple(self.variables)

        # then funcs
        for varname in self.variables:
            if varname not in self.config.definition:
                print("ERROR: {} variables was not defined.".format(varname))
                sys.exit()
    

        
        self.get_weight_str = "JetFlavourUtils::get_weights(rdfslot_, "
        for var in self.variables:
            self.get_weight_str += "{},".format(var)
        self.get_weight_str = "{})".format(self.get_weight_str[:-1])

        
        from ROOT import JetFlavourUtils
        weaver = JetFlavourUtils.setup_weaver(
            self.onnxCfg,  # name of the trained model exported
            self.jsonCfg,  # .json file produced by weaver during training
            self.variables, 
            ROOT.GetThreadPoolSize() if ROOT.GetThreadPoolSize() > 0 else 1
        )
        
        
    def inference(self, df):
    
        ### COMPUTE THE VARIABLES FOR INFERENCE OF THE TRAINING MODEL
        # first aliases
        for var, al in self.config.alias.items():
            df = df.Alias(var, al)
        # then funcs
        for var, call in self.config.definition.items():
            df = df.Define(var, call)

        ##### RUN INFERENCE and cast scores (fixed by the previous section)
        df = df.Define("MVAVec", self.get_weight_str)

        for i, scorename in enumerate(self.scores):
            df = df.Define(scorename, "JetFlavourUtils::get_weight(MVAVec, {})".format(i))
            
        return df
        
        
    def outputBranches(self):
    
        out = ["recojet_isG", "recojet_isQ","recojet_isS", "recojet_isC", "recojet_isB"]
        out += (self.config.variables_jet.keys())
        return out