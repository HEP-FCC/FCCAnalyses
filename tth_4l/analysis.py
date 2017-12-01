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
     #files = ["root://eospublic.cern.ch//eos/fcc/hh/generation/DelphesEvents/decay/pp_h012j_5f_zz/events997.root"]
     files = ["FCChhAnalyses/tth_4l/events0.root"]
)

from heppySampleList_fcc_v01 import *

'''selectedComponents = [
                      pp_h012j_5f_HT_0_100_hllll,
                      pp_h012j_5f_HT_100_400_hllll,
                      pp_h012j_5f_HT_400_1000_hllll,
                      pp_h012j_5f_HT_1000_1900_hllll,
                      pp_h012j_5f_HT_1900_4400_hllll,
                      pp_h012j_5f_HT_4400_8500_hllll,
                      pp_h012j_5f_HT_8500_100000_hllll,
                      pp_h012j_5f_hllll,
                      pp_tth01j_5f_HT_0_1100_hllll,
                      pp_tth01j_5f_HT_1100_2700_hllll,
                      pp_tth01j_5f_HT_2700_4900_hllll,
                      pp_tth01j_5f_HT_4900_8100_hllll,
                      pp_tth01j_5f_HT_8100_100000_hllll,
                      pp_tth01j_5f_hllll,
                      pp_vbf_h01j_5f_HT_0_2000_hllll,
                      pp_vbf_h01j_5f_HT_2000_4000_hllll,
                      pp_vbf_h01j_5f_HT_4000_7200_hllll,
                      pp_vbf_h01j_5f_HT_7200_100000_hllll,
                      pp_vbf_h01j_5f_hllll,
                      pp_vh012j_5f_HT_0_300_hllll,
                      pp_vh012j_5f_HT_300_1400_hllll,
                      pp_vh012j_5f_HT_1400_2900_hllll,
                      pp_vh012j_5f_HT_2900_5300_hllll,
                      pp_vh012j_5f_HT_5300_8800_hllll,
                      pp_vh012j_5f_HT_8800_100000_hllll,
                      pp_vh012j_5f_hllll,
                      pp_llv01j_5f_HT_0_800,
                      pp_llv01j_5f_HT_800_2000,
                      pp_llv01j_5f_HT_2000_4000,
                      pp_llv01j_5f_HT_4000_100000,
                      pp_llv01j_5f,
                      pp_ll012j_5f_HT_0_200,
                      pp_ll012j_5f_HT_200_700,
                      pp_ll012j_5f_HT_700_1500,
                      pp_ll012j_5f_HT_1500_2700,
                      pp_ll012j_5f_HT_2700_4200,
                      pp_ll012j_5f_HT_4200_100000,
                      pp_ll012j_5f,
                      pp_v0123j_5f_HT_0_1500,
                      pp_v0123j_5f_HT_1500_2900,
                      pp_v0123j_5f_HT_2900_5100,
                      pp_v0123j_5f_HT_5100_8500,
                      pp_v0123j_5f_HT_8500_100000,
                      pp_v0123j_5f,
                      pp_vv012j_5f_HT_0_300,
                      pp_vv012j_5f_HT_300_1400,
                      pp_vv012j_5f_HT_1400_2900,
                      pp_vv012j_5f_HT_2900_5300,
                      pp_vv012j_5f_HT_5300_8800,
                      pp_vv012j_5f_HT_8800_100000,
                      pp_vv012j_5f,
                      pp_tt012j_5f_HT_0_600,
                      pp_tt012j_5f_HT_600_1200,
                      pp_tt012j_5f_HT_1200_2100,
                      pp_tt012j_5f_HT_2100_3400,
                      pp_tt012j_5f_HT_3400_5300,
                      pp_tt012j_5f_HT_5300_8100,
                      pp_tt012j_5f_HT_8100_100000,
                      pp_tt012j_5f,
                      pp_llll01j_5f_HT_0_800,
                      pp_llll01j_5f_HT_800_2000,
                      pp_llll01j_5f_HT_2000_4000,
                      pp_llll01j_5f_HT_4000_100000,
                      pp_llll01j_5f,
                      pp_vvv01j_5f_HT_0_1200,
                      pp_vvv01j_5f_HT_1200_3000,
                      pp_vvv01j_5f_HT_3000_6000,
                      pp_vvv01j_5f_HT_6000_100000,
                      pp_vvv01j_5f,
                      ]


pp_h012j_5f_HT_0_100_hllll.splitFactor = 10
pp_h012j_5f_HT_100_400_hllll.splitFactor = 10
pp_h012j_5f_HT_400_1000_hllll.splitFactor = 10
pp_h012j_5f_HT_1000_1900_hllll.splitFactor = 10
pp_h012j_5f_HT_1900_4400_hllll.splitFactor = 10
pp_h012j_5f_HT_4400_8500_hllll.splitFactor = 10
pp_h012j_5f_HT_8500_100000_hllll.splitFactor = 10
pp_h012j_5f_hllll.splitFactor = 10
pp_tth01j_5f_HT_0_1100_hllll.splitFactor = 10
pp_tth01j_5f_HT_1100_2700_hllll.splitFactor = 10
pp_tth01j_5f_HT_2700_4900_hllll.splitFactor = 10
pp_tth01j_5f_HT_4900_8100_hllll.splitFactor = 10
pp_tth01j_5f_HT_8100_100000_hllll.splitFactor = 10
pp_tth01j_5f_hllll.splitFactor = 10
pp_vbf_h01j_5f_HT_0_2000_hllll.splitFactor = 10
pp_vbf_h01j_5f_HT_2000_4000_hllll.splitFactor = 10
pp_vbf_h01j_5f_HT_4000_7200_hllll.splitFactor = 10
pp_vbf_h01j_5f_HT_7200_100000_hllll.splitFactor = 10
pp_vbf_h01j_5f_hllll.splitFactor = 10
pp_vh012j_5f_HT_0_300_hllll.splitFactor = 10
pp_vh012j_5f_HT_300_1400_hllll.splitFactor = 10
pp_vh012j_5f_HT_1400_2900_hllll.splitFactor = 10
pp_vh012j_5f_HT_2900_5300_hllll.splitFactor = 10
pp_vh012j_5f_HT_5300_8800_hllll.splitFactor = 10
pp_vh012j_5f_HT_8800_100000_hllll.splitFactor = 10
pp_vh012j_5f_hllll.splitFactor = 10
pp_llv01j_5f_HT_0_800.splitFactor = 10
pp_llv01j_5f_HT_800_2000.splitFactor = 10
pp_llv01j_5f_HT_2000_4000.splitFactor = 10
pp_llv01j_5f_HT_4000_100000.splitFactor = 10
pp_llv01j_5f.splitFactor = 10
pp_ll012j_5f_HT_0_200.splitFactor = 10
pp_ll012j_5f_HT_200_700.splitFactor = 10
pp_ll012j_5f_HT_700_1500.splitFactor = 10
pp_ll012j_5f_HT_1500_2700.splitFactor = 10
pp_ll012j_5f_HT_2700_4200.splitFactor = 10
pp_ll012j_5f_HT_4200_100000.splitFactor = 10
pp_ll012j_5f.splitFactor = 10
pp_v0123j_5f_HT_0_1500.splitFactor = 10
pp_v0123j_5f_HT_1500_2900.splitFactor = 10
pp_v0123j_5f_HT_2900_5100.splitFactor = 10
pp_v0123j_5f_HT_5100_8500.splitFactor = 10
pp_v0123j_5f_HT_8500_100000.splitFactor = 10
pp_v0123j_5f.splitFactor = 10
pp_vv012j_5f_HT_0_300.splitFactor = 10
pp_vv012j_5f_HT_300_1400.splitFactor = 10
pp_vv012j_5f_HT_1400_2900.splitFactor = 10
pp_vv012j_5f_HT_2900_5300.splitFactor = 10
pp_vv012j_5f_HT_5300_8800.splitFactor = 10
pp_vv012j_5f_HT_8800_100000.splitFactor = 10
pp_vv012j_5f.splitFactor = 10
pp_tt012j_5f_HT_0_600.splitFactor = 10
pp_tt012j_5f_HT_600_1200.splitFactor = 10
pp_tt012j_5f_HT_1200_2100.splitFactor = 10
pp_tt012j_5f_HT_2100_3400.splitFactor = 10
pp_tt012j_5f_HT_3400_5300.splitFactor = 10
pp_tt012j_5f_HT_5300_8100.splitFactor = 10
pp_tt012j_5f_HT_8100_100000.splitFactor = 10
pp_tt012j_5f.splitFactor = 10
pp_llll01j_5f_HT_0_800.splitFactor = 10
pp_llll01j_5f_HT_800_2000.splitFactor = 10
pp_llll01j_5f_HT_2000_4000.splitFactor = 10
pp_llll01j_5f_HT_4000_100000.splitFactor = 10
pp_llll01j_5f.splitFactor = 10
pp_vvv01j_5f_HT_0_1200.splitFactor = 10
pp_vvv01j_5f_HT_1200_3000.splitFactor = 10
pp_vvv01j_5f_HT_3000_6000.splitFactor = 10
pp_vvv01j_5f_HT_6000_100000.splitFactor = 10
pp_vvv01j_5f.splitFactor = 10'''

