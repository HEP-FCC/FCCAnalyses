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
     files = ["/eos/experiment/fcc/ee/generation/DelphesEvents/fcc_v01/mgp8_ee_tt_ecm350/events_007264187.root"]
)

from FCCee_heppySampleList_fcc_v01 import *

selectedComponents = [
                      mgp8_ee_tt_ecm350,
		      ]

mgp8_ee_tt_ecm350.splitFactor = 10

selectedComponents = [comp]


from FCCeeAnalyses.analyzers.Reader import Reader

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


    jets = 'efjets',
    bTags = 'efbTags',
    cTags = 'efcTags',
    tauTags = 'eftauTags',

    photons = 'photons',
    photonITags = 'photonITags',
    photonsToMC = 'photonsToMC',

    pfphotons = 'efphotons',
    pfcharged = 'efcharged',
    pfneutrals = 'efneutrals',

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
    filter_func = lambda ptc: ptc.pt()>10
)

# select isolated muons
dressed_muons = cfg.Analyzer(
    Selector,
    'dressed_muons',
    output = 'dressed_muons',
    input_objects = 'sel_muons',
    filter_func = lambda ptc: ptc.iso.sumpt/ptc.pt()<0.4
)


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
match_muon_jets = cfg.Analyzer(
    Matcher,
    'muon_jets',
    delta_r = 0.2,
    match_particles = 'dressed_muons',
    particles = 'jets_10'
)

jets_nomuon = cfg.Analyzer(
    Selector,
    'jets_nomuon',
    output = 'jets_nomuon',
    input_objects = 'jets_10',
    filter_func = lambda jet: jet.match is None
)


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
    output = 'jets_nomuonnoelectron',
    input_objects = 'jets_nomuon',
    filter_func = lambda jet: jet.match is None
)



# select lights with pT > 10 GeV and relIso < 0.4
selected_lights = cfg.Analyzer(
    Selector,
    'selected_lights',
    output = 'selected_lights',
    input_objects = 'jets_nomuonnoelectron',
    filter_func = lambda ptc: ptc.pt()>1 and ptc.tags['bf'] == 0
)

# select b's with pT > 10 GeV
selected_bs = cfg.Analyzer(
    Selector,
    'selected_bs',
    output = 'selected_bs',
    input_objects = 'jets_nomuonnoelectron',
    filter_func = lambda ptc: ptc.pt()>10 and ptc.tags['bf'] > 0
)



# select tau's with pT > 10 GeV
selected_taus = cfg.Analyzer(
    Selector,
    'selected_taus',
    output = 'selected_taus',
    input_objects = 'jets_10',
    filter_func = lambda ptc: ptc.pt()>10 and ptc.tags['tauf'] > 0
)




# apply event selection. Defined in "selection.py"
from FCCeeAnalyses.tt.selection import Selection
selection = cfg.Analyzer(
    Selection,
    instance_label='cuts'
)


from heppy.analyzers.M3Builder import M3Builder
m3 = cfg.Analyzer(
    M3Builder,
    instance_label = 'm3',
    jets = 'jets_nomuonnoelectron',
    filter_func = lambda x : x.pt()>10.
)


from heppy.analyzers.MTW import MTW
mtw = cfg.Analyzer(
    MTW,
    instance_label = 'mtw',
    met = 'met',
    electron = 'dressed_electrons',
    muon = 'dressed_muons'
)

# store interesting quantities into flat ROOT tree
from FCCeeAnalyses.tt.TreeProducer import TreeProducer
reco_tree = cfg.Analyzer(
    TreeProducer,
    m3 = 'm3',
    mtw = 'mtw'
)






# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence( [
    source,
    sel_muons,
    sel_electrons,

    dressed_muons,
    dressed_electrons,
    jets_10,
    match_muon_jets,
    jets_nomuon,
    match_electron_jets,
    jets_noelectron,
    selected_lights,
    selected_bs,
    selected_taus,
    selection,
    m3,
    mtw,
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
