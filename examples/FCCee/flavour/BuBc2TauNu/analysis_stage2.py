runTraining=False

#TRAINING
processList_training = {
    'p8_ee_Zbb_ecm91':{},
    'p8_ee_Zcc_ecm91':{},
    'p8_ee_Zuds_ecm91':{},
    'p8_ee_Zbb_ecm91_EvtGen_Bc2TauNuTAUHADNU':{},
    'p8_ee_Zbb_ecm91_EvtGen_Bu2TauNuTAUHADNU':{}
}
inputDir_training   = "/eos/experiment/fcc/ee/analyses/case-studies/flavour/BuBc2TauNu/flatNtuples/spring2021/prod_04/training_stage1/"
outputDir_training  = "/eos/experiment/fcc/ee/analyses/case-studies/flavour/BuBc2TauNu/flatNtuples/spring2021/prod_04/training_stage2/"

#analysis_stage1
processList_analysis = {
    'p8_ee_Zbb_ecm91':{},
    'p8_ee_Zcc_ecm91':{},
    'p8_ee_Zuds_ecm91':{},
    'p8_ee_Zbb_ecm91_EvtGen_Bc2TauNuTAUHADNU':{},
    'p8_ee_Zbb_ecm91_EvtGen_Bu2TauNuTAUHADNU':{},
    'p8_ee_Zbb_ecm91_EvtGen_Bd2D3Pi':{},
    'p8_ee_Zbb_ecm91_EvtGen_Bd2DDs':{},
    'p8_ee_Zbb_ecm91_EvtGen_Bd2DTauNu':{},
    'p8_ee_Zbb_ecm91_EvtGen_Bd2Dst3Pi':{},
    'p8_ee_Zbb_ecm91_EvtGen_Bd2DstDs':{},
    'p8_ee_Zbb_ecm91_EvtGen_Bd2DstDsst':{},
    'p8_ee_Zbb_ecm91_EvtGen_Bd2DstTauNu':{},

    'p8_ee_Zbb_ecm91_EvtGen_Bs2Ds3Pi':{},
    'p8_ee_Zbb_ecm91_EvtGen_Bs2DsDs':{},
    'p8_ee_Zbb_ecm91_EvtGen_Bs2DsTauNu':{},
    'p8_ee_Zbb_ecm91_EvtGen_Bs2Dsst3Pi':{},
    'p8_ee_Zbb_ecm91_EvtGen_Bs2DsstDs':{},
    'p8_ee_Zbb_ecm91_EvtGen_Bs2DsstDsst':{},
    'p8_ee_Zbb_ecm91_EvtGen_Bs2DsstTauNu':{},

    'p8_ee_Zbb_ecm91_EvtGen_Bu2D03Pi':{},
    'p8_ee_Zbb_ecm91_EvtGen_Bu2D0Ds':{},
    'p8_ee_Zbb_ecm91_EvtGen_Bu2D0TauNu':{},
    'p8_ee_Zbb_ecm91_EvtGen_Bu2Dst03Pi':{},
    'p8_ee_Zbb_ecm91_EvtGen_Bu2Dst0Ds':{},
    'p8_ee_Zbb_ecm91_EvtGen_Bu2Dst0Dsst':{},
    'p8_ee_Zbb_ecm91_EvtGen_Bu2Dst0TauNu':{},

    'p8_ee_Zbb_ecm91_EvtGen_Lb2Lc3Pi':{},
    'p8_ee_Zbb_ecm91_EvtGen_Lb2LcDs':{},
    'p8_ee_Zbb_ecm91_EvtGen_Lb2LcTauNu':{},
    'p8_ee_Zbb_ecm91_EvtGen_Lb2Lcst3Pi':{},
    'p8_ee_Zbb_ecm91_EvtGen_Lb2LcstDs':{},
    'p8_ee_Zbb_ecm91_EvtGen_Lb2LcstDsst':{},
    'p8_ee_Zbb_ecm91_EvtGen_Lb2LcstTauNu':{}
    }
inputDir_analysis   = "/eos/experiment/fcc/ee/analyses/case-studies/flavour/BuBc2TauNu/flatNtuples/spring2021/prod_04/analysis_stage1/"
outputDir_analysis  = "/eos/experiment/fcc/ee/analyses/case-studies/flavour/BuBc2TauNu/flatNtuples/spring2021/prod_04/analysis_stage2/"

processList  = processList_analysis
outputDir    = outputDir_analysis
inputDir     = inputDir_analysis
MVA1Filter   = "EVT_MVA1Bis>0.6"
MVA2Filter   = "EVT_MVA2_bu>0.6||EVT_MVA2_bc>0.6"

if runTraining:
    processList  = processList_training
    outputDir    = outputDir_training
    inputDir     = inputDir_training
    MVA2Filter    = "1"

