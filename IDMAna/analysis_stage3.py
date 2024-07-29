processList = {
    'p8_ee_ZZ_ecm240':{},
    'p8_ee_WW_ecm240':{},
    'wzp6_ee_eeH_ecm240':{},
    'wzp6_ee_mumuH_ecm240':{},
    'wzp6_ee_nunuH_ecm240':{},
    'wzp6_ee_tautauH_ecm240':{},
    'wzp6_ee_qqH_ecm240':{},
    'wzp6_ee_ee_Mee_30_150_ecm240':{},
    'wzp6_ee_mumu_ecm240':{},
    'wzp6_ee_tautau_ecm240':{},
    'e240_bp1_h2h2ll':{},'e240_bp1_h2h2llvv':{},
    'e240_bp2_h2h2ll':{},'e240_bp2_h2h2llvv':{},
    'e240_bp3_h2h2ll':{},'e240_bp3_h2h2llvv':{},
    'e240_bp4_h2h2ll':{},'e240_bp4_h2h2llvv':{},
    'e240_bp5_h2h2ll':{},'e240_bp5_h2h2llvv':{},
    'e240_bp6_h2h2ll':{},'e240_bp6_h2h2llvv':{},
    'e240_bp7_h2h2ll':{},'e240_bp7_h2h2llvv':{},
    'e240_bp8_h2h2ll':{},'e240_bp8_h2h2llvv':{},
    'e240_bp9_h2h2ll':{},'e240_bp9_h2h2llvv':{},
    'e240_bp10_h2h2ll':{},'e240_bp10_h2h2llvv':{},
    'e240_bp11_h2h2ll':{},'e240_bp11_h2h2llvv':{},
    'e240_bp12_h2h2ll':{},'e240_bp12_h2h2llvv':{},
    'e240_bp13_h2h2ll':{},'e240_bp13_h2h2llvv':{},
    'e240_bp14_h2h2ll':{},'e240_bp14_h2h2llvv':{},
    'e240_bp18_h2h2ll':{},'e240_bp18_h2h2llvv':{},
    'e240_bp19_h2h2ll':{},'e240_bp19_h2h2llvv':{},
    'e240_bp20_h2h2ll':{},'e240_bp20_h2h2llvv':{},
    #'p8_ee_ZH_ecm240_out':{'output':'MySample_p8_ee_ZH_ecm240'} #Run over the full statistics from stage1 input file <inputDir>/p8_ee_ZH_ecm240_out.root. Change the output name to MySample_p8_ee_ZH_ecm240
}

#Mandatory: input directory when not running over centrally produced edm4hep events. 
#It can still be edm4hep files produced standalone or files from a first analysis step (this is the case in this example it runs over the files produced from analysis.py)
inputDir  = "iDM/stage2"

#Optional: output directory, default is local dir
outputDir   = "iDM/stage3/"

#Optional: ncpus, default is 4
nCPUS       = 4

#Optional running on HTCondor, default is False
runBatch    = False

