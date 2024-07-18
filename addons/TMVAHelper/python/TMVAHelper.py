import ROOT

ROOT.gInterpreter.ProcessLine('#include "TMVAHelper/TMVAHelper.h"')
ROOT.gSystem.Load("libTMVAHelper")


class TMVAHelperXGB():
    def __init__(self, model_input, model_name, variables=[]):
        # try to get the variables from the model file (saved as a TList)
        if len(variables) == 0:
            fIn = ROOT.TFile(model_input)
            variables_ = fIn.Get("variables")
            self.variables = [str(var.GetString()) for var in variables_]
            fIn.Close()
        else:
            self.variables = variables
        self.model_input = model_input
        self.model_name = model_name
        self.nthreads = ROOT.GetThreadPoolSize()

        self.tmva_helper = ROOT.tmva_helper_xgb(self.model_input,
                                                self.model_name,
                                                self.nthreads)
        self.var_col = f"tmva_vars_{self.model_name}"

    def run_inference(self, df, col_name="mva_score"):

        # check if columns exist in the dataframe
        cols = df.GetColumnNames()
        for var in self.variables:
            if var not in cols:
                raise Exception(f"Variable {var} not defined in dataframe.")

        vars_str = ', (float)'.join(self.variables)
        df = df.Define(self.var_col,
                       f"ROOT::VecOps::RVec<float>{{{vars_str}}}")
        df = df.Define(col_name, self.tmva_helper, [self.var_col])
        return df
