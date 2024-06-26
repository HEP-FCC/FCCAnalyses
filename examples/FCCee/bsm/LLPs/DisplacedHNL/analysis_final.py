#Input directory where the files produced at the stage1 level are
inputDir  = "/eos/experiment/fcc/ee/analyses/case-studies/bsm/LLPs/HNLs/"
#inputDir = "/eos/user/j/jalimena/FCCeeLLP/"
#inputDir = "output_stage1/"

#Output directory where the files produced at the final-selection level are
outputDir  = "output_finalSel/"

#Integrated luminosity for scaling number of events (required only if setting doScale to true)
#intLumi = 150e6 #pb^-1

#Scale event yields by intLumi and cross section (optional)
#doScale = True

#Save event yields in a table (optional)
#saveTabular = True

processList = {
    #run over the full statistics from stage1
    'p8_ee_Zee_ecm91':{},
    'p8_ee_Ztautau_ecm91':{},
    'p8_ee_Zbb_ecm91':{},
    'p8_ee_Zcc_ecm91':{},
    'p8_ee_Zuds_ecm91':{},
}

#Link to the dictonary that contains all the cross section information etc...
procDict = "FCCee_procDict_spring2021_IDEA.json"

#Add MySample_p8_ee_ZH_ecm240 as it is not an offical process
procDictAdd={
    #"MySample_p8_ee_ZH_ecm240":{"numberOfEvents": 10000000, "sumOfWeights": 10000000, "crossSection": 0.201868, "kfactor": 1.0, "matchingEfficiency": 1.0}
}

#Number of CPUs to use
nCPUS = 2

#produces ROOT TTrees, default is False
doTree = False

###Dictionnay of the list of cuts. The key is the name of the selection that will be added to the output file
cutList = {
    "selNone": "n_RecoTracks > -1",
    # "sel1FSGenEle": "n_FSGenElectron>0",
    # "sel1FSGenEle_eeInvMassGt80": "n_FSGenElectron>0 && FSGen_ee_invMass >80",
    # "sel1FSGenNu": "n_FSGenNeutrino>0",
    "sel2RecoEle": "n_RecoElectrons==2",
    "sel2RecoEle_vetoes": "n_RecoElectrons==2 && n_RecoMuons==0 && n_RecoPhotons==0 && n_RecoJets==0 && n_RecoPhotons==0",
    # "sel2RecoEle_absD0Gt0p1": "n_RecoElectrons==2 && RecoElectronTrack_absD0[0]>0.1 && RecoElectronTrack_absD0[1]>0.1", #both electrons displaced
    # "sel2RecoEle_chi2Gt0p1": "n_RecoElectrons==2 && RecoDecayVertex.chi2>0.1", #good vertex
    # "sel2RecoEle_chi2Gt0p1_LxyzGt1": "n_RecoElectrons==2 && RecoDecayVertex.chi2>0.1 && Reco_Lxyz>1", #displaced vertex
    "sel2RecoEle_vetoes_MissingEnergyGt10": "n_RecoElectrons==2 && n_RecoMuons==0 && n_RecoPhotons==0 && n_RecoJets==0 && n_RecoPhotons==0 && RecoMissingEnergy_p[0]>10", #missing energy > 10 GeV
    # "sel2RecoEle_vetoes_absD0Gt0p5": "n_RecoElectrons==2 && n_RecoMuons==0 && n_RecoPhotons==0 && n_RecoJets==0 && n_RecoPhotons==0 && RecoElectronTrack_absD0[0]>0.5 && RecoElectronTrack_absD0[1]>0.5", #both electrons displaced
    "sel2RecoEle_vetoes_MissingEnergyGt10_absD0Gt0p5": "n_RecoElectrons==2 && n_RecoMuons==0 && n_RecoPhotons==0 && n_RecoJets==0 && n_RecoPhotons==0 && RecoMissingEnergy_p[0]>10 && RecoElectronTrack_absD0[0]>0.5 && RecoElectronTrack_absD0[1]>0.5", #both electrons displaced
    # "sel2RecoEle_vetoes_MissingEnergyGt10_chi2Gt1_LxyzGt5": "n_RecoElectrons==2 && n_RecoMuons==0 && n_RecoPhotons==0 && n_RecoJets==0 && n_RecoPhotons==0 && RecoMissingEnergy_p[0]>10 && RecoDecayVertex.chi2>1 && Reco_Lxyz>5", #displaced vertex
}

