#Input directory where the files produced at the pre-selection level are
inputDir  = "/eos/user/a/amagnan/FCC/iDMprod/winter2023/stage3/"


outputDir  = "iDM/final/"

#Integrated luminosity for scaling number of events (required only if setting doScale to true)
intLumi = 5e6 #pb^-1

#Scale event yields by intLumi and cross section (optional)
doScale = True

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
}

#Link to the dictonary that contains all the cross section informations etc...
procDict = "FCCee_procDict_winter2023_IDEA.json"

#Add signals as it is not an offical process
procDictAdd={
    "e240_bp1_h2h2ll":{"numberOfEvents": 500000, "sumOfWeights": 500000, "crossSection": 0.0069, "kfactor": 1.0, "matchingEfficiency": 1.0},
    "e240_bp2_h2h2ll":{"numberOfEvents": 500000, "sumOfWeights": 500000, "crossSection":  0.005895, "kfactor": 1.0, "matchingEfficiency": 1.0},
    "e240_bp3_h2h2ll":{"numberOfEvents": 500000, "sumOfWeights": 500000, "crossSection":  0.004973, "kfactor": 1.0, "matchingEfficiency": 1.0},
    "e240_bp4_h2h2ll":{"numberOfEvents": 500000, "sumOfWeights": 500000, "crossSection":  0.007531, "kfactor": 1.0, "matchingEfficiency": 1.0},
    "e240_bp5_h2h2ll":{"numberOfEvents": 500000, "sumOfWeights": 500000, "crossSection":  0.006796, "kfactor": 1.0, "matchingEfficiency": 1.0},
    "e240_bp6_h2h2ll":{"numberOfEvents": 500000, "sumOfWeights": 500000, "crossSection":  0.002677, "kfactor": 1.0, "matchingEfficiency": 1.0},
    "e240_bp7_h2h2ll":{"numberOfEvents": 500000, "sumOfWeights": 500000, "crossSection":  0.001536, "kfactor": 1.0, "matchingEfficiency": 1.0},
    "e240_bp8_h2h2ll":{"numberOfEvents": 500000, "sumOfWeights": 500000, "crossSection":  0.001103, "kfactor": 1.0, "matchingEfficiency": 1.0},
    "e240_bp9_h2h2ll":{"numberOfEvents": 500000, "sumOfWeights": 500000, "crossSection":  0.0004448, "kfactor": 1.0, "matchingEfficiency": 1.0},
    "e240_bp10_h2h2ll":{"numberOfEvents": 500000, "sumOfWeights": 500000, "crossSection":  0.0008526, "kfactor": 1.0, "matchingEfficiency": 1.0},
    "e240_bp11_h2h2ll":{"numberOfEvents": 500000, "sumOfWeights": 500000, "crossSection":  4.716e-05, "kfactor": 1.0, "matchingEfficiency": 1.0},
    "e240_bp12_h2h2ll":{"numberOfEvents": 500000, "sumOfWeights": 500000, "crossSection":  0.0001749, "kfactor": 1.0, "matchingEfficiency": 1.0},
    "e240_bp13_h2h2ll":{"numberOfEvents": 500000, "sumOfWeights": 500000, "crossSection":  1.933e-07, "kfactor": 1.0, "matchingEfficiency": 1.0},
    "e240_bp14_h2h2ll":{"numberOfEvents": 500000, "sumOfWeights": 500000, "crossSection":  1.61e-07, "kfactor": 1.0, "matchingEfficiency": 1.0},
    "e240_bp18_h2h2ll":{"numberOfEvents": 500000, "sumOfWeights": 500000, "crossSection":  2.88e-05, "kfactor": 1.0, "matchingEfficiency": 1.0},
    "e240_bp19_h2h2ll":{"numberOfEvents": 500000, "sumOfWeights": 500000, "crossSection":  1.467e-07, "kfactor": 1.0, "matchingEfficiency": 1.0},
    "e240_bp20_h2h2ll":{"numberOfEvents": 500000, "sumOfWeights": 500000, "crossSection":  0.001014, "kfactor": 1.0, "matchingEfficiency": 1.0},
    "e240_bp1_h2h2llvv":{"numberOfEvents": 500000, "sumOfWeights": 500000, "crossSection":  0.001303, "kfactor": 1.0, "matchingEfficiency": 1.0},
    "e240_bp2_h2h2llvv":{"numberOfEvents": 500000, "sumOfWeights": 500000, "crossSection":  0.0009189, "kfactor": 1.0, "matchingEfficiency": 1.0},
    "e240_bp3_h2h2llvv":{"numberOfEvents": 500000, "sumOfWeights": 500000, "crossSection":  0.005148, "kfactor": 1.0, "matchingEfficiency": 1.0},
    "e240_bp4_h2h2llvv":{"numberOfEvents": 500000, "sumOfWeights": 500000, "crossSection":  2.634e-06, "kfactor": 1.0, "matchingEfficiency": 1.0},
    "e240_bp5_h2h2llvv":{"numberOfEvents": 500000, "sumOfWeights": 500000, "crossSection":  1.769e-06, "kfactor": 1.0, "matchingEfficiency": 1.0},
    "e240_bp6_h2h2llvv":{"numberOfEvents": 500000, "sumOfWeights": 500000, "crossSection":  1.615e-07, "kfactor": 1.0, "matchingEfficiency": 1.0},
    "e240_bp7_h2h2llvv":{"numberOfEvents": 500000, "sumOfWeights": 500000, "crossSection":  3.531e-08, "kfactor": 1.0, "matchingEfficiency": 1.0},
    "e240_bp8_h2h2llvv":{"numberOfEvents": 500000, "sumOfWeights": 500000, "crossSection":  2.433e-08, "kfactor": 1.0, "matchingEfficiency": 1.0},
    "e240_bp9_h2h2llvv":{"numberOfEvents": 400002, "sumOfWeights": 400002, "crossSection":  1.218e-10, "kfactor": 1.0, "matchingEfficiency": 1.0},
    "e240_bp10_h2h2llvv":{"numberOfEvents": 500000, "sumOfWeights": 500000, "crossSection":  5.058e-08, "kfactor": 1.0, "matchingEfficiency": 1.0},
    "e240_bp11_h2h2llvv":{"numberOfEvents": 63, "sumOfWeights": 63, "crossSection":  2.346e-10, "kfactor": 1.0, "matchingEfficiency": 1.0},
    "e240_bp12_h2h2llvv":{"numberOfEvents": 200614, "sumOfWeights": 200614, "crossSection":  6.152e-11, "kfactor": 1.0, "matchingEfficiency": 1.0},
    "e240_bp13_h2h2llvv":{"numberOfEvents": 500000, "sumOfWeights": 500000, "crossSection":  1.754e-11, "kfactor": 1.0, "matchingEfficiency": 1.0},
    "e240_bp14_h2h2llvv":{"numberOfEvents": 500000, "sumOfWeights": 500000, "crossSection":  1.634e-11, "kfactor": 1.0, "matchingEfficiency": 1.0},
    "e240_bp18_h2h2llvv":{"numberOfEvents": 500000, "sumOfWeights": 500000, "crossSection":  3.792e-09, "kfactor": 1.0, "matchingEfficiency": 1.0},
    "e240_bp19_h2h2llvv":{"numberOfEvents": 500000, "sumOfWeights": 500000, "crossSection":  1.674e-11, "kfactor": 1.0, "matchingEfficiency": 1.0},
    "e240_bp20_h2h2llvv":{"numberOfEvents": 400004, "sumOfWeights": 400004, "crossSection":  7.768e-09, "kfactor": 1.0, "matchingEfficiency": 1.0},
}

