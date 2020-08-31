import os, sys
import copy, math
import heppy.framework.config as cfg
import logging

# next 2 lines necessary to deal with reimports from ipython
logging.shutdown()
reload(logging)
logging.basicConfig(level=logging.WARNING)

sys.path.append('/afs/cern.ch/work/h/helsens/public/FCCDicts/')

comp = cfg.Component(
    'example',
     files = ["/eos/experiment/fcc/hh/generation/DelphesEvents/fcc_v02/mgp8_pp_h012j_5f_haa/events_000001373.root"]
)

from HELHC_heppySampleList_helhc_v01 import *

selectedComponents = [
                      mgp8_pp_h012j_5f_HT_0_27000_haa,
                      mgp8_pp_tth01j_5f_HT_0_27000_haa,
                      mgp8_pp_vbf_h01j_5f_HT_0_27000_haa,
                      mgp8_pp_vh012j_5f_HT_0_27000_haa,
                      mgp8_pp_aa012j_5f_HT_0_200,
		      mgp8_pp_aa012j_5f_HT_200_600,
		      mgp8_pp_aa012j_5f_HT_600_27000,
		      mgp8_gg_aa01j_5f_HT_0_200,
		      mgp8_gg_aa01j_5f_HT_200_600,
		      mgp8_gg_aa01j_5f_HT_600_27000,
		      
		      ]

mgp8_pp_h012j_5f_HT_0_27000_haa.splitFactor = 10
mgp8_pp_vbf_h01j_5f_HT_0_27000_haa.splitFactor = 5
mgp8_pp_tth01j_5f_HT_0_27000_haa.splitFactor = 20
mgp8_pp_vh012j_5f_HT_0_27000_haa.splitFactor = 10

mgp8_pp_aa012j_5f_HT_0_200.splitFactor = 10
mgp8_pp_aa012j_5f_HT_200_600.splitFactor = 10
mgp8_pp_aa012j_5f_HT_600_27000.splitFactor = 10
mgp8_gg_aa01j_5f_HT_0_200.splitFactor = 10
mgp8_gg_aa01j_5f_HT_200_600.splitFactor = 10
mgp8_gg_aa01j_5f_HT_600_27000.splitFactor = 10

#selectedComponents = [comp]

from heppy.FCChhAnalyses.analyzers.Reader import Reader

source = cfg.Analyzer(
    Reader,

    weights = 'mcEventWeights',

    gen_particles = 'skimmedGenParticles',
    
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

# select isolated photons with pT > 35 GeV and relIso < 0.4
from heppy.analyzers.Selector import Selector
selected_photons = cfg.Analyzer(
    Selector,
    'selected_photons',
    output = 'selected_photons',
    input_objects = 'photons',
    filter_func = lambda ptc: ptc.pt()> 25. and ptc.iso.sumpt/ptc.pt()<0.15
)


# select jet above 25 GeV
jets = cfg.Analyzer(
    Selector,
    'jets',
    output = 'jets',
    input_objects = 'jets',
    filter_func = lambda jet: jet.pt()>25.
)

from heppy.analyzers.Matcher import Matcher
match_photon_jets = cfg.Analyzer(
    Matcher,
    'photon_jets',
    delta_r = 0.2,
    match_particles = 'selected_photons',
    particles = 'jets'
)

jets_nophoton = cfg.Analyzer(
    Selector,
    'jets_nophoton',
    output = 'jets_nophoton',
    input_objects = 'jets',
    filter_func = lambda jet: jet.match is None
)

# select lights with pT > 25 GeV and relIso < 0.4
selected_lights = cfg.Analyzer(
    Selector,
    'selected_lights',
    output = 'selected_lights',
    input_objects = 'jets_nophoton',
    filter_func = lambda ptc: ptc.pt()>25 and ptc.tags['bf'] == 0
)

# select b's with pT > 25 GeV
selected_bs = cfg.Analyzer(
    Selector,
    'selected_bs',
    output = 'selected_bs',
    input_objects = 'jets_nophoton',
    filter_func = lambda ptc: ptc.pt()>25 and ptc.tags['bf'] > 0
)

# create H boson candidates with bs
from heppy.analyzers.ResonanceBuilder import ResonanceBuilder
higgses = cfg.Analyzer(
      ResonanceBuilder,
      output = 'higgses',
      leg_collection = 'selected_photons',
      pdgid = 25
)

# apply event selection. Defined in "analyzers/examples/haa/selection.py"
from heppy.FCChhAnalyses.HELHC.haa.selection import Selection
selection = cfg.Analyzer(
    Selection,
    instance_label='cuts'
)

# store interesting quantities into flat ROOT tree
from heppy.FCChhAnalyses.HELHC.haa.TreeProducer import TreeProducer
reco_tree = cfg.Analyzer(
    TreeProducer,
    higgses = 'higgses',
)

# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence( [
    source,
    selected_photons,
    jets,
    match_photon_jets,
    jets_nophoton,
    selected_lights,
    selected_bs,
    higgses,
    selection,
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
