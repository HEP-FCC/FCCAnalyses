import os
import copy
import heppy.framework.config as cfg
import logging
import imp
# next 2 lines necessary to deal with reimports from ipython
logging.shutdown()
reload(logging)
logging.basicConfig(level=logging.WARNING)

sample=imp.load_source('heppylist', '/afs/cern.ch/work/h/helsens/public/FCCDicts/FCC_heppySampleList_fcc_v02.py')

comp = cfg.Component(
    'example',
     files = ["/eos/experiment/fcc/hh/generation/DelphesEvents/fcc_v02/mgp8_pp_tttt_5f//events_000000004.root"]
)

selectedComponents = [
                        sample.mgp8_pp_tttt_5f,
                        sample.mgp8_pp_bbbbj_QCD,
                        sample.mgp8_pp_ttz_5f_zbb,
                        sample.mgp8_pp_ttbb_4f,
                        sample.mgp8_pp_tth01j_5f_hbb,
                        sample.mgp8_pp_ttzz_5f,
                        sample.mgp8_pp_ttww_4f,
                        sample.mgp8_pp_ttwz_5f,
                     ]

## short list from fcc_v02
#mgp8_pp_tttt_5f                   1,450,000
#------------
#------------
#mgp8_pp_tv012j_5f                   100,000
#------------
#mgp8_pp_ttw_5f                    3,720,000
#mgp8_pp_ttv01j_5f                 1,107,948
#------------
#mgp8_pp_ttz_5f_zbb               38,710,000
#mgp8_pp_ttz_5f                    3,750,000
#mgp8_pp_ttz01j_5f_HT_1100_2700    1,802,063
#mgp8_pp_ttz01j_5f_HT_2700_4900    1,876,797
#mgp8_pp_ttz01j_5f_HT_4900_8100    1,923,311
#mgp8_pp_ttz01j_5f_HT_8100_100000    677,540 
#------------
#mgp8_pp_bbbbj_QCD                14,010,000 ??
#------------
#mgp8_pp_tt012j_5f                15,253,535
#mgp8_pp_ttbb_4f                  23,239,639
#mgp8_pp_ttj_4f                   38,500,000
#------------
#mgp8_pp_tth01j_5f_hbb            32,486,572
#------------
#mgp8_pp_ttzz_5f                   1,430,000
#mgp8_pp_ttww_4f                     570,000
#mgp8_pp_ttwz_5f                     500,000

sample.mgp8_pp_tttt_5f.splitFactor       = 15
sample.mgp8_pp_bbbbj_QCD.splitFactor     = 140
sample.mgp8_pp_ttz_5f_zbb.splitFactor    = 390
sample.mgp8_pp_ttbb_4f.splitFactor       = 230
sample.mgp8_pp_tth01j_5f_hbb.splitFactor = 320
sample.mgp8_pp_ttzz_5f.splitFactor       = 14
sample.mgp8_pp_ttww_4f.splitFactor       = 6
sample.mgp8_pp_ttwz_5f.splitFactor       = 5

selectedComponents = [comp]




from heppy.FCChhAnalyses.analyzers.Reader import Reader
source = cfg.Analyzer(
    Reader,

    weights = 'mcEventWeights',
    gen_particles = 'skimmedGenParticles',
    met = 'met',   

    electrons = 'electrons',
    muons = 'muons',

    #main jets trk08
    trkjets08  = 'trkjets08',
    trkbTags08 = 'trkbTags08',

    trkjetsOneSubJettiness08    = 'trkjetsOneSubJettiness08',
    trkjetsTwoSubJettiness08    = 'trkjetsTwoSubJettiness08',
    trkjetsThreeSubJettiness08  = 'trkjetsThreeSubJettiness08',
    trksubjetsSoftDropTagged08  = 'trksubjetsSoftDropTagged08',
    trksubjetsSoftDrop08        = 'trksubjetsSoftDrop08',
  
    #pf jets pf08 for correction
    pfjets08  = 'pfjets08',
    pfbTags08 = 'pfbTags08',

    pfjetsOneSubJettiness08    = 'pfjetsOneSubJettiness08',
    pfjetsTwoSubJettiness08    = 'pfjetsTwoSubJettiness08',
    pfjetsThreeSubJettiness08  = 'pfjetsThreeSubJettiness08',
    pfsubjetsSoftDropTagged08  = 'pfsubjetsSoftDropTagged08',
    pfsubjetsSoftDrop08        = 'pfsubjetsSoftDrop08',


    # used for b-tagging
    pfjets04  = 'pfjets04',
    pfbTags04 = 'pfbTags04',
    pfjetsFlavor04  = 'pfjetsFlavor04',

)


from ROOT import gSystem
gSystem.Load("libdatamodelDict")
from EventStore import EventStore as Events

#############################
##   Reco Level Analysis   ##
#############################

#uncomment the following to go back to normal

from heppy.analyzers.Selector import Selector
# select pf08 jets above 30 GeV
jets_pf08_30 = cfg.Analyzer(
    Selector,
    'jets_pf08_30',
    output = 'jets_pf08_30',
    input_objects = 'pfjets08',
    filter_func = lambda fatjet: fatjet.pt()>30.
)

jets_trk08_20 = cfg.Analyzer(
    Selector,
    'jets_trk08_20',
    output = 'jets_trk08_20',
    input_objects = 'trkjets08',
    filter_func = lambda jet: jet.pt()>20
)

# select pf04 jets above 20 GeV for direct b-tagging
jets_pf04_20 = cfg.Analyzer(
    Selector,
    'jets_pf04_20',
    output = 'jets_pf04_20',
    input_objects = 'pfjets04',
    filter_func = lambda jet: jet.pt()>20
)

# apply jet flavour tagging
from heppy.FCChhAnalyses.analyzers.FlavourTagger import FlavourTagger
jets_pf04_20_pdg = cfg.Analyzer(
    FlavourTagger,
    'jets_pf04_20_pdg',
    input_jets = 'jets_pf04_20',
    input_genparticles = 'gen_particles',
    output_jets = 'jets_pf04_20_pdg',
    dr_match = 0.4,
    pdg_tags = [5, 4, 0],
    ptr_min = 0.1,
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
from heppy.FCChhAnalyses.FCChh.tttt.TreeProducer import TreeProducer
tree = cfg.Analyzer(
    TreeProducer,
    jets_trk08_20 = 'jets_trk08_20',
    jets_pf04_20  = 'jets_pf04_20',
    jets_pf08_30  = 'jets_pf08_30',

    electrons = 'electrons_100',
    muons = 'muons_100',

)


# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence( [
    source,
    jets_pf08_30,
    jets_pf04_20,
    jets_pf04_20_pdg,

    jets_trk08_20,

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