nCPUS       = 8


import ROOT
ROOT.gInterpreter.ProcessLine('''
TMVA::Experimental::RBDT<> bdt("BuBc_BDT2", "/afs/cern.ch/work/x/xzuo/public/FCC_files/BuBc2TauNu/data/ROOT/xgb_bdt_stage2_Bu_vs_Bc_vs_qq_multi.root");
computeModel = TMVA::Experimental::Compute<21, float>(bdt);

TMVA::Experimental::RBDT<> bdt("BuBc_BDT", "/afs/cern.ch/work/x/xzuo/public/FCC_files/BuBc2TauNu/data/ROOT/xgb_bdt_BuBc_vtx.root");
computeModel1 = TMVA::Experimental::Compute<18, float>(bdt);
''')


#Mandatory: RDFanalysis class where the use defines the operations on the TTree
class RDFanalysis():

    #__________________________________________________________
    #Mandatory: analysers funtion to define the analysers to process, please make sure you return the last dataframe, in this example it is df2
    def analysers(df):
        df2 = (
            df
               #a candidate is found with a mass
               .Define("CUT_CandInd",     "myFinalSel::selTauCand(Tau23PiCandidates_mass, Tau23PiCandidates_vertex, Vertex_chi2 )")
               .Filter("CUT_CandInd>-1")

               .Define("CUT_CandTruth",   "myFinalSel::selTauCandTM(Tau23PiCandidates_mcvertex, TrueTau23PiBc_vertex, CUT_CandInd)")
               .Define("CUT_CandTruth2",   "myFinalSel::selTauCandTM(Tau23PiCandidates_mcvertex, TrueTau23PiBu_vertex, CUT_CandInd)")

               .Define("CUT_CandRho",      "if ((Tau23PiCandidates_rho1mass.at(CUT_CandInd)<1. && Tau23PiCandidates_rho2mass.at(CUT_CandInd)>0.6 && Tau23PiCandidates_rho2mass.at(CUT_CandInd)<1.0)|| (Tau23PiCandidates_rho2mass.at(CUT_CandInd)<1. && Tau23PiCandidates_rho1mass.at(CUT_CandInd)>0.6 && Tau23PiCandidates_rho1mass.at(CUT_CandInd)<1.)) return 1; else return 0;")
               .Filter("CUT_CandRho>0")

               .Define("EVT_CandMass",     "Tau23PiCandidates_mass.at(CUT_CandInd)")
               .Filter("EVT_CandMass<1.8")

               .Define("LOCAL_CandVtxInd", "Tau23PiCandidates_vertex.at(CUT_CandInd)")
               ##LOCAL INDEX screwed up in prod02!!!! need -1 because PV is removed
               .Define("CUT_CandVtxThrustEmin", "Vertex_thrusthemis_emin.at(LOCAL_CandVtxInd)")
               .Filter("CUT_CandVtxThrustEmin>0")

               .Define("EVT_CandN",           "float(Tau23PiCandidates_vertex.size())")
               .Define("EVT_CandPx",          "Tau23PiCandidates_px.at(CUT_CandInd)")
               .Define("EVT_CandPy",          "Tau23PiCandidates_py.at(CUT_CandInd)")
               .Define("EVT_CandPz",          "Tau23PiCandidates_pz.at(CUT_CandInd)")
               .Define("EVT_CandP",           "Tau23PiCandidates_p.at(CUT_CandInd)")
               .Define("EVT_CandD0",          "Tau23PiCandidates_d0.at(CUT_CandInd)")
               .Define("EVT_CandZ0",          "Tau23PiCandidates_z0.at(CUT_CandInd)")
               .Define("EVT_CandAngleThrust", "Tau23PiCandidates_anglethrust.at(CUT_CandInd)")

               .Define("EVT_CandRho1Mass", "Tau23PiCandidates_rho1mass.at(CUT_CandInd)" )
               .Define("EVT_CandRho2Mass", "Tau23PiCandidates_rho2mass.at(CUT_CandInd)")

               .Define("EVT_CandVtxFD",    "Vertex_d2PV.at(LOCAL_CandVtxInd)")
               .Define("EVT_CandVtxFDErr", "Vertex_d2PVErr.at(LOCAL_CandVtxInd)")
               .Define("EVT_CandVtxChi2",  "Vertex_chi2.at(LOCAL_CandVtxInd)")

               .Define("EVT_CandPion1P",          "Tau23PiCandidates_pion1p.at(CUT_CandInd)")
               .Define("EVT_CandPion2P",          "Tau23PiCandidates_pion2p.at(CUT_CandInd)")
               .Define("EVT_CandPion3P",          "Tau23PiCandidates_pion3p.at(CUT_CandInd)")

               .Define("EVT_CandPion1D0",         "Tau23PiCandidates_pion1d0.at(CUT_CandInd)")
               .Define("EVT_CandPion2D0",         "Tau23PiCandidates_pion2d0.at(CUT_CandInd)")
               .Define("EVT_CandPion3D0",         "Tau23PiCandidates_pion3d0.at(CUT_CandInd)")

               .Define("EVT_CandPion1Z0",         "Tau23PiCandidates_pion1z0.at(CUT_CandInd)")
               .Define("EVT_CandPion2Z0",         "Tau23PiCandidates_pion2z0.at(CUT_CandInd)")
               .Define("EVT_CandPion3Z0",         "Tau23PiCandidates_pion3z0.at(CUT_CandInd)")

               .Define("EVT_Nominal_B_E", "float(91.1876 - EVT_ThrustEmin_E - EVT_ThrustEmax_E + sqrt(EVT_CandP*EVT_CandP + EVT_CandMass*EVT_CandMass))")
               .Define("EVT_DVd0_min", "myFinalSel::get_min(DV_d0, EVT_CandD0)")
               .Define("EVT_DVd0_max", "myFinalSel::get_max(DV_d0, EVT_CandD0)")
               .Define("EVT_DVd0_ave", "myFinalSel::get_ave(DV_d0, EVT_CandD0)")

               .Define("EVT_DVz0_min", "myFinalSel::get_min(DV_z0, EVT_CandZ0)")
               .Define("EVT_DVz0_max", "myFinalSel::get_max(DV_z0, EVT_CandZ0)")
               .Define("EVT_DVz0_ave", "myFinalSel::get_ave(DV_z0, EVT_CandZ0)")

               .Define("EVT_DVmass_min", "myFinalSel::get_min(Vertex_mass, Vertex_isPV, LOCAL_CandVtxInd)")
               .Define("EVT_DVmass_max", "myFinalSel::get_max(Vertex_mass, Vertex_isPV, LOCAL_CandVtxInd)")
               .Define("EVT_DVmass_ave", "myFinalSel::get_ave(Vertex_mass, Vertex_isPV, LOCAL_CandVtxInd)")
               .Define("EVT_PVmass", "Vertex_mass.at(0)")

               .Define("MVAVec1Bis", ROOT.computeModel1, ("EVT_ThrustEmin_E",        "EVT_ThrustEmax_E",
                                                        "EVT_ThrustEmin_Echarged", "EVT_ThrustEmax_Echarged",
                                                        "EVT_ThrustEmin_Eneutral", "EVT_ThrustEmax_Eneutral",
                                                        "EVT_ThrustEmin_Ncharged", "EVT_ThrustEmax_Ncharged",
                                                        "EVT_ThrustEmin_Nneutral", "EVT_ThrustEmax_Nneutral",
                                                        "EVT_NtracksPV",           "EVT_NVertex",
                                                        "EVT_NTau23Pi",            "EVT_ThrustEmin_NDV",
                                                        "EVT_ThrustEmax_NDV",      "EVT_dPV2DVmin",
                                                        "EVT_dPV2DVmax",           "EVT_dPV2DVave"))
               .Define("EVT_MVA1Bis", "MVAVec1Bis.at(0)")
               .Filter(MVA1Filter)

               .Define("MVAVec", ROOT.computeModel, ("EVT_CandMass",        "EVT_CandRho1Mass", "EVT_CandRho2Mass",
                                                     "EVT_CandN",           "EVT_CandVtxFD",    "EVT_CandVtxChi2",
                                                     "EVT_CandPx",          "EVT_CandPy",       "EVT_CandPz",
                                                     "EVT_CandP",           "EVT_CandD0",       "EVT_CandZ0",
                                                     "EVT_CandAngleThrust", "EVT_DVd0_min",     "EVT_DVd0_max",
                                                     "EVT_DVd0_ave",        "EVT_DVz0_min",     "EVT_DVz0_max",
                                                     "EVT_DVz0_ave",        "EVT_PVmass",       "EVT_Nominal_B_E"))


               .Define("EVT_MVA2_bkg", "MVAVec.at(0)")
               .Define("EVT_MVA2_bu", "MVAVec.at(1)")
               .Define("EVT_MVA2_bc", "MVAVec.at(2)")

               .Filter(MVA2Filter)

               .Define("EVT_minRhoMass", "if (EVT_CandRho1Mass<EVT_CandRho2Mass) return EVT_CandRho1Mass; else return EVT_CandRho2Mass;")
               .Define("EVT_maxRhoMass", "if (EVT_CandRho1Mass>EVT_CandRho2Mass) return EVT_CandRho1Mass; else return EVT_CandRho2Mass;")
               .Define("EVT_ThrustDiff_E",        "EVT_ThrustEmax_E-EVT_ThrustEmin_E")
               .Define("EVT_ThrustDiff_N",        "EVT_ThrustEmax_N-EVT_ThrustEmin_N")
               .Define("EVT_ThrustDiff_Echarged", "EVT_ThrustEmax_Echarged-EVT_ThrustEmin_Echarged")
               .Define("EVT_ThrustDiff_Eneutral", "EVT_ThrustEmax_Eneutral-EVT_ThrustEmin_Eneutral")
               .Define("EVT_ThrustDiff_Ncharged", "EVT_ThrustEmax_Ncharged-EVT_ThrustEmin_Ncharged")
               .Define("EVT_ThrustDiff_Nneutral", "EVT_ThrustEmax_Nneutral-EVT_ThrustEmin_Nneutral")

               .Define("LOCAL_CandMCVtxInd", "Tau23PiCandidates_mcvertex.at(CUT_CandInd)")
               .Define("MCVertex_PDG", "MC_Vertex_PDG.at(LOCAL_CandMCVtxInd)")
               .Define("MCVertex_PDGmother", "MC_Vertex_PDGmother.at(LOCAL_CandMCVtxInd)")
               .Define("MCVertex_PDGgmother", "MC_Vertex_PDGgmother.at(LOCAL_CandMCVtxInd)")
               .Define("MCVertex_n", "int(MC_Vertex_PDG.at(LOCAL_CandMCVtxInd).size())")
               .Define("MCVertex_nmother", "int(MC_Vertex_PDGmother.at(LOCAL_CandMCVtxInd).size())")
               .Define("MCVertex_ngmother", "int(MC_Vertex_PDGgmother.at(LOCAL_CandMCVtxInd).size())")
           )
        return df2

    #__________________________________________________________
    #Mandatory: output function, please make sure you return the branchlist as a python list
    def output():
        branchList = [
                "CUT_CandTruth",
                "CUT_CandTruth2",
                "CUT_CandRho",
                "CUT_CandVtxThrustEmin",

                "EVT_ThrustEmin_E",          "EVT_ThrustEmax_E",
                "EVT_ThrustEmin_Echarged",   "EVT_ThrustEmax_Echarged",
                "EVT_ThrustEmin_Eneutral",   "EVT_ThrustEmax_Eneutral",
                "EVT_ThrustEmin_Ncharged",   "EVT_ThrustEmax_Ncharged",
                "EVT_ThrustEmin_Nneutral",   "EVT_ThrustEmax_Nneutral",
                "EVT_ThrustEmin_NDV",        "EVT_ThrustEmax_NDV",
                "EVT_ThrustDiff_E",          "EVT_ThrustDiff_N",
                "EVT_ThrustDiff_Echarged",   "EVT_ThrustDiff_Eneutral",
                "EVT_ThrustDiff_Ncharged",   "EVT_ThrustDiff_Nneutral",
                "EVT_Thrust_Mag",
                "EVT_Thrust_X",  "EVT_Thrust_XErr",
                "EVT_Thrust_Y",  "EVT_Thrust_YErr",
                "EVT_Thrust_Z",  "EVT_Thrust_ZErr",

                "EVT_CandN",
                "EVT_CandMass","EVT_CandRho1Mass","EVT_CandRho2Mass",
                "EVT_CandVtxFD","EVT_CandVtxFDErr", "EVT_CandVtxChi2",
                "EVT_CandPx","EVT_CandP","EVT_CandPz","EVT_CandPy",
                "EVT_CandD0","EVT_CandZ0","EVT_CandAngleThrust",
                "EVT_minRhoMass", "EVT_maxRhoMass",
                "EVT_MVA1", "EVT_MVA2_bkg", "EVT_MVA2_bu", "EVT_MVA2_bc",  "EVT_MVA1Bis",

                "EVT_CandPion1P","EVT_CandPion1D0","EVT_CandPion1Z0",
                "EVT_CandPion2P","EVT_CandPion2D0","EVT_CandPion2Z0",
                "EVT_CandPion3P","EVT_CandPion3D0","EVT_CandPion3Z0",

                "EVT_DVd0_min", "EVT_DVd0_max", "EVT_DVd0_ave",
                "EVT_DVz0_min", "EVT_DVz0_max", "EVT_DVz0_ave",
                "EVT_DVmass_min", "EVT_DVmass_max", "EVT_DVmass_ave",
                "EVT_PVmass",
                "EVT_Nominal_B_E",
                "MCVertex_PDG","MCVertex_PDGmother","MCVertex_PDGgmother","MCVertex_n","MCVertex_nmother","MCVertex_ngmother",
                "MC_PDG","MC_M1","MC_M2","MC_n","MC_D1","MC_D2",
                "TrueTau23PiBc_vertex",  "TrueTau23PiBu_vertex"
                ]
        return branchList
