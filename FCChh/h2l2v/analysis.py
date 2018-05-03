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
     files = ["root://eospublic.cern.ch//eos/fcc/hh/generation/DelphesEvents/decay/pp_h012j_5f_ww/events997.root"]
)

from heppySampleList import *

'''selectedComponents = [pp_h012j_5f_HT_0_100_hlvlv,
                      pp_h012j_5f_HT_100_400_hlvlv,
                      pp_h012j_5f_HT_400_1000_hlvlv,
                      pp_h012j_5f_HT_1000_1900_hlvlv,
                      pp_h012j_5f_HT_1900_4400_hlvlv,
                      pp_h012j_5f_HT_4400_8500_hlvlv,
                      pp_h012j_5f_HT_8500_100000_hlvlv,
                      pp_h012j_5f_hlvlv,
                      pp_tth01j_5f_HT_0_1100_hlvlv,
                      pp_tth01j_5f_HT_1100_2700_hlvlv,
                      pp_tth01j_5f_HT_2700_4900_hlvlv,
                      pp_tth01j_5f_HT_4900_8100_hlvlv,
                      pp_tth01j_5f_HT_8100_100000_hlvlv,
                      pp_tth01j_5f_hlvlv,
                      pp_vbf_h01j_5f_HT_0_2000_hlvlv,
                      pp_vbf_h01j_5f_HT_2000_4000_hlvlv,
                      pp_vbf_h01j_5f_HT_4000_7200_hlvlv,
                      pp_vbf_h01j_5f_HT_7200_100000_hlvlv,
                      pp_vbf_h01j_5f_hlvlv,
                      pp_vh012j_5f_HT_0_300_hlvlv,
                      pp_vh012j_5f_HT_300_1400_hlvlv,
                      pp_vh012j_5f_HT_1400_2900_hlvlv,
                      pp_vh012j_5f_HT_2900_5300_hlvlv,
                      pp_vh012j_5f_HT_5300_8800_hlvlv,
                      pp_vh012j_5f_HT_8800_100000_hlvlv,
                      pp_vh012j_5f_hlvlv,
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
                      pp_tv012j_5f_HT_0_500,
                      pp_tv012j_5f_HT_500_1500,
                      pp_tv012j_5f_HT_1500_2800,
                      pp_tv012j_5f_HT_2800_4700,
                      pp_tv012j_5f_HT_4700_7400,
                      pp_tv012j_5f_HT_7400_100000,
                      pp_tv012j_5f,
                      pp_vvv01j_5f_HT_0_1200,
                      pp_vvv01j_5f_HT_1200_3000,
                      pp_vvv01j_5f_HT_3000_6000,
                      pp_vvv01j_5f_HT_6000_100000,
                      pp_vvv01j_5f,
                      ]

pp_h012j_5f_HT_0_100_hlvlv.splitFactor = 10
pp_h012j_5f_HT_100_400_hlvlv.splitFactor = 10
pp_h012j_5f_HT_400_1000_hlvlv.splitFactor = 10
pp_h012j_5f_HT_1000_1900_hlvlv.splitFactor = 10
pp_h012j_5f_HT_1900_4400_hlvlv.splitFactor = 10
pp_h012j_5f_HT_4400_8500_hlvlv.splitFactor = 10
pp_h012j_5f_HT_8500_100000_hlvlv.splitFactor = 10
pp_h012j_5f_hlvlv.splitFactor = 10
pp_tth01j_5f_HT_0_1100_hlvlv.splitFactor = 10
pp_tth01j_5f_HT_1100_2700_hlvlv.splitFactor = 10
pp_tth01j_5f_HT_2700_4900_hlvlv.splitFactor = 10
pp_tth01j_5f_HT_4900_8100_hlvlv.splitFactor = 10
pp_tth01j_5f_HT_8100_100000_hlvlv.splitFactor = 10
pp_tth01j_5f_hlvlv.splitFactor = 10
pp_vbf_h01j_5f_HT_0_2000_hlvlv.splitFactor = 10
pp_vbf_h01j_5f_HT_2000_4000_hlvlv.splitFactor = 10
pp_vbf_h01j_5f_HT_4000_7200_hlvlv.splitFactor = 10
pp_vbf_h01j_5f_HT_7200_100000_hlvlv.splitFactor = 10
pp_vbf_h01j_5f_hlvlv.splitFactor = 10
pp_vh012j_5f_HT_0_300_hlvlv.splitFactor = 10
pp_vh012j_5f_HT_300_1400_hlvlv.splitFactor = 10
pp_vh012j_5f_HT_1400_2900_hlvlv.splitFactor = 10
pp_vh012j_5f_HT_2900_5300_hlvlv.splitFactor = 10
pp_vh012j_5f_HT_5300_8800_hlvlv.splitFactor = 10
pp_vh012j_5f_HT_8800_100000_hlvlv.splitFactor = 10
pp_vh012j_5f_hlvlv.splitFactor = 10
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
pp_tv012j_5f_HT_0_500.splitFactor = 10
pp_tv012j_5f_HT_500_1500.splitFactor = 10
pp_tv012j_5f_HT_1500_2800.splitFactor = 10
pp_tv012j_5f_HT_2800_4700.splitFactor = 10
pp_tv012j_5f_HT_4700_7400.splitFactor = 10
pp_tv012j_5f_HT_7400_100000.splitFactor = 10
pp_tv012j_5f.splitFactor = 10
pp_vvv01j_5f_HT_0_1200.splitFactor = 10
pp_vvv01j_5f_HT_1200_3000.splitFactor = 10
pp_vvv01j_5f_HT_3000_6000.splitFactor = 10
pp_vvv01j_5f_HT_6000_100000.splitFactor = 10
pp_vvv01j_5f.splitFactor = 10
'''

