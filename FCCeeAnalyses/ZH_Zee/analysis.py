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
     files = ["/eos/experiment/fcc/ee/generation/DelphesEvents/fcc_v01/p8_ee_ZH_ecm240/events_033829802.root"]
)

from FCCee_heppySampleList_fcc_v01 import *

selectedComponents = [
                      p8_ee_ZH_ecm240,
                      p8_ee_ZZ_ecm240,
                      p8_ee_WW_ecm240
		      ]

p8_ee_ZH_ecm240.splitFactor = 10
p8_ee_ZZ_ecm240.splitFactor = 10
p8_ee_WW_ecm240.splitFactor = 10

selectedComponents = [comp]


from FCCeeAnalyses.analyzers.Reader import Reader

source = cfg.Analyzer(
    Reader,

    weights = 'mcEventWeights',

    gen_particles = 'skimmedGenParticles',
    
    electrons = 'electrons',
    electronITags = 'electronITags',
    electronsToMC = 'electronsToMC',

    jets = 'pfjets',
    bTags = 'pfbTags',
    cTags = 'pfcTags',

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

# select electrons with pT > 10
from heppy.analyzers.Selector import Selector
sel_electrons = cfg.Analyzer(
    Selector,
    'sel_electrons',
    output = 'sel_electrons',
    input_objects = 'electrons',
    filter_func = lambda ptc: ptc.pt()>10
)

# select isolated electrons
dressed_electrons = cfg.Analyzer(
    Selector,
    'dressed_electrons',
    output = 'dressed_electrons',
    input_objects = 'sel_electrons',
    filter_func = lambda ptc: ptc.iso.sumpt/ptc.pt()<0.4
)

###############################################################


# select jet above 10 GeV
jets_10 = cfg.Analyzer(
    Selector,
    'jets_10',
    output = 'jets_10',
    input_objects = 'jets',
    filter_func = lambda jet: jet.pt()>10.
)
from heppy.analyzers.Matcher import Matcher
match_electron_jets = cfg.Analyzer(
    Matcher,
    'electron_jets',
    delta_r = 0.2,
    match_particles = 'dressed_electrons',
    particles = 'jets_10'
)

jets_noelectron = cfg.Analyzer(
    Selector,
    'jets_noelectron',
    output = 'jets_noelectron',
    input_objects = 'jets_10',
    filter_func = lambda jet: jet.match is None
)

# select lights with pT > 10 GeV and relIso < 0.4
selected_lights = cfg.Analyzer(
    Selector,
    'selected_lights',
    output = 'selected_lights',
    input_objects = 'jets_noelectron',
    filter_func = lambda ptc: ptc.pt()>1 and ptc.tags['bf'] == 0
)

# select b's with pT > 10 GeV
selected_bs = cfg.Analyzer(
    Selector,
    'selected_bs',
    output = 'selected_bs',
    input_objects = 'jets_noelectron',
    filter_func = lambda ptc: ptc.pt()>10 and ptc.tags['bf'] > 0
)

# create H boson candidates with bs
from FCCeeAnalyses.analyzers.LeptonicZedBuilder import LeptonicZedBuilder
zeds = cfg.Analyzer(
      LeptonicZedBuilder,
      output = 'zeds',
      leptons = 'dressed_electrons',
      pdgid = 23
)

from heppy.analyzers.RecoilBuilder import RecoilBuilder
recoil = cfg.Analyzer(
    RecoilBuilder,
    output = 'recoil',
    sqrts = 240.,
    to_remove = 'zeds'
) 

# apply event selection. Defined in "selection.py"
from FCCeeAnalyses.ZH_Zee.selection import Selection
selection = cfg.Analyzer(
    Selection,
    instance_label='cuts'
)

# store interesting quantities into flat ROOT tree
from FCCeeAnalyses.ZH_Zee.TreeProducer import TreeProducer
reco_tree = cfg.Analyzer(
    TreeProducer,
    zeds = 'zeds',
    recoil = 'recoil',
)




# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence( [
    source,
    sel_electrons,
    dressed_electrons,
    jets_10,
    match_electron_jets,
    jets_noelectron,
    selected_lights,
    selected_bs,
    zeds,
    recoil,
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