#Number of CPUs to use
nCPUS = 4

#produces ROOT TTrees, default is False
doTree = False

###Dictionnay of the list of cuts. The key is the name of the selection that will be added to the output file
cutList = {
    "TwoEle":"n_electrons==2 && n_muons==0 && Zcand_m<120 && TMath::Abs(Zcand_pz)<70 && MET_pt[0]>5",
    "TwoEleVetoObj":"Zcand_m<120 && TMath::Abs(Zcand_pz)<70 && n_electrons==2 && n_muons==0 && n_seljets<1 && n_photons==0 && MET_pt[0]>5",
    "TwoEleLepCuts":"Zcand_m<120 && TMath::Abs(Zcand_pz)<70 && n_electrons==2 && n_muons==0 && n_seljets<1 && n_photons==0 && MET_pt[0]>5 && lep1_pt<80 && lep2_pt<60",
    "TwoElePoverE":"Zcand_m<120 && TMath::Abs(Zcand_pz)<70 && n_electrons==2 && n_muons==0 && n_seljets<1 && n_photons==0 && MET_pt[0]>5 && lep1_pt<80 && lep2_pt<60 && Zcand_povere>0.1",
    "TwoMu":"n_electrons==0 && n_muons==2 && Zcand_m<120 && TMath::Abs(Zcand_pz)<70 && MET_pt[0]>5",
    "TwoMuVetoObj":"Zcand_m<120 && TMath::Abs(Zcand_pz)<70 && n_electrons==0 && n_muons==2 && n_seljets<1 && n_photons==0 && MET_pt[0]>5",
    "TwoMuLepCuts":"Zcand_m<120 && TMath::Abs(Zcand_pz)<70 && n_electrons==0 && n_muons==2 && n_seljets<1 && n_photons==0 && MET_pt[0]>5 && lep1_pt<80 && lep2_pt<60",
    "TwoMuPoverE":"Zcand_m<120 && TMath::Abs(Zcand_pz)<70 && n_electrons==0 && n_muons==2 && n_seljets<1 && n_photons==0 && MET_pt[0]>5 && lep1_pt<80 && lep2_pt<60 && Zcand_povere>0.1",
}


