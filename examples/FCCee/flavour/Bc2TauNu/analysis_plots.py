import ROOT

# global parameters
intLumi        = 150000000. #in pb-1
ana_tex        = "Z #rightarrow q#bar{q}"
delphesVersion = "3.4.2"
energy         = 91.0
collider       = "FCC-ee"
inputDir       = "/eos/experiment/fcc/ee/analyses/case-studies/flavour/Bc2TauNu/flatNtuples/spring2021/prod_04/analysis_final/"
formats        = ['png','pdf']
yaxis          = ['lin','log']
stacksig       = ['nostack']
outdir         = '/eos/home-h/helsens/www/FCC/ee/flavour/Bc2TauNu/spring2021/prod_04/plots/'
variables = [ "EVT_CandMass",
              "EVT_ThrustEmin_E","EVT_ThrustEmax_E",
              "EVT_ThrustEmin_Echarged", "EVT_ThrustEmax_Echarged",
              "EVT_ThrustEmin_Eneutral", "EVT_ThrustEmax_Eneutral",
              "EVT_ThrustEmin_Ncharged", "EVT_ThrustEmax_Ncharged",
              "EVT_ThrustEmin_Nneutral", "EVT_ThrustEmax_Nneutral",
              "EVT_ThrustEmin_NDV",      "EVT_ThrustEmax_NDV",
              "EVT_ThrustDiff_E",              "EVT_ThrustDiff_N",

              "EVT_ThrustDiff_Echarged","EVT_ThrustDiff_Eneutral",
              "EVT_ThrustDiff_Ncharged","EVT_ThrustDiff_Nneutral",
              "EVT_CandVtxFD",
              "EVT_CandAngleThrust",
              "EVT_CandAngleThrust_2",
              "EVT_MVA1","EVT_MVA2",

              "EVT_Nominal_B_E",
              "EVT_PVmass",
              "EVT_DVmass_min",
              "EVT_DVmass_max",
              "EVT_DVmass_ave",
              "EVT_DVd0_min",
              "EVT_DVd0_max",
              "EVT_DVd0_ave",
              "EVT_DVz0_min",
              "EVT_DVz0_max",
              "EVT_DVz0_ave",


              ]

scaleSig=1.
###Dictonnary with the analysis name as a key, and the list of selections to be plotted for this analysis. The name of the selections should be the same than in the final selection
selections = {}
selections['Inclusive']       = ["sel1","sel2","sel3","sel4"]
selections['ExclusiveMerged'] = ["sel1","sel2","sel3","sel4"]

selections['Inclusive']       = ["sel5"]
selections['InclusiveEvtGen'] = ["sel5"]
selections['ExclusiveMerged'] = ["sel5"]

extralabel = {}
extralabel['sel0'] = "Selection: MVA1>0.8, MVA2>0.8"
extralabel['sel1'] = "Selection: MVA1>0.9, MVA2>0.9"
extralabel['sel2'] = "Selection: MVA1>0.95, MVA2>0.95"
extralabel['sel3'] = "Selection: MVA1>0.98, MVA2>0.98"
extralabel['sel4'] = "Selection: MVA1>0.99, MVA2>0.99"
extralabel['sel5'] = "Selection: Donal's cuts"

colors = {}
colors['Z_Bc']    = ROOT.kRed
colors['Z_bb']    = ROOT.kBlue
colors['Z_bb_EvtGen'] = ROOT.kBlue
colors['Z_bb_B']  = ROOT.kBlue
colors['Z_bb_Bu'] = ROOT.kBlue+1
colors['Z_bb_Bd'] = ROOT.kBlue+2
colors['Z_bb_Bs'] = ROOT.kBlue+3
colors['Z_bb_Lb'] = ROOT.kBlue+4
colors['Z_cc']    = ROOT.kGreen+1
colors['Z_uds']   = ROOT.kGreen+2
colors['Z_Bu']    = ROOT.kGreen+3

plots = {}
plots['Inclusive'] = {'signal':{'Z_Bc':['p8_ee_Zbb_ecm91_EvtGen_Bc2TauNuTAUHADNU']},
                      'backgrounds':{'Z_bb':['p8_ee_Zbb_ecm91'],
                                     'Z_cc':['p8_ee_Zcc_ecm91'],
                                     'Z_uds':['p8_ee_Zuds_ecm91'],
                                     'Z_Bu':['p8_ee_Zbb_ecm91_EvtGen_Bu2TauNuTAUHADNU']
                                     }
                      }