selectedComponents = [comp]

from heppy.analyzers.fcc.Reader import Reader
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


# select isolated muons with pT > 5 GeV and relIso < 0.4
from heppy.analyzers.Selector import Selector
selected_muons = cfg.Analyzer(
    Selector,
    'selected_muons',
    output = 'selected_muons',
    input_objects = 'muons',
    filter_func = lambda ptc: ptc.pt()>20 and ptc.iso.sumpt/ptc.pt()<0.4
)

# select electrons with pT > 7 GeV and relIso < 0.4
selected_electrons = cfg.Analyzer(
    Selector,
    'selected_electrons',
    output = 'selected_electrons',
    input_objects = 'electrons',
    filter_func = lambda ptc: ptc.pt()>20 and ptc.iso.sumpt/ptc.pt()<0.4
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
from heppy.FCChhAnalyses.tth_4l.selection import Selection
selection = cfg.Analyzer(
    Selection,
    instance_label='cuts'
)

# store interesting quantities into flat ROOT tree
from heppy.FCChhAnalyses.tth_4l.TreeProducer import TreeProducer
reco_tree = cfg.Analyzer(
    TreeProducer,
    zeds = 'zeds',
    higgses = 'higgses',
    leptons = "selected_leptons"
)

from heppy.FCChhAnalyses.analyzers.ExtraLeptons import ExtraLeptons
extra_leptons = cfg.Analyzer(
    ExtraLeptons,
    inputA = "selected_leptons",
    inputB = "zeds",
    extra_leptons = "extra_leptons",
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
    extra_leptons,
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
