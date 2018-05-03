import os, sys
import copy
import heppy.framework.config as cfg

import logging
# next 2 lines necessary to deal with reimports from ipython
logging.shutdown()
reload(logging)
logging.basicConfig(level=logging.WARNING)

sys.path.append('/afs/cern.ch/work/h/helsens/public/FCCDicts/')

comp = cfg.Component(
    'example',
     files = ["/eos/experiment/fcc/hh/generation/DelphesEvents/fcc_v02/mgp8_pp_h012j_5f_hlla/events_000001296.root"]
)

from FCC_heppySampleList_fcc_v02 import *

selectedComponents = [
                      mgp8_pp_h012j_5f_hlla,
                      mgp8_pp_tth01j_5f_hlla,
                      mgp8_pp_vbf_h01j_5f_hlla,
                      mgp8_pp_vh012j_5f_hlla,
                      #mgp8_pp_lla01j_mhcut_5f
                      mgp8_pp_lla01j_mhcut_5f_HT_0_100,
                      mgp8_pp_lla01j_mhcut_5f_HT_100_300, 
                      mgp8_pp_lla01j_mhcut_5f_HT_300_500, 
                      mgp8_pp_lla01j_mhcut_5f_HT_500_100000,
                      mgp8_pp_lla01j_mhcut_5f_HT_300_100000,
                      ]

mgp8_pp_h012j_5f_hlla.splitFactor = 50
mgp8_pp_vbf_h01j_5f_hlla.splitFactor = 50
mgp8_pp_tth01j_5f_hlla.splitFactor = 50
mgp8_pp_vh012j_5f_hlla.splitFactor = 50
#mgp8_pp_lla01j_mhcut_5f.splitFactor = 50
mgp8_pp_lla01j_mhcut_5f_HT_0_100.splitFactor = 4
mgp8_pp_lla01j_mhcut_5f_HT_100_300.splitFactor = 4
mgp8_pp_lla01j_mhcut_5f_HT_300_500.splitFactor = 2 
mgp8_pp_lla01j_mhcut_5f_HT_500_100000.splitFactor = 2
mgp8_pp_lla01j_mhcut_5f_HT_300_100000.splitFactor = 2


#selectedComponents = [comp]


from heppy.FCChhAnalyses.analyzers.Reader import Reader
source = cfg.Analyzer(
    Reader,

    weights = 'mcEventWeights',

    gen_particles = 'skimmedGenParticles',

    electrons = 'electrons',
    electronITags = 'electronITags',
    electronsToMC = 'electronsToMC',

    muons = 'muons',
    muonITags = 'muonITags',
    muonsToMC = 'muonsToMC',

    jets = 'pfjets04',
    bTags = 'pfbTags04',

    photons = 'photons',
    
    pfphotons = 'pfphotons',
    pfcharged = 'pfcharged',
    pfneutrals = 'pfneutrals',

    met = 'met',

)

from ROOT import gSystem
gSystem.Load("libdatamodelDict")
from EventStore import EventStore as Events


#############################
##   Reco Level Analysis   ##
#############################


# select isolated muons with pT > 5 GeV and relIso < 0.4
from heppy.analyzers.Selector import Selector
selected_muons = cfg.Analyzer(
    Selector,
    'selected_muons',
    output = 'selected_muons',
    input_objects = 'muons',
    filter_func = lambda ptc: ptc.pt()>10 and ptc.iso.sumpt/ptc.pt()<0.15
)

# select electrons with pT > 7 GeV and relIso < 0.4
selected_electrons = cfg.Analyzer(
    Selector,
    'selected_electrons',
    output = 'selected_electrons',
    input_objects = 'electrons',
    filter_func = lambda ptc: ptc.pt()>10 and ptc.iso.sumpt/ptc.pt()<0.15
)

# select isolated photons with pT > 35 GeV and relIso < 0.4
from heppy.analyzers.Selector import Selector
selected_photons = cfg.Analyzer(
    Selector,
    'selected_photons',
    output = 'selected_photons',
    input_objects = 'photons',
    filter_func = lambda ptc: ptc.pt()> 15. and ptc.iso.sumpt/ptc.pt()<0.15
)

# merge electrons and muons into a single lepton collection
from heppy.analyzers.Merger import Merger
selected_leptons = cfg.Analyzer(
      Merger,
      instance_label = 'selected_leptons', 
      inputs = ['selected_electrons','selected_muons'],
      output = 'selected_leptons'
)

# create Z boson candidates with leptons
from heppy.analyzers.LeptonicZedBuilder import LeptonicZedBuilder
zeds = cfg.Analyzer(
      LeptonicZedBuilder,
      output = 'zeds',
      leptons = 'selected_leptons',
)


# store interesting quantities into flat ROOT tree
from heppy.FCChhAnalyses.FCChh.hza.TreeProducer import TreeProducer
reco_tree = cfg.Analyzer(
    TreeProducer,
    zeds = 'zeds',
    photons = 'selected_photons',
)

# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence( [
    source,
    selected_muons,
    selected_electrons,
    selected_leptons,
    selected_photons,
    zeds,
    reco_tree,
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
