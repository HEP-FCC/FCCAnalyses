import os
import copy
import heppy.framework.config as cfg
import sys
import logging
# next 2 lines necessary to deal with reimports from ipython
logging.shutdown()
reload(logging)
logging.basicConfig(level=logging.WARNING)
sys.path.append('/afs/cern.ch/work/h/helsens/public/FCCDicts/')

comp = cfg.Component(
    'example',
     files = ["/eos/experiment/fcc/helhc/generation/DelphesEvents/helhc_v01/p8_pp_Zprime_5TeV_ttbar/events_093536804.root"]
)

from heppySampleList_helhc_v01 import *

selectedComponents = [

    
                        p8_pp_Zprime_2TeV_ttbar,
                        p8_pp_Zprime_5TeV_ttbar,
                        p8_pp_Zprime_10TeV_ttbar,
                        mgp8_pp_tt_lo,
                     ]

p8_pp_Zprime_2TeV_ttbar.splitFactor = 10
p8_pp_Zprime_5TeV_ttbar.splitFactor = 10
p8_pp_Zprime_10TeV_ttbar.splitFactor = 10
mgp8_pp_tt_lo.splitFactor = 10

#selectedComponents = [comp]




from heppy.FCChhAnalyses.analyzers.Reader import Reader
source = cfg.Analyzer(
    Reader,

    weights = 'mcEventWeights',
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


    # used for mreco
    pfjets08  = 'pfjets08',
    pfbTags08 = 'pfbTags08',

)


from ROOT import gSystem
gSystem.Load("libdatamodelDict")
from EventStore import EventStore as Events

#############################
##   Reco Level Analysis   ##
#############################

#uncomment the following to go back to normal

from heppy.analyzers.Selector import Selector
# select pf02 jets above 2000 GeV
jets_pf02_1500 = cfg.Analyzer(
    Selector,
    'jets_pf02_1500',
    output = 'jets_pf02_1500',
    input_objects = 'pfjets02',
    filter_func = lambda fatjet: fatjet.pt()>1500.
)

jets_trk02_1000 = cfg.Analyzer(
    Selector,
    'jets_trk02_1000',
    output = 'jets_trk02_1000',
    input_objects = 'trkjets02',
    filter_func = lambda jet: jet.pt()>1000
)

# select pf04 jets above 1000 GeV for b-tagging
jets_pf04_1000 = cfg.Analyzer(
    Selector,
    'jets_pf04_1000',
    output = 'jets_pf04_1000',
    input_objects = 'pfjets04',
    filter_func = lambda jet: jet.pt()>1000
)

# select pf04 jets above 1000 GeV for b-tagging
jets_pf08_1500 = cfg.Analyzer(
    Selector,
    'jets_pf08_1500',
    output = 'jets_pf08_1500',
    input_objects = 'pfjets08',
    filter_func = lambda jet: jet.pt()>1500
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
from heppy.FCChhAnalyses.HELHC.Zprime_tt.TreeProducer import TreeProducer
tree = cfg.Analyzer(
    TreeProducer,
    jets_trk02_1000 = 'jets_trk02_1000',
    jets_pf02_1500  = 'jets_pf02_1500',
    jets_pf08_1500  = 'jets_pf08_1500',
    jets_pf04_1000  = 'jets_pf04_1000',
    electrons = 'electrons_100',
    muons = 'muons_100',

)


# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence( [
    source,
    jets_pf02_1500,
    jets_pf08_1500,
    jets_pf04_1000,
    jets_trk02_1000,
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