###Dictionary for prettier names of cuts (optional)
cutLabels = {
    "selNone": "Before selection",
    "sel2RecoEle": "Exactly 2 electrons",
    "sel2RecoEle_vetoes": "Veto photons, muons, and jets",
    "sel2RecoEle_vetoes_MissingEnergyGt10": "$\\not\\! p >$ 10 GeV",
    "sel2RecoEle_vetoes_MissingEnergyGt10_absD0Gt0p5": "Electron $|d_0| >$ 0.5 mm",
}

###Dictionary for the ouput variable/hitograms. The key is the name of the variable in the output files. "name" is the name of the variable in the input file, "title" is the x-axis label of the histogram, "bin" the number of bins of the histogram, "xmin" the minimum x-axis value and "xmax" the maximum x-axis value.
histoList = {

    #gen variables
    "n_FSGenElectron":                   {"name":"n_FSGenElectron",                  "title":"Number of final state gen electrons",        "bin":5,"xmin":-0.5 ,"xmax":4.5},

    "FSGenElectron_e":                   {"name":"FSGenElectron_e",                  "title":"Final state gen electrons energy [GeV]",     "bin":100,"xmin":0 ,"xmax":50},
    "FSGenElectron_p":                   {"name":"FSGenElectron_p",                  "title":"Final state gen electrons p [GeV]",          "bin":100,"xmin":0 ,"xmax":50},
    "FSGenElectron_pt":                  {"name":"FSGenElectron_pt",                 "title":"Final state gen electrons p_{T} [GeV]",      "bin":100,"xmin":0 ,"xmax":50},
    "FSGenElectron_pz":                  {"name":"FSGenElectron_pz",                 "title":"Final state gen electrons p_{z} [GeV]",      "bin":100,"xmin":0 ,"xmax":50},
    "FSGenElectron_eta":                 {"name":"FSGenElectron_eta",                "title":"Final state gen electrons #eta",             "bin":60, "xmin":-3,"xmax":3},
    "FSGenElectron_theta":               {"name":"FSGenElectron_theta",              "title":"Final state gen electrons #theta",           "bin":64, "xmin":0,"xmax":3.2},
    "FSGenElectron_phi":                 {"name":"FSGenElectron_phi",                "title":"Final state gen electrons #phi",             "bin":64, "xmin":-3.2,"xmax":3.2},
    "FSGenElectron_charge":              {"name":"FSGenElectron_charge",             "title":"Final state gen electrons charge",           "bin":3, "xmin":-1.5,"xmax":1.5},

    "FSGenElectron_vertex_x": {"name":"FSGenElectron_vertex_x", "title":"Final state gen e^{#font[122]{\55}} production vertex x [mm]",      "bin":100,"xmin":-1000 ,"xmax":1000},
    "FSGenElectron_vertex_y": {"name":"FSGenElectron_vertex_y", "title":"Final state gen e^{#font[122]{\55}} production vertex y [mm]",      "bin":100,"xmin":-1000 ,"xmax":1000},
    "FSGenElectron_vertex_z": {"name":"FSGenElectron_vertex_z", "title":"Final state gen e^{#font[122]{\55}} production vertex z [mm]",      "bin":100,"xmin":-1000 ,"xmax":1000},

    "FSGenElectron_vertex_x_prompt": {"name":"FSGenElectron_vertex_x", "title":"Final state gen e^{#font[122]{\55}} production vertex x [mm]",      "bin":100,"xmin":-0.01 ,"xmax":0.01},
    "FSGenElectron_vertex_y_prompt": {"name":"FSGenElectron_vertex_y", "title":"Final state gen e^{#font[122]{\55}} production vertex y [mm]",      "bin":100,"xmin":-0.01 ,"xmax":0.01},
    "FSGenElectron_vertex_z_prompt": {"name":"FSGenElectron_vertex_z", "title":"Final state gen e^{#font[122]{\55}} production vertex z [mm]",      "bin":100,"xmin":-0.01 ,"xmax":0.01},

    "FSGen_Lxy":      {"name":"FSGen_Lxy",      "title":"Gen L_{xy} [mm]",     "bin":100,"xmin":0 ,"xmax":1000},
    "FSGen_Lxyz":     {"name":"FSGen_Lxyz",     "title":"Gen L_{xyz} [mm]",    "bin":100,"xmin":0 ,"xmax":1000},
    "FSGen_Lxyz_prompt":     {"name":"FSGen_Lxyz",     "title":"Gen L_{xyz} [mm]",    "bin":100,"xmin":0 ,"xmax":10},

    "n_FSGenNeutrino":                   {"name":"n_FSGenNeutrino",                  "title":"Number of final state gen neutrinos",        "bin":5,"xmin":-0.5 ,"xmax":4.5},

    "FSGenNeutrino_e":                   {"name":"FSGenNeutrino_e",                  "title":"Final state gen neutrinos energy [GeV]",     "bin":100,"xmin":0 ,"xmax":50},
    "FSGenNeutrino_p":                   {"name":"FSGenNeutrino_p",                  "title":"Final state gen neutrinos p [GeV]",          "bin":100,"xmin":0 ,"xmax":50},
    "FSGenNeutrino_pt":                  {"name":"FSGenNeutrino_pt",                 "title":"Final state gen neutrinos p_{T} [GeV]",      "bin":100,"xmin":0 ,"xmax":50},
    "FSGenNeutrino_pz":                  {"name":"FSGenNeutrino_pz",                 "title":"Final state gen neutrinos p_{z} [GeV]",      "bin":100,"xmin":0 ,"xmax":50},
    "FSGenNeutrino_eta":                 {"name":"FSGenNeutrino_eta",                "title":"Final state gen neutrinos #eta",             "bin":60, "xmin":-3,"xmax":3},
    "FSGenNeutrino_theta":               {"name":"FSGenNeutrino_theta",              "title":"Final state gen neutrinos #theta",           "bin":64, "xmin":0,"xmax":3.2},
    "FSGenNeutrino_phi":                 {"name":"FSGenNeutrino_phi",                "title":"Final state gen neutrinos #phi",             "bin":64, "xmin":-3.2,"xmax":3.2},
    "FSGenNeutrino_charge":              {"name":"FSGenNeutrino_charge",             "title":"Final state gen neutrinos charge",           "bin":3, "xmin":-1.5,"xmax":1.5},

    "FSGen_ee_invMass":   {"name":"FSGen_ee_invMass",   "title":"Gen m_{ee} [GeV]",           "bin":100,"xmin":0, "xmax":100},
    "FSGen_eenu_invMass": {"name":"FSGen_eenu_invMass", "title":"Gen m_{ee#nu} [GeV]",           "bin":100,"xmin":0, "xmax":100},

    "n_FSGenPhoton":                   {"name":"n_FSGenPhoton",                  "title":"Number of final state gen photons",          "bin":10,"xmin":-0.5 ,"xmax":9.5},
    "FSGenPhoton_e":                   {"name":"FSGenPhoton_e",                  "title":"Final state gen photons energy [GeV]",       "bin":100,"xmin":0 ,"xmax":50},
    "FSGenPhoton_p":                   {"name":"FSGenPhoton_p",                  "title":"Final state gen photons p [GeV]",            "bin":100,"xmin":0 ,"xmax":50},
    "FSGenPhoton_pt":                  {"name":"FSGenPhoton_pt",                 "title":"Final state gen photons p_{T} [GeV]",        "bin":100,"xmin":0 ,"xmax":50},
    "FSGenPhoton_pz":                  {"name":"FSGenPhoton_pz",                 "title":"Final state gen photons p_{z} [GeV]",        "bin":100,"xmin":0 ,"xmax":50},
    "FSGenPhoton_eta":                 {"name":"FSGenPhoton_eta",                "title":"Final state gen photons #eta",               "bin":60, "xmin":-3,"xmax":3},
    "FSGenPhoton_theta":               {"name":"FSGenPhoton_theta",              "title":"Final state gen photons #theta",             "bin":64, "xmin":0,"xmax":3.2},
    "FSGenPhoton_phi":                 {"name":"FSGenPhoton_phi",                "title":"Final state gen photons #phi",               "bin":64, "xmin":-3.2,"xmax":3.2},
    "FSGenPhoton_charge":              {"name":"FSGenPhoton_charge",             "title":"Final state gen photons charge",             "bin":3, "xmin":-1.5,"xmax":1.5},

    #reco variables
    "n_RecoTracks":                    {"name":"n_RecoTracks",                   "title":"Total number of reco tracks",           "bin":5,"xmin":-0.5 ,"xmax":4.5},
    "n_RecoJets":       {"name":"n_RecoJets",      "title":"Total number of reco jets",         "bin":5,"xmin":-0.5 ,"xmax":4.5},
    "n_RecoPhotons":    {"name":"n_RecoPhotons",   "title":"Total number of reco photons",      "bin":5,"xmin":-0.5 ,"xmax":4.5},
    "n_RecoElectrons":  {"name":"n_RecoElectrons", "title":"Total number of reco electrons",    "bin":5,"xmin":-0.5 ,"xmax":4.5},
    "n_RecoMuons":      {"name":"n_RecoMuons",     "title":"Total number of reco muons",        "bin":5,"xmin":-0.5 ,"xmax":4.5},

    "RecoJet_e":        {"name":"RecoJet_e",        "title":"Reco jet energy [GeV]", "bin":100,"xmin":0 ,"xmax":50},
    "RecoJet_p":        {"name":"RecoJet_p",        "title":"Reco jet p [GeV]",      "bin":100,"xmin":0 ,"xmax":50},
    "RecoJet_pt":       {"name":"RecoJet_pt",       "title":"Reco jet p_{T} [GeV]",  "bin":100,"xmin":0 ,"xmax":50},
    "RecoJet_pz":       {"name":"RecoJet_pz",       "title":"Reco jet p_{z} [GeV]",  "bin":100,"xmin":0 ,"xmax":50},
    "RecoJet_eta":      {"name":"RecoJet_eta",      "title":"Reco jet #eta",         "bin":60, "xmin":-3,"xmax":3},
    "RecoJet_theta":    {"name":"RecoJet_theta",    "title":"Reco jet #theta",       "bin":64, "xmin":0,"xmax":3.2},
    "RecoJet_phi":      {"name":"RecoJet_phi",      "title":"Reco jet #phi",         "bin":64, "xmin":-3.2,"xmax":3.2},
    "RecoJet_charge":   {"name":"RecoJet_charge",   "title":"Reco jet charge",       "bin":3, "xmin":-1.5,"xmax":1.5},

    "RecoJetTrack_absD0":             {"name":"RecoJetTrack_absD0",     "title":"Reco jet tracks |d_{0}| [mm]",      "bin":100,"xmin":0, "xmax":2000},
    "RecoJetTrack_absD0_prompt":      {"name":"RecoJetTrack_absD0",     "title":"Reco jet tracks |d_{0}| [mm]",      "bin":100,"xmin":0, "xmax":1},
    "RecoJetTrack_absZ0":             {"name":"RecoJetTrack_absZ0",     "title":"Reco jet tracks |z_{0}| [mm]",      "bin":100,"xmin":0, "xmax":2000},
    "RecoJetTrack_absZ0_prompt":      {"name":"RecoJetTrack_absZ0",     "title":"Reco jet tracks |z_{0}| [mm]",      "bin":100,"xmin":0, "xmax":1},
    "RecoJetTrack_absD0sig":          {"name":"RecoJetTrack_absD0sig",  "title":"Reco jet tracks |d_{0} significance|",      "bin":100,"xmin":0, "xmax":600000},
    "RecoJetTrack_absD0sig_prompt":   {"name":"RecoJetTrack_absD0sig",  "title":"Reco jet tracks |d_{0} significance|",      "bin":100,"xmin":0, "xmax":5},
    "RecoJetTrack_absZ0sig":          {"name":"RecoJetTrack_absZ0sig",  "title":"Reco jet tracks |z_{0} significance|",      "bin":100,"xmin":0, "xmax":600000},
    "RecoJetTrack_absZ0sig_prompt":   {"name":"RecoJetTrack_absZ0sig",  "title":"Reco jet tracks |z_{0} significance|",      "bin":100,"xmin":0, "xmax":5},
    "RecoJetTrack_D0cov":      {"name":"RecoJetTrack_D0cov",     "title":"Reco jet tracks d_{0} #sigma^{2}",      "bin":100,"xmin":0, "xmax":0.5},
    "RecoJetTrack_Z0cov":      {"name":"RecoJetTrack_Z0cov",     "title":"Reco jet tracks z_{0} #sigma^{2}",      "bin":100,"xmin":0, "xmax":0.5},

    "RecoElectron_e":        {"name":"RecoElectron_e",        "title":"Reco electron energy [GeV]", "bin":100,"xmin":0 ,"xmax":50},
    "RecoElectron_p":        {"name":"RecoElectron_p",        "title":"Reco electron p [GeV]",      "bin":100,"xmin":0 ,"xmax":50},
    "RecoElectron_pt":       {"name":"RecoElectron_pt",       "title":"Reco electron p_{T} [GeV]",  "bin":100,"xmin":0 ,"xmax":50},
    "RecoElectron_pz":       {"name":"RecoElectron_pz",       "title":"Reco electron p_{z} [GeV]",  "bin":100,"xmin":0 ,"xmax":50},
    "RecoElectron_eta":      {"name":"RecoElectron_eta",      "title":"Reco electron #eta",         "bin":60, "xmin":-3,"xmax":3},
    "RecoElectron_theta":    {"name":"RecoElectron_theta",    "title":"Reco electron #theta",       "bin":64, "xmin":0,"xmax":3.2},
    "RecoElectron_phi":      {"name":"RecoElectron_phi",      "title":"Reco electron #phi",         "bin":64, "xmin":-3.2,"xmax":3.2},
    "RecoElectron_charge":   {"name":"RecoElectron_charge",   "title":"Reco electron charge",       "bin":3, "xmin":-1.5,"xmax":1.5},

    "RecoElectronTrack_absD0":             {"name":"RecoElectronTrack_absD0",     "title":"Reco electron tracks |d_{0}| [mm]",      "bin":100,"xmin":0, "xmax":2000},
    "RecoElectronTrack_absD0_med":         {"name":"RecoElectronTrack_absD0",     "title":"Reco electron tracks |d_{0}| [mm]",      "bin":100,"xmin":0, "xmax":10},
    "RecoElectronTrack_absD0_prompt":      {"name":"RecoElectronTrack_absD0",     "title":"Reco electron tracks |d_{0}| [mm]",      "bin":100,"xmin":0, "xmax":1},
    "RecoElectronTrack_absZ0":             {"name":"RecoElectronTrack_absZ0",     "title":"Reco electron tracks |z_{0}| [mm]",      "bin":100,"xmin":0, "xmax":2000},
    "RecoElectronTrack_absZ0_prompt":      {"name":"RecoElectronTrack_absZ0",     "title":"Reco electron tracks |z_{0}| [mm]",      "bin":100,"xmin":0, "xmax":1},
    "RecoElectronTrack_absD0sig":          {"name":"RecoElectronTrack_absD0sig",  "title":"Reco electron tracks |d_{0} significance|",      "bin":100,"xmin":0, "xmax":600000},
    "RecoElectronTrack_absD0sig_prompt":   {"name":"RecoElectronTrack_absD0sig",  "title":"Reco electron tracks |d_{0} significance|",      "bin":100,"xmin":0, "xmax":5},
    "RecoElectronTrack_absZ0sig":          {"name":"RecoElectronTrack_absZ0sig",  "title":"Reco electron tracks |z_{0} significance|",      "bin":100,"xmin":0, "xmax":600000},
    "RecoElectronTrack_absZ0sig_prompt":   {"name":"RecoElectronTrack_absZ0sig",  "title":"Reco electron tracks |z_{0} significance|",      "bin":100,"xmin":0, "xmax":5},
    "RecoElectronTrack_D0cov":      {"name":"RecoElectronTrack_D0cov",     "title":"Reco electron tracks d_{0} #sigma^{2}",      "bin":100,"xmin":0, "xmax":0.5},
    "RecoElectronTrack_Z0cov":      {"name":"RecoElectronTrack_Z0cov",     "title":"Reco electron tracks z_{0} #sigma^{2}",      "bin":100,"xmin":0, "xmax":0.5},

    "Reco_DecayVertex_x":           {"name":"RecoDecayVertex.position.x",  "title":"Reco decay vertex x [mm]",            "bin":100,"xmin":-1000 ,"xmax":1000},
    "Reco_DecayVertex_y":           {"name":"RecoDecayVertex.position.y",  "title":"Reco decay vertex y [mm]",            "bin":100,"xmin":-1000 ,"xmax":1000},
    "Reco_DecayVertex_z":           {"name":"RecoDecayVertex.position.z",  "title":"Reco decay vertex z [mm]",            "bin":100,"xmin":-1000 ,"xmax":1000},
    "Reco_DecayVertex_x_prompt":    {"name":"RecoDecayVertex.position.x",  "title":"Reco decay vertex x [mm]",            "bin":100,"xmin":-0.01 ,"xmax":0.01},
    "Reco_DecayVertex_y_prompt":    {"name":"RecoDecayVertex.position.y",  "title":"Reco decay vertex y [mm]",            "bin":100,"xmin":-0.01 ,"xmax":0.01},
    "Reco_DecayVertex_z_prompt":    {"name":"RecoDecayVertex.position.z",  "title":"Reco decay vertex z [mm]",            "bin":100,"xmin":-0.01 ,"xmax":0.01},
    "Reco_DecayVertex_chi2":        {"name":"RecoDecayVertex.chi2",        "title":"Reco decay vertex #chi^{2}",          "bin":100,"xmin":0 ,"xmax":3},
    "Reco_DecayVertex_ndf":         {"name":"RecoDecayVertex.ndf",         "title":"Reco decay vertex fit ndf",           "bin":50,"xmin":0 ,"xmax":50},
    "Reco_Lxy":                     {"name":"Reco_Lxy",                    "title":"Reco L_{xy} [mm]",     "bin":100,"xmin":0 ,"xmax":1000},
    "Reco_Lxyz":                    {"name":"Reco_Lxyz",                   "title":"Reco L_{xyz} [mm]",    "bin":100,"xmin":0 ,"xmax":1000},
    "Reco_Lxyz_prompt":             {"name":"Reco_Lxyz",                   "title":"Reco L_{xyz} [mm]",    "bin":100,"xmin":0 ,"xmax":0.1},

    "Reco_ee_invMass":   {"name":"Reco_ee_invMass",   "title":"Reco m_{ee} [GeV]",           "bin":100,"xmin":0, "xmax":100},

    "RecoPhoton_e":        {"name":"RecoPhoton_e",        "title":"Reco photon energy [GeV]", "bin":100,"xmin":0 ,"xmax":50},
    "RecoPhoton_p":        {"name":"RecoPhoton_p",        "title":"Reco photon p [GeV]",      "bin":100,"xmin":0 ,"xmax":50},
    "RecoPhoton_pt":       {"name":"RecoPhoton_pt",       "title":"Reco photon p_{T} [GeV]",  "bin":100,"xmin":0 ,"xmax":50},
    "RecoPhoton_pz":       {"name":"RecoPhoton_pz",       "title":"Reco photon p_{z} [GeV]",  "bin":100,"xmin":0 ,"xmax":50},
    "RecoPhoton_eta":      {"name":"RecoPhoton_eta",      "title":"Reco photon #eta",         "bin":60, "xmin":-3,"xmax":3},
    "RecoPhoton_theta":    {"name":"RecoPhoton_theta",    "title":"Reco photon #theta",       "bin":64, "xmin":0,"xmax":3.2},
    "RecoPhoton_phi":      {"name":"RecoPhoton_phi",      "title":"Reco photon #phi",         "bin":64, "xmin":-3.2,"xmax":3.2},
    "RecoPhoton_charge":   {"name":"RecoPhoton_charge",   "title":"Reco photon charge",       "bin":3, "xmin":-1.5,"xmax":1.5},

    "RecoMuon_e":        {"name":"RecoMuon_e",        "title":"Reco muon energy [GeV]", "bin":100,"xmin":0 ,"xmax":50},
    "RecoMuon_p":        {"name":"RecoMuon_p",        "title":"Reco muon p [GeV]",      "bin":100,"xmin":0 ,"xmax":50},
    "RecoMuon_pt":       {"name":"RecoMuon_pt",       "title":"Reco muon p_{T} [GeV]",  "bin":100,"xmin":0 ,"xmax":50},
    "RecoMuon_pz":       {"name":"RecoMuon_pz",       "title":"Reco muon p_{z} [GeV]",  "bin":100,"xmin":0 ,"xmax":50},
    "RecoMuon_eta":      {"name":"RecoMuon_eta",      "title":"Reco muon #eta",         "bin":60, "xmin":-3,"xmax":3},
    "RecoMuon_theta":    {"name":"RecoMuon_theta",    "title":"Reco muon #theta",       "bin":64, "xmin":0,"xmax":3.2},
    "RecoMuon_phi":      {"name":"RecoMuon_phi",      "title":"Reco muon #phi",         "bin":64, "xmin":-3.2,"xmax":3.2},
    "RecoMuon_charge":   {"name":"RecoMuon_charge",   "title":"Reco muon charge",       "bin":3, "xmin":-1.5,"xmax":1.5},

    "RecoMuonTrack_absD0":             {"name":"RecoMuonTrack_absD0",     "title":"Reco muon tracks |d_{0}| [mm]",      "bin":100,"xmin":0, "xmax":2000},
    "RecoMuonTrack_absD0_prompt":      {"name":"RecoMuonTrack_absD0",     "title":"Reco muon tracks |d_{0}| [mm]",      "bin":100,"xmin":0, "xmax":1},
    "RecoMuonTrack_absZ0":             {"name":"RecoMuonTrack_absZ0",     "title":"Reco muon tracks |z_{0}| [mm]",      "bin":100,"xmin":0, "xmax":2000},
    "RecoMuonTrack_absZ0_prompt":      {"name":"RecoMuonTrack_absZ0",     "title":"Reco muon tracks |z_{0}| [mm]",      "bin":100,"xmin":0, "xmax":1},
    "RecoMuonTrack_absD0sig":          {"name":"RecoMuonTrack_absD0sig",  "title":"Reco muon tracks |d_{0} significance|",      "bin":100,"xmin":0, "xmax":600000},
    "RecoMuonTrack_absD0sig_prompt":   {"name":"RecoMuonTrack_absD0sig",  "title":"Reco muon tracks |d_{0} significance|",      "bin":100,"xmin":0, "xmax":5},
    "RecoMuonTrack_absZ0sig":          {"name":"RecoMuonTrack_absZ0sig",  "title":"Reco muon tracks |z_{0} significance|",      "bin":100,"xmin":0, "xmax":600000},
    "RecoMuonTrack_absZ0sig_prompt":   {"name":"RecoMuonTrack_absZ0sig",  "title":"Reco muon tracks |z_{0} significance|",      "bin":100,"xmin":0, "xmax":5},
    "RecoMuonTrack_D0cov":      {"name":"RecoMuonTrack_D0cov",     "title":"Reco muon tracks d_{0} #sigma^{2}",      "bin":100,"xmin":0, "xmax":0.5},
    "RecoMuonTrack_Z0cov":      {"name":"RecoMuonTrack_Z0cov",     "title":"Reco muon tracks z_{0} #sigma^{2}",      "bin":100,"xmin":0, "xmax":0.5},

    "RecoMissingEnergy_e":       {"name":"RecoMissingEnergy_e",       "title":"Reco Total Missing Energy [GeV]",    "bin":100,"xmin":0 ,"xmax":50},
    "RecoMissingEnergy_p":       {"name":"RecoMissingEnergy_p",       "title":"Reco Total Missing p [GeV]",         "bin":100,"xmin":0 ,"xmax":50},
    "RecoMissingEnergy_pt":      {"name":"RecoMissingEnergy_pt",      "title":"Reco Missing p_{T} [GeV]",           "bin":100,"xmin":0 ,"xmax":50},
    "RecoMissingEnergy_px":      {"name":"RecoMissingEnergy_px",      "title":"Reco Missing p_{x} [GeV]",           "bin":100,"xmin":0 ,"xmax":50},
    "RecoMissingEnergy_py":      {"name":"RecoMissingEnergy_py",      "title":"Reco Missing p_{y} [GeV]",           "bin":100,"xmin":0 ,"xmax":50},
    "RecoMissingEnergy_pz":      {"name":"RecoMissingEnergy_pz",      "title":"Reco Missing p_{z} [GeV]",           "bin":100,"xmin":0 ,"xmax":50},
    "RecoMissingEnergy_eta":     {"name":"RecoMissingEnergy_eta",     "title":"Reco Missing Energy #eta",           "bin":60,"xmin":-3 ,"xmax":3},
    "RecoMissingEnergy_theta":   {"name":"RecoMissingEnergy_theta",   "title":"Reco Missing Energy #theta",         "bin":64,"xmin":0 , "xmax":3.2},
    "RecoMissingEnergy_phi":     {"name":"RecoMissingEnergy_phi",     "title":"Reco Missing Energy #phi",           "bin":64,"xmin":-3.2 ,"xmax":3.2},

}