##USER DEFINED CODE
#import ROOT
#ROOT.gInterpreter.Declare("""
#bdt("BDT", "dataset/weights/TMVAClassification_BDT.weights.xml");
#std::vector<float> ComputeBDT(TMVA::Experimental::RBDT<> bdt,
#float Zcand_e,
#float Zcand_m,
#float Zcand_pt,
#float Zcand_costheta,
#float Zcand_povere,
#float Zcand_recoil_m,
#float cosThetaStar,
#float cosThetaR){
#return bdt.Compute({Zcand_e,Zcand_m,Zcand_pt,Zcand_costheta,Zcand_povere,Zcand_recoil_m,cosThetaStar,cosThetaR});
#}
#""")
##END USER DEFINED CODE
import ROOT
import os
def add_bdt(df):#, xmlpath, bpnum):
    
    vec_varn = []

    for bpnum in range(1,21):
        xmlpath="dataset_{}/weights/TMVAClassification_BDT.weights.xml".format(bpnum)

        if not os.path.exists(xmlpath):
            continue

        ROOT.gInterpreter.ProcessLine('''TMVA::Experimental::RReader model{}("{}");'''.format(bpnum,xmlpath))


        nvars = ROOT.model1.GetVariableNames().size()
        print("BP = ", bpnum)
        print("Nvars = ", nvars)
        ROOT.gInterpreter.ProcessLine('''auto computeModel{} = TMVA::Experimental::Compute<{}, float>(model{});'''.format(bpnum,nvars,bpnum))

    
        l_expr = ROOT.model1.GetVariableNames()

        #print("VarNames = ", l_expr)
        
        l_varn = ROOT.std.vector['std::string']()
        for i_expr, expr in enumerate(l_expr):
            varname = 'v_{}_{}'.format(i_expr,bpnum)
            #print(varname)
            l_varn.push_back(varname)
            
            #if (bpnum==1):
            df=df.Define(varname, '(float)({})'.format(expr) )
            #else:
            #    df=df.Redefine(varname, '(float)({})'.format(expr) )
        vec_varn.append(l_varn)

    df2 = (df
           .Define("bdt_output_bp1", ROOT.computeModel1, vec_varn[0])
           .Define("bdt_output_bp2", ROOT.computeModel2, vec_varn[1])
           .Define("bdt_output_bp3", ROOT.computeModel3, vec_varn[2])
           .Define("bdt_output_bp4", ROOT.computeModel4, vec_varn[3])
           .Define("bdt_output_bp5", ROOT.computeModel5, vec_varn[4])
           .Define("bdt_output_bp6", ROOT.computeModel6, vec_varn[5])
           .Define("bdt_output_bp7", ROOT.computeModel7, vec_varn[6])
           .Define("bdt_output_bp8", ROOT.computeModel8, vec_varn[7])
           .Define("bdt_output_bp9", ROOT.computeModel9, vec_varn[8])
           .Define("bdt_output_bp10", ROOT.computeModel10, vec_varn[9])
           .Define("bdt_output_bp11", ROOT.computeModel11, vec_varn[10])
           .Define("bdt_output_bp12", ROOT.computeModel12, vec_varn[11])
           .Define("bdt_output_bp13", ROOT.computeModel13, vec_varn[12])
           .Define("bdt_output_bp14", ROOT.computeModel14, vec_varn[13])
           .Define("bdt_output_bp18", ROOT.computeModel18, vec_varn[14])
           .Define("bdt_output_bp19", ROOT.computeModel19, vec_varn[15])
           .Define("bdt_output_bp20", ROOT.computeModel20, vec_varn[16])

           )

    return df2

#Mandatory: RDFanalysis class where the use defines the operations on the TTree
class RDFanalysis():


    #__________________________________________________________
    #Mandatory: analysers funtion to define the analysers to process, please make sure you return the last dataframe, in this example it is df2
    def analysers(df):
#        prevdf=df
#        for BP in range(1,21):
#            df2 = add_bdt(prevdf,"dataset_{}/weights/TMVAClassification_BDT.weights.xml".format(BP),BP)
#            prevdf=df2

#        return prevdf
        df2 = add_bdt(df)
        return df2


    #__________________________________________________________
    #Mandatory: output function, please make sure you return the branchlist as a python list.
    def output():
        branchList = [
            "Zcand_m",
            "Zcand_pt",
            "Zcand_pz",
            "Zcand_p",
            "Zcand_povere",
            "Zcand_e",
            "Zcand_costheta",
            "Zcand_recoil_m",
            "photon1_pt","photon1_eta","photon1_e",
            "lep1_pt","lep1_eta","lep1_e","lep1_charge",
            "lep2_pt","lep2_eta","lep2_e","lep2_charge",
            "lep_chargeprod",
            "jet1_pt","jet1_eta","jet1_e",
            "jet2_pt","jet2_eta","jet2_e",
            "cosDphiLep","cosThetaStar","cosThetaR",
            "n_jets","n_seljets",
            "MET_e","MET_pt","MET_eta","MET_phi",
            "n_photons","n_muons","n_electrons",
            "bdt_output_bp1","bdt_output_bp2","bdt_output_bp3",
            "bdt_output_bp4","bdt_output_bp5","bdt_output_bp6",
            "bdt_output_bp7","bdt_output_bp8","bdt_output_bp9",
            "bdt_output_bp10","bdt_output_bp11","bdt_output_bp12",
            "bdt_output_bp13","bdt_output_bp14","bdt_output_bp18",
            "bdt_output_bp19","bdt_output_bp20"
        ]
        return branchList




