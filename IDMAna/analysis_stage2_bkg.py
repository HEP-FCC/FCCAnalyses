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
    #'p8_ee_ZH_ecm240_out':{'output':'MySample_p8_ee_ZH_ecm240'} #Run over the full statistics from stage1 input file <inputDir>/p8_ee_ZH_ecm240_out.root. Change the output name to MySample_p8_ee_ZH_ecm240
}

#Mandatory: input directory when not running over centrally produced edm4hep events. 
#It can still be edm4hep files produced standalone or files from a first analysis step (this is the case in this example it runs over the files produced from analysis.py)
inputDir  = "/eos/user/a/amagnan/FCC/iDMprod/Analysis/stage1"

#Optional: output directory, default is local dir
outputDir   = "iDM/stage2/"

#Optional: ncpus, default is 4
nCPUS       = 4

#Optional running on HTCondor, default is False
runBatch    = False

##USER DEFINED CODE
#import ROOT
#ROOT.gInterpreter.Declare("""
#bool myFilter(ROOT::VecOps::RVec<float> mass) {
#    for (size_t i = 0; i < mass.size(); ++i) {
#        if (mass.at(i)>80. && mass.at(i)<100.)
#            return true;
#    }
#    return false;
#}
#""")
##END USER DEFINED CODE

