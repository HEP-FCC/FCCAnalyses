import ROOT as r
r.gROOT.ProcessLine('.L /afs/cern.ch/user/r/rasmith/fcc/heppy/FCChhAnalyses/Zprime_tt/BDT_pp_Zprime_10TeV_ttbar_BDT_nosel_8Var.class.C+')
'''
varlist=["Jet1_tau32", "Jet2_tau32", "Jet1_tau21", "Jet2_tau21", "softDroppedJet1_m", "softDroppedJet2_m", "Jet1_softDroppedProngMaxPtRatio", "Jet1_softDroppedProngMinPtRatio", "Jet2_softDroppedProngMaxPtRatio", "Jet2_softDroppedProngMinPtRatio", "Jet1_trimmedProngMaxPtRatio", "Jet1_trimmedProngMinPtRatio", "Jet2_trimmedProngMaxPtRatio", "Jet2_trimmedProngMinPtRatio", "Jet1_prunedProngMaxPtRatio", "Jet1_prunedProngMinPtRatio", "Jet2_prunedProngMaxPtRatio", "Jet2_prunedProngMinPtRatio"]

inputs = r.vector('string')()
for v in varlist:
    inputs.push_back(v)

mva = r.ReadBDT_nosel_8Var(inputs)

values = r.vector('double')()
input_file = r.TFile.Open('/eos/user/r/rasmith/fcc_v01/Zprime_tt/hadronic/pp_tt_PT_10000_12000/heppy.FCChhAnalyses.Zprime_tt.TreeProducer.TreeProducer_1/tree.root')
input_tree = input_file.Get('events')
for i in xrange(input_tree.GetEntries()):
    input_tree.GetEntry(i)
    for v in varlist:
        values.push_back(getattr(input_tree,v))

    mva_value=mva.GetMvaValue(values)
    print '===================   ',mva_value

    values.clear()
'''