selectedComponents = [comp]

from heppy.FCChhAnalyses.analyzers.Reader import Reader

source = cfg.Analyzer(
    Reader,

    weights = 'mcEventWeights',

    gen_particles = 'skimmedGenParticles',
    
    muons = 'muons',
    muonITags = 'muonITags',
    muonsToMC = 'muonsToMC',

    electrons = 'electrons',
    electronITags = 'electronITags',
    electronsToMC = 'electronsToMC',

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


'''
####### ADVANCED ANALYSIS (double check workflow) ######################)

# select fsr photon candidates
from heppy.analyzers.Selector import Selector
sel_photons = cfg.Analyzer(
    Selector,
    'sel_photons',
    output = 'sel_photons',
    input_objects = 'photons',
    filter_func = lambda ptc: ptc.pt()>2
)

# produce particle collection to be used for fsr photon isolation
from heppy.analyzers.Merger import Merger
iso_candidates = cfg.Analyzer(
      Merger,
      instance_label = 'iso_candidates', 
      inputs = ['pfphotons','pfcharged','pfneutrals'],
      output = 'iso_candidates'
)
# compute fsr photon isolation w/r other particles in the event.
from heppy.analyzers.IsolationAnalyzer import IsolationAnalyzer
from heppy.particles.isolation import EtaPhiCircle

iso_photons = cfg.Analyzer(
    IsolationAnalyzer,
    candidates = 'photons',
    particles = 'iso_candidates',
    iso_area = EtaPhiCircle(0.3)
)

# select isolated photons
sel_iso_photons = cfg.Analyzer(
    Selector,
    'sel_iso_photons',
    output = 'sel_iso_photons',
    input_objects = 'sel_photons',
    filter_func = lambda ptc : ptc.iso.sumpt/ptc.pt()<1.0
)

# remove fsr photons from particle-flow photon collections
from heppy.analyzers.Subtractor import Subtractor
pfphotons_nofsr = cfg.Analyzer(
      Subtractor,
      instance_label = 'pfphotons_nofsr', 
      inputA = 'pfphotons',
      inputB = 'sel_iso_photons',
      output = 'pfphotons_nofsr'
)

# produce particle collection to be used for lepton isolation
iso_candidates_nofsr = cfg.Analyzer(
      Merger,
      instance_label = 'iso_candidates_nofsr', 
      inputs = ['pfphotons_nofsr','pfcharged','pfneutrals'],
      output = 'iso_candidates_nofsr'
)

# select muons with pT > 10
from heppy.analyzers.Selector import Selector
sel_muons = cfg.Analyzer(
    Selector,
    'sel_muons',
    output = 'sel_muons',
    input_objects = 'muons',
    filter_func = lambda ptc: ptc.pt()>10
)

# compute muon isolation 
iso_muons = cfg.Analyzer(
    IsolationAnalyzer,
    candidates = 'sel_muons',
    particles = 'iso_candidates_nofsr',
    iso_area = EtaPhiCircle(0.4)
)

# "dress" muons with fsr photons
from heppy.analyzers.LeptonFsrDresser import LeptonFsrDresser
dressed_muons = cfg.Analyzer(
    LeptonFsrDresser,
    output = 'dressed_muons',
    particles = 'sel_iso_photons',
    leptons = 'sel_iso_muons',
    area = EtaPhiCircle(0.3)
)
'''

######################## SIMPLE ANALYSIS #####################

# select isolated muons with pT > 5 GeV and relIso < 0.4
from heppy.analyzers.Selector import Selector
selected_muons = cfg.Analyzer(
    Selector,
    'selected_muons',
    output = 'selected_muons',
    input_objects = 'muons',
    filter_func = lambda ptc: ptc.pt()>15 and ptc.iso.sumpt/ptc.pt()<0.1
)

# select electrons with pT > 7 GeV and relIso < 0.4
selected_electrons = cfg.Analyzer(
    Selector,
    'selected_electrons',
    output = 'selected_electrons',
    input_objects = 'electrons',
    filter_func = lambda ptc: ptc.pt()>15 and ptc.iso.sumpt/ptc.pt()<0.1
)

# merge electrons and muons into a single lepton collection
from heppy.analyzers.Merger import Merger
selected_leptons = cfg.Analyzer(
      Merger,
      instance_label = 'selected_leptons', 
      inputs = ['selected_electrons','selected_muons'],
      output = 'selected_leptons'
)

###############################################################


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

# create H boson candidates with bs
from heppy.analyzers.LeptonicHiggs2l2vBuilder import LeptonicHiggs2l2vBuilder
higgses = cfg.Analyzer(
      LeptonicHiggs2l2vBuilder,
      output = 'higgses',
      leptons = 'selected_leptons',
      pdgid = 25
)

# apply event selection. Defined in "analyzers/examples/h2l2v/selection.py"
from heppy.FCChhAnalyses.FCChh.h2l2v.selection import Selection
selection = cfg.Analyzer(
    Selection,
    instance_label='cuts'
)

# store interesting quantities into flat ROOT tree
from heppy.FCChhAnalyses.FCChh.h2l2v.TreeProducer import TreeProducer
reco_tree = cfg.Analyzer(
    TreeProducer,
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