plots['InclusiveEvtGen'] = {'signal':{'Z_Bc':['p8_ee_Zbb_ecm91_EvtGen_Bc2TauNuTAUHADNU']},
                            'backgrounds':{'Z_bb_EvtGen':['p8_ee_Zbb_ecm91_EvtGen'],
                                           'Z_cc':['p8_ee_Zcc_ecm91'],
                                           'Z_uds':['p8_ee_Zuds_ecm91'],
                                           'Z_Bu':['p8_ee_Zbb_ecm91_EvtGen_Bu2TauNuTAUHADNU']
                                     }
                      }


plots['ExclusiveMerged'] = {'signal':{'Z_Bc':['p8_ee_Zbb_ecm91_EvtGen_Bc2TauNuTAUHADNU']},
                            'backgrounds':{'Z_bb_B':['p8_ee_Zbb_ecm91_EvtGen_Bd2D3Pi',
                                                     'p8_ee_Zbb_ecm91_EvtGen_Bd2DDs',
                                                     'p8_ee_Zbb_ecm91_EvtGen_Bd2DTauNu',
                                                     'p8_ee_Zbb_ecm91_EvtGen_Bd2Dst3Pi',
                                                     'p8_ee_Zbb_ecm91_EvtGen_Bd2DstDs',
                                                     'p8_ee_Zbb_ecm91_EvtGen_Bd2DstDsst',
                                                     'p8_ee_Zbb_ecm91_EvtGen_Bd2DstTauNu',

                                                     'p8_ee_Zbb_ecm91_EvtGen_Bs2Ds3Pi',
                                                     'p8_ee_Zbb_ecm91_EvtGen_Bs2DsDs',
                                                     'p8_ee_Zbb_ecm91_EvtGen_Bs2DsTauNu',
                                                     'p8_ee_Zbb_ecm91_EvtGen_Bs2Dsst3Pi',
                                                     'p8_ee_Zbb_ecm91_EvtGen_Bs2DsstDs',
                                                     'p8_ee_Zbb_ecm91_EvtGen_Bs2DsstDsst',
                                                     'p8_ee_Zbb_ecm91_EvtGen_Bs2DsstTauNu',

                                                     'p8_ee_Zbb_ecm91_EvtGen_Bu2D03Pi',
                                                     'p8_ee_Zbb_ecm91_EvtGen_Bu2D0Ds',
                                                     'p8_ee_Zbb_ecm91_EvtGen_Bu2D0TauNu',
                                                     'p8_ee_Zbb_ecm91_EvtGen_Bu2Dst03Pi',
                                                     'p8_ee_Zbb_ecm91_EvtGen_Bu2Dst0Ds',
                                                     'p8_ee_Zbb_ecm91_EvtGen_Bu2Dst0Dsst',
                                                     'p8_ee_Zbb_ecm91_EvtGen_Bu2Dst0TauNu',

                                                     'p8_ee_Zbb_ecm91_EvtGen_Lb2Lc3Pi',
                                                     'p8_ee_Zbb_ecm91_EvtGen_Lb2LcDs',
                                                     'p8_ee_Zbb_ecm91_EvtGen_Lb2LcTauNu',
                                                     'p8_ee_Zbb_ecm91_EvtGen_Lb2Lcst3Pi',
                                                     'p8_ee_Zbb_ecm91_EvtGen_Lb2LcstDs',
                                                     'p8_ee_Zbb_ecm91_EvtGen_Lb2LcstDsst',
                                                     'p8_ee_Zbb_ecm91_EvtGen_Lb2LcstTauNu',
                                                    ],
                                           'Z_cc':['p8_ee_Zcc_ecm91'],
                                           'Z_uds':['p8_ee_Zuds_ecm91'],
                                           'Z_Bu':['p8_ee_Zbb_ecm91_EvtGen_Bu2TauNuTAUHADNU']
                                          }
                           }

legend = {}
legend['Z_Bc']    = 'B_{c}#rightarrow #tau#nu (#tau#rightarrow 3#pi)'
legend['Z_bb']    = 'Z#rightarrow b#bar{b}'
legend['Z_bb_EvtGen']    = 'Z#rightarrow b#bar{b} EvtGen'
legend['Z_bb_B']  = 'Z#rightarrow b#bar{b} B_{u}+B_{d}+B_{s}+L_{b}'
legend['Z_cc']    = 'Z#rightarrow c#bar{c}'
legend['Z_uds']   = 'Z#rightarrow q#bar{q}'
legend['Z_Bu']    = 'B_{u}#rightarrow #tau#nu (#tau#rightarrow 3#pi)'