#Dictionary for the ouput variable/hitograms. The key is the name of the variable in the output files. "name" is the name of the variable in the input file, "title" is the x-axis label of the histogram, "bin" the number of bins of the histogram, "xmin" the minimum x-axis value and "xmax" the maximum x-axis value.
histoList = {
    "bdt_output_bp1":{"name":"bdt_output_bp1","title":"BDT output","bin":100,"xmin":-1,"xmax":0.5},
    "bdt_output_bp2":{"name":"bdt_output_bp2","title":"BDT output","bin":100,"xmin":-1,"xmax":0.5},
    "bdt_output_bp6":{"name":"bdt_output_bp6","title":"BDT output","bin":100,"xmin":-1,"xmax":0.5},
    "bdt_output_bp8":{"name":"bdt_output_bp8","title":"BDT output","bin":100,"xmin":-1,"xmax":0.5},
    "n_seljets":{"name":"n_seljets","title":"Number of cleaned jets","bin":10,"xmin":0,"xmax":10},
    "n_photons":{"name":"n_photons","title":"Number of photons","bin":10,"xmin":0,"xmax":10},
#    "n_electrons":{"name":"n_electrons","title":"Number of electrons","bin":10,"xmin":0,"xmax":10},
#    "n_muons":{"name":"n_muons","title":"Number of muons","bin":10,"xmin":0,"xmax":10},
    "mZ":{"name":"Zcand_m","title":"m_{ll} [GeV]","bin":60,"xmin":0,"xmax":240},
    "mZzoom":{"name":"Zcand_m","title":"m_{ll} [GeV]","bin":60,"xmin":0,"xmax":120},
    "ptZ":{"name":"Zcand_pt","title":"p_{T}^{ll} [GeV]","bin":50,"xmin":0,"xmax":150},
    "mZrecoil":{"name":"Zcand_recoil_m","title":"Z recoil [GeV]","bin":50,"xmin":0,"xmax":250},
    "photon1_pt":{"name":"photon1_pt","title":"p_{T}^{photon1} [GeV]","bin":50,"xmin":-1,"xmax":200},
    "photon1_eta":{"name":"photon1_eta","title":"#eta^{photon1}","bin":50,"xmin":-5,"xmax":5},
    "photon1_e":{"name":"photon1_e","title":"E^{photon1} [GeV]","bin":60,"xmin":-1,"xmax":120},
    "lep1_pt":{"name":"lep1_pt","title":"p_{T}^{lep1} [GeV]","bin":50,"xmin":0,"xmax":200},
    "lep1_eta":{"name":"lep1_eta","title":"#eta^{lep1}","bin":50,"xmin":-5,"xmax":5},
    "lep1_e":{"name":"lep1_e","title":"E^{lep1} [GeV]","bin":60,"xmin":0,"xmax":120},
    "lep1_charge":{"name":"lep1_charge","title":"charge^{lep1}","bin":4,"xmin":-2,"xmax":2},
    "lep2_pt":{"name":"lep2_pt","title":"p_{T}^{lep2} [GeV]","bin":50,"xmin":0,"xmax":200},
    "lep2_eta":{"name":"lep2_eta","title":"#eta^{lep2}","bin":50,"xmin":-5,"xmax":5},
    "lep2_e":{"name":"lep2_e","title":"E^{lep2} [GeV]","bin":60,"xmin":0,"xmax":120},
    "lep2_charge":{"name":"lep2_charge","title":"charge^{lep2}","bin":4,"xmin":-2,"xmax":2},
    "lep_chargeprod":{"name":"lep_chargeprod","title":"charge^{lep1}*charge^{lep2}","bin":4,"xmin":-2,"xmax":2},
    "jet1_pt":{"name":"jet1_pt","title":"p_{T}^{jet1} [GeV]","bin":50,"xmin":-1,"xmax":200},
    "jet1_eta":{"name":"jet1_eta","title":"#eta^{jet1}","bin":50,"xmin":-5,"xmax":5},
    "jet1_e":{"name":"jet1_e","title":"E^{jet1} [GeV]","bin":60,"xmin":-1,"xmax":120},
    "jet2_pt":{"name":"jet2_pt","title":"p_{T}^{jet2} [GeV]","bin":30,"xmin":-1,"xmax":120},
    "jet2_eta":{"name":"jet2_eta","title":"#eta^{jet2}","bin":50,"xmin":-5,"xmax":5},
    "jet2_e":{"name":"jet2_e","title":"E^{jet2} [GeV]","bin":60,"xmin":-1,"xmax":120},
    "MET_e":{"name":"MET_e","title":"Emiss [GeV]","bin":50,"xmin":0,"xmax":250},
    "MET_pt":{"name":"MET_pt","title":"ETmiss [GeV]","bin":50,"xmin":0,"xmax":250},
    "pZ":{"name":"Zcand_p","title":"p^{ll} [GeV]","bin":50,"xmin":0,"xmax":200},
    "pzZ":{"name":"Zcand_pz","title":"p_{z}^{ll} [GeV]","bin":100,"xmin":-200,"xmax":200},
    "eZ":{"name":"Zcand_e","title":"E^{ll} [GeV]","bin":50,"xmin":0,"xmax":250},
    "povereZ":{"name":"Zcand_povere","title":"p^{ll}/E^{ll}","bin":50,"xmin":0,"xmax":1.5},
    "costhetaZ":{"name":"Zcand_costheta","title":"cos#theta^{ll}","bin":50,"xmin":-1,"xmax":1},
    "cosThetaStar":{"name":"cosThetaStar","title":"cos#theta_{l}^{*}","bin":50,"xmin":-1,"xmax":1},
    "cosThetaR":{"name":"cosThetaR","title":"cos#theta_{R}","bin":50,"xmin":-1,"xmax":1},
    "cosDphiLep":{"name":"cosDphiLep","title":"cos#Delta#phi(ll)","bin":50,"xmin":-1,"xmax":1},
    "pzZ_mZ_2D":{"cols":["Zcand_pz", "Zcand_m"],"title":"p_{z}^{ll} - m^{ll} [GeV]", "bins": [(100,-200,200), (100,0,250)]}, # 2D histogram
}
