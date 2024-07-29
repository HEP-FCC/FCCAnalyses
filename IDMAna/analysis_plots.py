import ROOT

# global parameters
intLumi        = 5.0e+06 #in pb-1
ana_tex        = 'e^{+}e^{-} #rightarrow l^{+}l^{-} + H + H'
delphesVersion = '3.4.2'
energy         = 240.0
collider       = 'FCC-ee'
inputDir       = 'iDM/final/'
formats        = ['png','pdf']
yaxis          = ['lin','log']
stacksig       = ['nostack']
outdir         = 'iDM/plots/'
plotStatUnc    = True

###If scaleSig=0 or scaleBack=0, we don't apply any additional scaling, on top of the normalization to cross section and integrated luminosity, as defined in finalSel.py
###If scaleSig or scaleBack is not defined, plots will be normalized to 1
scaleSig       = 1.
#scaleBack      = 0.
#splitLeg       = True

variables = ['n_seljets','n_photons',
             'mZ','mZzoom','ptZ','mZrecoil',
             'photon1_pt','photon1_eta','photon1_e',
             'lep1_pt','lep1_eta','lep1_e','lep1_charge',
             'lep2_pt','lep2_eta','lep2_e','lep2_charge',
             'lep_chargeprod',
             'jet1_pt','jet1_eta','jet1_e',
             'MET_e','MET_pt',
             'pZ','pzZ','eZ','povereZ','costhetaZ',
             'cosDphiLep','cosThetaStar','cosThetaR',
             'bdt_output'
]

rebin = [1,1,
         1,1,1,1,
         1,1,1,
         1,1,1,1,
         1,1,1,1,
         1,
         1,1,1,
         1,1,
         1,1,1,1,1,
         1,1,1,
         1
]# uniform rebin per variable (optional)

###Dictonnary with the analysis name as a key, and the list of selections to be plotted for this analysis. The name of the selections should be the same than in the final selection
selections = {}
selections['Zee']   = ["TwoEle","TwoEleVetoObj","TwoEleLepCuts",
    "TwoElePoverE"]
selections['Zmumu']   = ["TwoMu","TwoMuVetoObj","TwoMuLepCuts",
    "TwoMuPoverE"]

extralabel = {}
extralabel['TwoEle'] = "Selection: N_{e} = 2, |p_{z}^{ee}|<70 GeV, M_{ee}<120 GeV, MET p_{T}>5 GeV"
extralabel['TwoEleVetoObj'] = "Selection: N_{e} = 2, N_{jet}<1, no other lep or #gamma"
extralabel['TwoEleLepCuts'] = "Selection: N_{e} = 2, p^{e}_{T}<80,60 GeV"
extralabel['TwoElePoverE'] = "Selection: N_{e} = 2, p(ee)/E(ee)>0.1"
extralabel['TwoMu'] = "Selection: N_{#mu} = 2,  |p_{z}^{#mu#mu}|<70 GeV, M_{#mu#mu}<120 GeV, MET p_{T}>5 GeV"
extralabel['TwoMuVetoObj'] = "Selection: N_{#mu} = 2, N_{jet}<1, no other lep or #gamma"
extralabel['TwoMuLepCuts'] = "Selection: N_{#mu} = 2, p^{#mu}_{T}<80,60 GeV"
extralabel['TwoMuPoverE'] = "Selection: N_{#mu} = 2, p(#mu#mu)/E(#mu#mu)>0.1"


colors = {}
colors['nunuH'] = ROOT.kRed
colors['llH'] = ROOT.kRed+2
colors['mumuH'] = ROOT.kRed+4
colors['tautauH'] = ROOT.kRed-2
colors['qqH'] = ROOT.kRed-4
colors['eem30'] = ROOT.kViolet
colors['tautau'] = ROOT.kViolet-1
colors['mumu'] = ROOT.kViolet+1
colors['WW'] = ROOT.kBlue+1
colors['ZZ'] = ROOT.kGreen+2
colors['iDM1'] = ROOT.kBlack
colors['iDM2'] = ROOT.kGray+1
colors['iDM6'] = ROOT.kGray-1

plots = {}
plots['Zee'] = {
    'signal':{
        'iDM1':['e240_bp1_h2h2ll','e240_bp1_h2h2llvv'],
        'iDM2':['e240_bp2_h2h2ll','e240_bp2_h2h2llvv'],
        'iDM6':['e240_bp6_h2h2ll','e240_bp6_h2h2llvv'],
    },
    'backgrounds':{
        'eem30':['wzp6_ee_ee_Mee_30_150_ecm240'],
        'mumu':['wzp6_ee_mumu_ecm240'],
        'tautau':['wzp6_ee_tautau_ecm240'],
        'WW':['p8_ee_WW_ecm240'],
        'ZZ':['p8_ee_ZZ_ecm240'],
        'llH':['wzp6_ee_eeH_ecm240','wzp6_ee_mumuH_ecm240','wzp6_ee_tautauH_ecm240'],
        #'mumuH':['wzp6_ee_mumuH_ecm240'],
        #'tautauH':['wzp6_ee_tautauH_ecm240'],
        'qqH':['wzp6_ee_qqH_ecm240'],
        'nunuH':['wzp6_ee_nunuH_ecm240'],
    }
}
plots['Zmumu'] = plots['Zee']

legend = {}
legend['nunuH'] = '#nu#nuH'
legend['llH'] = 'llH'
legend['mumuH'] = '#mu#muH'
legend['tautauH'] = '#tau#tauH'
legend['qqH'] = 'qqH'
legend['eem30'] = 'ee30-150GeV'
legend['mumu'] = '#mu#mu'
legend['tautau'] = '#tau#tau'
legend['WW'] = 'WW'
legend['ZZ'] = 'ZZ'
legend['iDM1'] = 'iDM BP1'
legend['iDM2'] = 'iDM BP2'
legend['iDM6'] = 'iDM BP6'
