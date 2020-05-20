import os
import copy
import heppy.framework.config as cfg
import logging
import imp
# next 2 lines necessary to deal with reimports from ipython
logging.shutdown()
reload(logging)
logging.basicConfig(level=logging.WARNING)

sample=imp.load_source('heppylist', '/afs/cern.ch/work/h/helsens/public/FCCDicts/HELHC_heppySampleList_helhc_v01.py')

comp = cfg.Component(
    'example',
     files = ["/eos/experiment/fcc/helhc/generation/DelphesEvents/helhc_v01/mgp8_pp_tt_5f_HT_5000_10000/events_089436160.root"]
#     files = ["/eos/experiment/fcc/helhc/generation/DelphesEvents/helhc_v01/mgp8_pp_jj_5f_HT_2000_5000/events_163309325.root"]
#     files = ["/eos/experiment/fcc/helhc/generation/DelphesEvents/helhc_v01/mgp8_pp_tj_5f//events_048843027.root"]
#     files = ["/eos/experiment/fcc/helhc/generation/DelphesEvents/helhc_v01/mgp8_pp_tvj_5f//events_085461659.root"]
)

selectedComponents = [
                        sample.mgp8_pp_jj_5f_HT_500_1000,
                        sample.mgp8_pp_jj_5f_HT_1000_2000,
                        sample.mgp8_pp_jj_5f_HT_2000_5000,
                        sample.mgp8_pp_jj_5f_HT_5000_10000,
                        sample.mgp8_pp_jj_5f_HT_10000_27000,
                        sample.mgp8_pp_tt_5f_HT_500_1000,
                        sample.mgp8_pp_tt_5f_HT_1000_2000,
                        sample.mgp8_pp_tt_5f_HT_2000_5000,
                        sample.mgp8_pp_tt_5f_HT_5000_10000,
                        sample.mgp8_pp_tt_5f_HT_10000_27000,
                        sample.mgp8_pp_vv_5f_HT_500_1000,
                        sample.mgp8_pp_vv_5f_HT_1000_2000,
                        sample.mgp8_pp_vv_5f_HT_2000_5000,
                        sample.mgp8_pp_vv_5f_HT_5000_10000,
                        sample.mgp8_pp_vv_5f_HT_10000_27000,
                        sample.mgp8_pp_vj_5f_HT_500_1000,
                        sample.mgp8_pp_vj_5f_HT_1000_2000,
                        sample.mgp8_pp_vj_5f_HT_2000_5000,
                        sample.mgp8_pp_vj_5f_HT_5000_10000,
                        sample.mgp8_pp_vj_5f_HT_10000_27000,
                        sample.mgp8_pp_tj_5f,
                        sample.mgp8_pp_tvj_5f,
                     ]


splitFac = 40
sample.mgp8_pp_tj_5f.splitFactor  = splitFac
sample.mgp8_pp_tvj_5f.splitFactor = splitFac

splitFac2 = 60
sample.mgp8_pp_jj_5f_HT_500_1000.splitFactor    = splitFac2
sample.mgp8_pp_jj_5f_HT_1000_2000.splitFactor   = splitFac2
sample.mgp8_pp_jj_5f_HT_2000_5000.splitFactor   = splitFac2
sample.mgp8_pp_jj_5f_HT_5000_10000.splitFactor  = splitFac2
sample.mgp8_pp_jj_5f_HT_10000_27000.splitFactor = splitFac2
sample.mgp8_pp_tt_5f_HT_500_1000.splitFactor    = splitFac2
sample.mgp8_pp_tt_5f_HT_1000_2000.splitFactor   = splitFac2
sample.mgp8_pp_tt_5f_HT_2000_5000.splitFactor   = splitFac2
sample.mgp8_pp_tt_5f_HT_5000_10000.splitFactor  = splitFac2
sample.mgp8_pp_tt_5f_HT_10000_27000.splitFactor = splitFac2
sample.mgp8_pp_vv_5f_HT_500_1000.splitFactor    = splitFac2
sample.mgp8_pp_vv_5f_HT_1000_2000.splitFactor   = splitFac2
sample.mgp8_pp_vv_5f_HT_2000_5000.splitFactor   = splitFac2
sample.mgp8_pp_vv_5f_HT_5000_10000.splitFactor  = splitFac2
sample.mgp8_pp_vv_5f_HT_10000_27000.splitFactor = splitFac2
sample.mgp8_pp_vj_5f_HT_500_1000.splitFactor    = splitFac2
sample.mgp8_pp_vj_5f_HT_1000_2000.splitFactor   = splitFac2
sample.mgp8_pp_vj_5f_HT_2000_5000.splitFactor   = splitFac2
sample.mgp8_pp_vj_5f_HT_5000_10000.splitFactor  = splitFac2
sample.mgp8_pp_vj_5f_HT_10000_27000.splitFactor = splitFac2

