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
     files = ["/eos/experiment/fcc/hh/generation/DelphesEvents/fcc_v02/mgp8_pp_h012j_5f_hmumu/events_000001139.root"]
)

from FCC_heppySampleList_fcc_v02 import *

selectedComponents = [
                      mgp8_pp_h012j_5f_hmumu,
                      mgp8_pp_tth01j_5f_hmumu,
                      mgp8_pp_vbf_h01j_5f_hmumu,
                      mgp8_pp_vh012j_5f_hmumu,
                      mgp8_pp_mumu012j_mhcut_5f_HT_0_100,
		      mgp8_pp_mumu012j_mhcut_5f_HT_100_300,
		      mgp8_pp_mumu012j_mhcut_5f_HT_1100_100000,
		      mgp8_pp_mumu012j_mhcut_5f_HT_300_500,
		      mgp8_pp_mumu012j_mhcut_5f_HT_500_700,
		      mgp8_pp_mumu012j_mhcut_5f_HT_700_900,
		      mgp8_pp_mumu012j_mhcut_5f_HT_900_1100,
		      ]

mgp8_pp_h012j_5f_hmumu.splitFactor = 10
mgp8_pp_tth01j_5f_hmumu.splitFactor = 10
mgp8_pp_vbf_h01j_5f_hmumu.splitFactor = 10
mgp8_pp_vh012j_5f_hmumu.splitFactor = 10
#mgp8_pp_mumu012j_mhcut_5f.splitFactor = 10

mgp8_pp_mumu012j_mhcut_5f_HT_0_100.splitFactor = 10
mgp8_pp_mumu012j_mhcut_5f_HT_100_300.splitFactor = 3
mgp8_pp_mumu012j_mhcut_5f_HT_1100_100000.splitFactor = 2
mgp8_pp_mumu012j_mhcut_5f_HT_300_500.splitFactor = 2
mgp8_pp_mumu012j_mhcut_5f_HT_500_700.splitFactor = 2
mgp8_pp_mumu012j_mhcut_5f_HT_700_900.splitFactor = 2
mgp8_pp_mumu012j_mhcut_5f_HT_900_1100.splitFactor = 2

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

# select muons with pT > 10
from heppy.analyzers.Selector import Selector
sel_muons = cfg.Analyzer(
    Selector,
    'sel_muons',
    output = 'sel_muons',
    input_objects = 'muons',
    filter_func = lambda ptc: ptc.pt()>15
)

# select isolated muons
dressed_muons = cfg.Analyzer(
    Selector,
    'dressed_muons',
    output = 'dressed_muons',
    input_objects = 'sel_muons',
    filter_func = lambda ptc: ptc.iso.sumpt/ptc.pt()<0.4
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
match_muon_jets = cfg.Analyzer(
    Matcher,
    'muon_jets',
    delta_r = 0.2,
    match_particles = 'dressed_muons',
    particles = 'jets_30'
)

jets_nomuon = cfg.Analyzer(
    Selector,
    'jets_nomuon',
    output = 'jets_nomuon',
    input_objects = 'jets_30',
    filter_func = lambda jet: jet.match is None
)

# select lights with pT > 30 GeV and relIso < 0.4
selected_lights = cfg.Analyzer(
    Selector,
    'selected_lights',
    output = 'selected_lights',
    input_objects = 'jets_nomuon',
    filter_func = lambda ptc: ptc.pt()>30 and ptc.tags['bf'] == 0
)

# select b's with pT > 30 GeV
selected_bs = cfg.Analyzer(
    Selector,
    'selected_bs',
    output = 'selected_bs',
    input_objects = 'jets_nomuon',
    filter_func = lambda ptc: ptc.pt()>30 and ptc.tags['bf'] > 0
)

# create H boson candidates with bs
from heppy.FCChhAnalyses.analyzers.LeptonicHiggsBuilder import LeptonicHiggsBuilder
higgses = cfg.Analyzer(
      LeptonicHiggsBuilder,
      output = 'higgses',
      leptons = 'dressed_muons',
      pdgid = 25
)

# apply event selection. Defined in "analyzers/examples/hmumu/selection.py"
from heppy.FCChhAnalyses.FCChh.hmumu.selection import Selection
selection = cfg.Analyzer(
    Selection,
    instance_label='cuts'
)

# store interesting quantities into flat ROOT tree
from heppy.FCChhAnalyses.FCChh.hmumu.TreeProducer import TreeProducer
reco_tree = cfg.Analyzer(
    TreeProducer,
    higgses = 'higgses',
)

# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence( [
    source,
    sel_muons,
    dressed_muons,
    jets_30,
    match_muon_jets,
    jets_nomuon,
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