#Mandatory: RDFanalysis class where the use defines the operations on the TTree
class RDFanalysis():

    #__________________________________________________________
    #Mandatory: analysers funtion to define the analysers to process, please make sure you return the last dataframe, in this example it is df2
    def analysers(df):
        df2 = (df
               .Filter("zed_mumu_m.size()==1 || zed_ee_m.size()==1")
               .Define("Zcand_m","if (zed_mumu_m.size()==1) return zed_mumu_m.at(0); else if (zed_ee_m.size()==1) return zed_ee_m.at(0); else return float(-1);")
               .Define("Zcand_pt","if (zed_mumu_pt.size()==1) return zed_mumu_pt.at(0); else if (zed_ee_pt.size()==1) return zed_ee_pt.at(0); else return float(-1);")
               .Define("Zcand_pz","if (zed_mumu_pz.size()==1) return zed_mumu_pz.at(0); else if (zed_ee_pz.size()==1) return zed_ee_pz.at(0); else return float(-1000);")
               .Define("Zcand_p","if (zed_mumu_p.size()==1) return zed_mumu_p.at(0); else if (zed_ee_p.size()==1) return zed_ee_p.at(0); else return float(-1);")
               .Define("Zcand_e","return sqrt(pow(Zcand_m,2)+pow(Zcand_p,2));")
               .Define("Zcand_povere","return Zcand_p/Zcand_e;")
               .Define("Zcand_costheta","if (zed_mumu_theta.size()==1) return TMath::Cos(zed_mumu_theta.at(0)); else if (zed_ee_theta.size()==1) return TMath::Cos(zed_ee_theta.at(0)); else return double(-1.1);")
               .Define("Zcand_recoil_m","if (zed_mumu_recoil_m.size()==1) return zed_mumu_recoil_m.at(0); else if (zed_ee_recoil_m.size()==1) return zed_ee_recoil_m.at(0); else return float(-1);")
               .Define("photon1_pt","if (selected_photons_pt.size()>=1) return selected_photons_pt.at(0); else return float(-1);")
               .Define("photon1_eta","if (selected_photons_eta.size()>=1) return selected_photons_eta.at(0); else return float(-5);")
               .Define("photon1_e","if (selected_photons_e.size()>=1) return selected_photons_e.at(0); else return float(-1);")
               .Define("lep1_pt","if (selected_muons_pt.size()>=2) return selected_muons_pt.at(0); else if (selected_electrons_pt.size()>=2) return selected_electrons_pt.at(0); else return float(-1);")
              .Define("lep2_pt","if (selected_muons_pt.size()>=2) return selected_muons_pt.at(1); else if (selected_electrons_pt.size()>=2) return selected_electrons_pt.at(1); else return float(-1);")
               .Define("lep1_eta","if (selected_muons_eta.size()>=2) return selected_muons_eta.at(0); else if (selected_electrons_eta.size()>=2) return selected_electrons_eta.at(0); else return float(-5);")
               .Define("lep2_eta","if (selected_muons_eta.size()>=2) return selected_muons_eta.at(1); else if (selected_electrons_eta.size()>=2) return selected_electrons_eta.at(1); else return float(-5);")
               .Define("lep1_e","if (selected_muons_e.size()>=2) return selected_muons_e.at(0); else if (selected_electrons_e.size()>=2) return selected_electrons_e.at(0); else return float(-1);")
               .Define("lep2_e","if (selected_muons_e.size()>=2) return selected_muons_e.at(1); else if (selected_electrons_e.size()>=2) return selected_electrons_e.at(1); else return float(-1);")
               .Define("lep1_pz","if (selected_muons_pt.size()>=2) return selected_muons_pt.at(0)*sinh(selected_muons_eta.at(0)); else if (selected_electrons_pt.size()>=2) return selected_electrons_pt.at(0)*sinh(selected_electrons_eta.at(0)); else return float(-1000);")
               .Define("lep2_pz","if (selected_muons_pt.size()>=2) return selected_muons_pt.at(1)*sinh(selected_muons_eta.at(1)); else if (selected_electrons_pt.size()>=2) return selected_electrons_pt.at(1)*sinh(selected_electrons_eta.at(1)); else return float(-1000);")
               .Define("lep1_charge","if (selected_muons_charge.size()>=2) return selected_muons_charge.at(0); else if (selected_electrons_charge.size()>=2) return selected_electrons_charge.at(0); else return float(-2);")
               .Define("lep2_charge","if (selected_muons_charge.size()>=2) return selected_muons_charge.at(1); else if (selected_electrons_charge.size()>=2) return selected_electrons_charge.at(1); else return float(-2);")
               .Define("lep_chargeprod","return lep1_charge*lep2_charge;")

               .Define("lepp_e","if (lep1_charge>0) return lep1_e; else return lep2_e")
               .Define("lepm_e","if (lep1_charge<0) return lep1_e; else return lep2_e")
               .Define("lepp_pz","if (lep1_charge>0) return lep1_pz; else return lep2_pz")
               .Define("lepm_pz","if (lep1_charge<0) return lep1_pz; else return lep2_pz")


               .Define("cosDphiLep","if (selected_muons_eta.size()>=2) return TMath::Cos(selected_muons_phi.at(0)-selected_muons_phi.at(1)); else if (selected_electrons_eta.size()>=2) return TMath::Cos(selected_electrons_phi.at(0)-selected_electrons_phi.at(1)); else return double(-1.1);")
               .Define("jet1_pt","if (seljet_pt.size()>=1) return seljet_pt.at(0); else return float(-1.);")
               .Define("jet1_eta","if (seljet_eta.size()>=1) return seljet_eta.at(0); else return float(-5.);")
               .Define("jet1_e","if (seljet_e.size()>=1) return seljet_e.at(0); else return float(-1.);")
               .Define("jet2_pt","if (seljet_pt.size()>=2) return seljet_pt.at(1); else return float(-1.);")
               .Define("jet2_eta","if (seljet_eta.size()>=2) return seljet_eta.at(1); else return float(-5.);")
               .Define("jet2_e","if (seljet_e.size()>=2) return seljet_e.at(1); else return float(-1.);")
               .Define("n_seljets","return seljet_pt.size()")

               .Define("p1plus","1/sqrt(2)*(lepm_e+lepm_pz)")
               .Define("p2plus","1/sqrt(2)*(lepp_e+lepp_pz)")
               .Define("p1minus","1/sqrt(2)*(lepm_e-lepm_pz)")
               .Define("p2minus","1/sqrt(2)*(lepp_e-lepp_pz)")
               .Define("cosThetaStar","2*(p1plus*p2minus-p1minus*p2plus)/(Zcand_m*sqrt(Zcand_m*Zcand_m+Zcand_pt*Zcand_pt))")
               .Define("cosThetaR","Zcand_pz/abs(Zcand_pz)*cosThetaStar")

               #Define new var rdf entry (example)
               #.Define("entry", "rdfentry_")
               #Define a weight based on entry (inline example of possible operations)
               #.Define("weight", "return 1./(entry+1)")
               #Define a variable based on a custom filter
               #.Define("MyFilter", "myFilter(zed_leptonic_m)")
               )
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
            "n_photons","n_muons","n_electrons"

        ]
        return branchList