#selectedComponents = [comp]




from heppy.FCChhAnalyses.analyzers.Reader import Reader
source = cfg.Analyzer(
    Reader,

    weights = 'mcEventWeights',
    gen_particles = 'skimmedGenParticles',
    met = 'met',   

    electrons = 'electrons',
    muons = 'muons',

    #main jets trk02
    trkjets02  = 'trkjets02',
    trkbTags02 = 'trkbTags02',

    trkjetsOneSubJettiness02    = 'trkjetsOneSubJettiness02',
    trkjetsTwoSubJettiness02    = 'trkjetsTwoSubJettiness02',
    trkjetsThreeSubJettiness02  = 'trkjetsThreeSubJettiness02',
    trksubjetsSoftDropTagged02  = 'trksubjetsSoftDropTagged02',
    trksubjetsSoftDrop02        = 'trksubjetsSoftDrop02',
    #
    trksubjetsSoftDropTagged04  = 'trksubjetsSoftDropTagged04',
    trksubjetsSoftDrop04        = 'trksubjetsSoftDrop04',
    trksubjetsSoftDropTagged08  = 'trksubjetsSoftDropTagged08',
    trksubjetsSoftDrop08        = 'trksubjetsSoftDrop08',
  
    #pf jets pf02 for correction
    pfjets02  = 'pfjets02',
    pfbTags02 = 'pfbTags02',

    pfjetsOneSubJettiness02    = 'pfjetsOneSubJettiness02',
    pfjetsTwoSubJettiness02    = 'pfjetsTwoSubJettiness02',
    pfjetsThreeSubJettiness02  = 'pfjetsThreeSubJettiness02',
    pfsubjetsSoftDropTagged02  = 'pfsubjetsSoftDropTagged02',
    pfsubjetsSoftDrop02        = 'pfsubjetsSoftDrop02',


    # used for b-tagging
    pfjets04  = 'pfjets04',
    pfbTags04 = 'pfbTags04',
    pfjetsFlavor04  = 'pfjetsFlavor04',

    # used for mreco
    pfjets08  = 'pfjets08',
    pfbTags08 = 'pfbTags08',

    trkjets04  = 'trkjets04',
    trkjets08  = 'trkjets08',

)


from ROOT import gSystem
gSystem.Load("libdatamodelDict")
from EventStore import EventStore as Events

#############################
##   Reco Level Analysis   ##
#############################

# fix pf04 jets (get muon back in)
from heppy.FCChhAnalyses.analyzers.JetCorrector import JetCorrector
pfjets04_fix = cfg.Analyzer(
    JetCorrector,
    'pfjets04_fix',
    output = 'pfjets04_fix',
    input_jets = 'pfjets04',
    input_extra = 'muons',
    dr_match = 0.4,
)

from heppy.analyzers.Matcher import Matcher
lepton_jets = cfg.Analyzer(
    Matcher,
    'lepton_jets',
    delta_r = 0.2,
    match_particles = 'muons',
    particles = 'pfjets02'
)

from heppy.analyzers.Selector import Selector
# select pf02 jets above 2000 GeV
jets_pf02_1500 = cfg.Analyzer(
    Selector,
    'jets_pf02_1500',
    output = 'jets_pf02_1500',
    input_objects = 'pfjets02',
    filter_func = lambda fatjet: fatjet.pt()>500. and fatjet.match is None
)

