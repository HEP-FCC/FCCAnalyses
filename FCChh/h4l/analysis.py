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
     files = ["/eos/experiment/fcc/hh/generation/DelphesEvents/fcc_v02/mgp8_pp_h012j_5f_hllll/events_000000625.root"]
)

from FCC_heppySampleList_fcc_v02 import *

selectedComponents = [
                      mgp8_pp_h012j_5f_hllll,
                      mgp8_pp_tth01j_5f_hllll,
                      mgp8_pp_vbf_h01j_5f_hllll,
                      mgp8_pp_vh012j_5f_hllll,
                      mgp8_pp_llll01j_mhcut_5f_HT_0_200,
                      mgp8_pp_llll01j_mhcut_5f_HT_200_500,
                      mgp8_pp_llll01j_mhcut_5f_HT_500_1100,
                      mgp8_pp_llll01j_mhcut_5f_HT_1100_100000,
                      ]

mgp8_pp_h012j_5f_hllll.splitFactor = 50
mgp8_pp_vbf_h01j_5f_hllll.splitFactor = 50
mgp8_pp_tth01j_5f_hllll.splitFactor = 50
mgp8_pp_vh012j_5f_hllll.splitFactor = 50
mgp8_pp_llll01j_mhcut_5f_HT_0_200.splitFactor = 5
mgp8_pp_llll01j_mhcut_5f_HT_200_500.splitFactor = 5
mgp8_pp_llll01j_mhcut_5f_HT_500_1100.splitFactor = 5
mgp8_pp_llll01j_mhcut_5f_HT_1100_100000.splitFactor = 5

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
    filter_func = lambda ptc: ptc.pt()>5 and ptc.iso.sumpt/ptc.pt()<0.4
)

# select electrons with pT > 7 GeV and relIso < 0.4
selected_electrons = cfg.Analyzer(
    Selector,
    'selected_electrons',
    output = 'selected_electrons',
    input_objects = 'electrons',
    filter_func = lambda ptc: ptc.pt()>7 and ptc.iso.sumpt/ptc.pt()<0.4
)

# merge electrons and muons into a single lepton collection
from heppy.analyzers.Merger import Merger
selected_leptons = cfg.Analyzer(
      Merger,
      instance_label = 'selected_leptons', 
      inputs = ['selected_electrons','selected_muons'],
      output = 'selected_leptons'
)

# select jet above 30 GeV
jets_30 = cfg.Analyzer(
    Selector,
    'jets_30',
    output = 'jets_30',
    input_objects = 'jets',
    filter_func = lambda jet: jet.pt()>30.
)
from heppy.analyzers.Matcher import Matcher
match_lepton_jets = cfg.Analyzer(
    Matcher,
    'lepton_jets',
    delta_r = 0.2,
    match_particles = 'selected_leptons',
    particles = 'jets_30'
)

jets_nolepton = cfg.Analyzer(
    Selector,
    'jets_nolepton',
    output = 'jets_nolepton',
    input_objects = 'jets_30',
    filter_func = lambda jet: jet.match is None
)

# select lights with pT > 30 GeV and relIso < 0.4
selected_lights = cfg.Analyzer(
    Selector,
    'selected_lights',
    output = 'selected_lights',
    input_objects = 'jets_nolepton',
    filter_func = lambda ptc: ptc.pt()>30 and ptc.tags['bf'] == 0
)

# select b's with pT > 30 GeV
selected_bs = cfg.Analyzer(
    Selector,
    'selected_bs',
    output = 'selected_bs',
    input_objects = 'jets_nolepton',
    filter_func = lambda ptc: ptc.pt()>30 and ptc.tags['bf'] > 0
)

# create Z boson candidates with leptons
from heppy.analyzers.LeptonicZedBuilder import LeptonicZedBuilder
zeds = cfg.Analyzer(
      LeptonicZedBuilder,
      output = 'zeds',
      leptons = 'selected_leptons',
)

# create H boson candidates
from heppy.analyzers.ResonanceBuilder import ResonanceBuilder
higgses = cfg.Analyzer(
      ResonanceBuilder,
      output = 'higgses',
      leg_collection = 'zeds',
      pdgid = 25
)

# apply event selection. Defined in "analyzers/examples/h4l/selection.py"
from heppy.FCChhAnalyses.FCChh.h4l.selection import Selection
selection = cfg.Analyzer(
    Selection,
    instance_label='cuts'
)

# store interesting quantities into flat ROOT tree
from heppy.FCChhAnalyses.FCChh.h4l.TreeProducer import TreeProducer
reco_tree = cfg.Analyzer(
    TreeProducer,
    zeds = 'zeds',
    higgses = 'higgses',
)

# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence( [
    source,
    selected_muons,
    selected_electrons,
    selected_leptons,
    jets_30,
    match_lepton_jets,
    jets_nolepton,
    selected_lights,
    selected_bs,
    zeds,
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
