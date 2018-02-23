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
     files = ["root://eospublic.cern.ch//eos/experiment/fcc/hh/generation/DelphesEvents/v0_0/pp_tth/events1.root"]
)

from heppySampleList import *

'''selectedComponents = [
                      pp_h012j_5f_HT_0_100_haa,
                      pp_h012j_5f_HT_100_400_haa,
                      pp_h012j_5f_HT_400_1000_haa,
                      pp_h012j_5f_HT_1000_1900_haa,
                      pp_h012j_5f_HT_1900_4400_haa,
                      pp_h012j_5f_HT_4400_8500_haa,
                      pp_h012j_5f_HT_8500_100000_haa,
                      pp_h012j_5f_haa,
                      pp_tth01j_5f_HT_0_1100_haa,
                      pp_tth01j_5f_HT_1100_2700_haa,
                      pp_tth01j_5f_HT_2700_4900_haa,
                      pp_tth01j_5f_HT_4900_8100_haa,
                      pp_tth01j_5f_HT_8100_100000_haa,
                      pp_tth01j_5f_haa,
                      pp_vbf_h01j_5f_HT_0_2000_haa,
                      pp_vbf_h01j_5f_HT_2000_4000_haa,
                      pp_vbf_h01j_5f_HT_4000_7200_haa,
                      pp_vbf_h01j_5f_HT_7200_100000_haa,
                      pp_vbf_h01j_5f_haa,
                      pp_vh012j_5f_HT_0_300_haa,
                      pp_vh012j_5f_HT_300_1400_haa,
                      pp_vh012j_5f_HT_1400_2900_haa,
                      pp_vh012j_5f_HT_2900_5300_haa,
                      pp_vh012j_5f_HT_5300_8800_haa,
                      pp_vh012j_5f_HT_8800_100000_haa,
                      pp_vh012j_5f_haa,
                      gg_aa01j_5f_HT_0_500,
                      gg_aa01j_5f_HT_500_1000,
                      gg_aa01j_5f_HT_1000_2000,
                      gg_aa01j_5f_HT_2000_4000,
                      gg_aa01j_5f_HT_4000_7200,
                      gg_aa01j_5f_HT_7200_100000,
                      gg_aa01j_5f,
                      pp_aa012j_5f_HT_0_500,
                      pp_aa012j_5f_HT_500_1000,
                      pp_aa012j_5f_HT_1000_2000,
                      pp_aa012j_5f_HT_2000_4000,
                      pp_aa012j_5f_HT_4000_7200,
                      pp_aa012j_5f_HT_7200_100000,
                      pp_aa012j_5f,
                      pp_aj012j_5f_HT_0_500,
                      pp_aj012j_5f_HT_500_1000,
                      pp_aj012j_5f_HT_1000_2000,
                      pp_aj012j_5f_HT_2000_4000,
                      pp_aj012j_5f_HT_4000_7200,
                      pp_aj012j_5f_HT_7200_100000,
                      pp_aj012j_5f,
                      ]

selectedComponents_fakes = [pp_aj012j_5f]

pp_h012j_5f_HT_0_100_haa.splitFactor = 10
pp_h012j_5f_HT_100_400_haa.splitFactor = 10
pp_h012j_5f_HT_400_1000_haa.splitFactor = 10
pp_h012j_5f_HT_1000_1900_haa.splitFactor = 10
pp_h012j_5f_HT_1900_4400_haa.splitFactor = 10
pp_h012j_5f_HT_4400_8500_haa.splitFactor = 10
pp_h012j_5f_HT_8500_100000_haa.splitFactor = 10
pp_h012j_5f_haa.splitFactor = 10
pp_tth01j_5f_HT_0_1100_haa.splitFactor = 10
pp_tth01j_5f_HT_1100_2700_haa.splitFactor = 10
pp_tth01j_5f_HT_2700_4900_haa.splitFactor = 10
pp_tth01j_5f_HT_4900_8100_haa.splitFactor = 10
pp_tth01j_5f_HT_8100_100000_haa.splitFactor = 10
pp_tth01j_5f_haa.splitFactor = 10
pp_vbf_h01j_5f_HT_0_2000_haa.splitFactor = 10
pp_vbf_h01j_5f_HT_2000_4000_haa.splitFactor = 10
pp_vbf_h01j_5f_HT_4000_7200_haa.splitFactor = 10
pp_vbf_h01j_5f_HT_7200_100000_haa.splitFactor = 10
pp_vbf_h01j_5f_haa.splitFactor = 10
pp_vh012j_5f_HT_0_300_haa.splitFactor = 10
pp_vh012j_5f_HT_300_1400_haa.splitFactor = 10
pp_vh012j_5f_HT_1400_2900_haa.splitFactor = 10
pp_vh012j_5f_HT_2900_5300_haa.splitFactor = 10
pp_vh012j_5f_HT_5300_8800_haa.splitFactor = 10
pp_vh012j_5f_HT_8800_100000_haa.splitFactor = 10
pp_vh012j_5f_haa.splitFactor = 10
gg_aa01j_5f_HT_0_500.splitFactor = 10
gg_aa01j_5f_HT_500_1000.splitFactor = 10
gg_aa01j_5f_HT_1000_2000.splitFactor = 10
gg_aa01j_5f_HT_2000_4000.splitFactor = 10
gg_aa01j_5f_HT_4000_7200.splitFactor = 10
gg_aa01j_5f_HT_7200_100000.splitFactor = 10
gg_aa01j_5f.splitFactor = 10
pp_aa012j_5f_HT_0_500.splitFactor = 10
pp_aa012j_5f_HT_500_1000.splitFactor = 10
pp_aa012j_5f_HT_1000_2000.splitFactor = 10
pp_aa012j_5f_HT_2000_4000.splitFactor = 10
pp_aa012j_5f_HT_4000_7200.splitFactor = 10
pp_aa012j_5f_HT_7200_100000.splitFactor = 10
pp_aa012j_5f.splitFactor = 10
pp_aj012j_5f_HT_0_500.splitFactor = 10
pp_aj012j_5f_HT_500_1000.splitFactor = 10
pp_aj012j_5f_HT_1000_2000.splitFactor = 10
pp_aj012j_5f_HT_2000_4000.splitFactor = 10
pp_aj012j_5f_HT_4000_7200.splitFactor = 10
pp_aj012j_5f_HT_7200_100000.splitFactor = 10
pp_aj012j_5f.splitFactor = 10
'''
selectedComponents = [comp]

#from heppy.analyzers.fcc.Reader import Reader
#for fcc_v02
from heppy.FCChhAnalyses.analyzers.Reader import Reader

source = cfg.Analyzer(
    Reader,

    weights = 'mcEventWeights',

    gen_particles = 'skimmedGenParticles',
    
    muons = 'muons',
    muonITags = 'muonITags',
    muonsToMC = 'muonsToMC',

    jets = 'jets',
    bTags = 'bTags',
 
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
from heppy.FCChhAnalyses.haa.selection import Selection
selection = cfg.Analyzer(
    Selection,
    instance_label='cuts'
)

# store interesting quantities into flat ROOT tree
from heppy.FCChhAnalyses.haa.TreeProducer import TreeProducer
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