jets_trk02_1000 = cfg.Analyzer(
    Selector,
    'jets_trk02_1000',
    output = 'jets_trk02_1000',
    input_objects = 'trkjets02',
    filter_func = lambda jet: jet.pt()>250
)

jets_trk04_1000 = cfg.Analyzer(
    Selector,
    'jets_trk04_1000',
    output = 'jets_trk04_1000',
    input_objects = 'trkjets04',
    filter_func = lambda jet: jet.pt()>250
)

jets_trk08_1000 = cfg.Analyzer(
    Selector,
    'jets_trk08_1000',
    output = 'jets_trk08_1000',
    input_objects = 'trkjets08',
    filter_func = lambda jet: jet.pt()>250
)

# select pf04 jets above 1000 GeV for b-tagging
jets_pf04_1000 = cfg.Analyzer(
    Selector,
    'jets_pf04_1000',
    output = 'jets_pf04_1000',
    input_objects = 'pfjets04_fix',
    filter_func = lambda jet: jet.pt()>250
)

# apply jet flavour tagging
from heppy.FCChhAnalyses.analyzers.FlavourTagger import FlavourTagger
jets_pf04_1000_pdg = cfg.Analyzer(
    FlavourTagger,
    'jets_pf04_1000_pdg',
    input_jets = 'jets_pf04_1000',
    input_genparticles = 'gen_particles',
    output_jets = 'jets_pf04_1000_pdg',
    dr_match = 0.4,
    pdg_tags = [5, 4, 0],
    ptr_min = 0.1,
)

# select pf04 jets above 1500 GeV for jet correction
# -> avoid rare crashes when pf04 jet is a little bit smaller than pf02
jets_pf04_1500 = cfg.Analyzer(
    Selector,
    'jets_pf04_1500',
    output = 'jets_pf04_1500',
    input_objects = 'pfjets04_fix',
    filter_func = lambda jet: jet.pt()>300
)

# select pf08 jets above 1500 GeV
jets_pf08_1500 = cfg.Analyzer(
    Selector,
    'jets_pf08_1500',
    output = 'jets_pf08_1500',
    input_objects = 'pfjets08',
    filter_func = lambda jet: jet.pt()>500
)

# select electrons above 100 GeV
electrons_100 = cfg.Analyzer(
    Selector,
    'electrons_100',
    output = 'electrons_100',
    input_objects = 'electrons',
    filter_func = lambda electron: electron.pt()>100.
)

# select muons above 100 GeV
muons_100 = cfg.Analyzer(
    Selector,
    'muons_100',
    output = 'muons_100',
    input_objects = 'muons',
    filter_func = lambda muon: muon.pt()>100.
)

# produce flat root tree containing jet substructure information
from heppy.FCChhAnalyses.HELHC.single_top.TreeProducer import TreeProducer
tree = cfg.Analyzer(
    TreeProducer,
    pfjets04_fix    = 'pfjets04_fix',

    jets_trk02_1000 = 'jets_trk02_1000',
    jets_trk04_1000 = 'jets_trk04_1000',
    jets_trk08_1000 = 'jets_trk08_1000',

    jets_pf02_1500  = 'jets_pf02_1500',
    jets_pf04_1000  = 'jets_pf04_1000',
    jets_pf04_1500  = 'jets_pf04_1500',
    jets_pf08_1500  = 'jets_pf08_1500',

    electrons = 'electrons_100',
    muons = 'muons_100',

)

# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence( [
    source,
    pfjets04_fix,
    lepton_jets,
    jets_pf02_1500,
    jets_pf04_1000,
    jets_pf04_1000_pdg,
    jets_pf04_1500,
    jets_pf08_1500,

    jets_trk02_1000,
    jets_trk04_1000,
    jets_trk08_1000,

    electrons_100,
    muons_100,
    tree,
    ] )

config = cfg.Config(
    components = selectedComponents,
    sequence = sequence,
    services = [],
    events_class = Events
)

if __name__ == '__main__':
    import sys
    from heppy.framework.looper import Looper

    def next():
        loop.process(loop.iEvent+1)

    loop = Looper( 'looper', config,
                   nEvents=100,
                   nPrint=0,
                   timeReport=True)
    loop.process(6)
    print loop.event
