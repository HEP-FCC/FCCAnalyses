import os, sys, math
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
     files = ["/eos/experiment/fcc/hh/generation/DelphesEvents/fcc_v02/mgp8_pp_jjja_5f/events_000014779.root"]
)

from FCC_heppySampleList_fcc_v02 import *

selectedComponents = [
                      mgp8_pp_jjja_5f,
                     ]
		     
mgp8_pp_jjja_5f.splitFactor = 1000

#selectedComponents = [comp]

from heppy.FCChhAnalyses.analyzers.Reader import Reader
source = cfg.Analyzer(
    Reader,

    weights = 'mcEventWeights',

    gen_particles = 'skimmedGenParticles',

    jets = 'pfjets04',
    bTags = 'pfbTags04',
    
    photons = 'photons',
    photonsToMC = 'photonsToMC',
    photonITags = 'photonITags',

    electrons = 'electrons',
    electronITags = 'electronITags',
    electronsToMC = 'electronsToMC',

    muons = 'muons',
    muonITags = 'muonITags',
    muonsToMC = 'muonsToMC',
    
    met = 'met',
)

from ROOT import gSystem
gSystem.Load("libdatamodelDict")
from EventStore import EventStore as Events


#############################
##   Reco Level Analysis   ##
#############################

# select isolated muons with pT > 25 GeV and relIso < 0.2
from heppy.analyzers.Selector import Selector
selected_muons = cfg.Analyzer(
    Selector,
    'selected_muons',
    output = 'selected_muons',
    input_objects = 'muons',
    filter_func = lambda ptc: ptc.pt()>20 and ptc.iso.sumpt/ptc.pt()<0.15
)

# select electrons with pT > 25 GeV and relIso < 0.1
selected_electrons = cfg.Analyzer(
    Selector,
    'selected_electrons',
    output = 'selected_electrons',
    input_objects = 'electrons',
    filter_func = lambda ptc: ptc.pt()>20 and ptc.iso.sumpt/ptc.pt()<0.15
)

# merge electrons and muons into a single lepton collection
from heppy.analyzers.Merger import Merger
selected_leptons = cfg.Analyzer(
      Merger,
      instance_label = 'selected_leptons', 
      inputs = ['selected_electrons','selected_muons'],
      output = 'selected_leptons'
)

# select isolated photons with pT > 35 GeV and relIso < 0.4
from heppy.analyzers.Selector import Selector
selected_photons = cfg.Analyzer(
    Selector,
    'selected_photons',
    output = 'selected_photons',
    input_objects = 'photons',
    filter_func = lambda ptc: ptc.pt()> 30. and ptc.iso.sumpt/ptc.pt()<0.15
)


# select jet above 20 GeV
jets_25 = cfg.Analyzer(
    Selector,
    'jets_25',
    output = 'jets_25',
    input_objects = 'jets',
    filter_func = lambda jet: jet.pt()>30.
)

# clean jets from isolated electrons, muons and photons

from heppy.analyzers.Matcher import Matcher
match_jet_electrons = cfg.Analyzer(
    Matcher,
    'electron_jets',
    delta_r = 0.4,
    match_particles = 'selected_electrons',
    particles = 'jets_25'
)

jets_noelectron = cfg.Analyzer(
    Selector,
    'jets_noelectron',
    output = 'jets_noelectron',
    input_objects = 'jets_25',
    filter_func = lambda jet: jet.match is None
)

match_muon_jets = cfg.Analyzer(
    Matcher,
    'muon_jets',
    delta_r = 0.4,
    match_particles = 'selected_muons',
    particles = 'jets_noelectron'
)

jets_nomuon = cfg.Analyzer(
    Selector,
    'jets_nomuon',
    output = 'jets_nomuon',
    input_objects = 'jets_noelectron',
    filter_func = lambda jet: jet.match is None
)

match_photon_jets = cfg.Analyzer(
    Matcher,
    'photon_jets',
    delta_r = 0.4,
    match_particles = 'selected_photons',
    particles = 'jets_nomuon'
)

jets_nophoton = cfg.Analyzer(
    Selector,
    'jets_nophoton',
    output = 'jets_nophoton',
    input_objects = 'jets_nomuon',
    filter_func = lambda jet: jet.match is None
)

# convert jets into fake photons
from heppy.FCChhAnalyses.analyzers.FakeParticleBuilder import FakeParticleBuilder
fake_photons = cfg.Analyzer(
    FakeParticleBuilder,
    'fake_photons',
    input_objects = 'jets_nophoton',
    input_weights = 'weights',
    output_jets = 'jets_nofakes',
    output_fakes = 'fake_photons',
    output_weights = 'fake_weights',
    fake_prob = lambda pt: 0.002*math.exp(-pt/30.)
)

# merge prompt and fake photons into a single collection
from heppy.analyzers.Merger import Merger
merged_photons = cfg.Analyzer(
      Merger,
      instance_label = 'merged_photons', 
      inputs = ['selected_photons','fake_photons'],
      output = 'merged_photons'
)

# select lights with pT > 30 GeV and relIso < 0.4
selected_lights = cfg.Analyzer(
    Selector,
    'selected_lights',
    output = 'selected_lights',
    input_objects = 'jets_nofakes',
    filter_func = lambda ptc: ptc.tags['bf'] == 0
)

# select b's with pT > 35 GeV and relIso < 0.4
selected_bs = cfg.Analyzer(
    Selector,
    'selected_bs',
    output = 'selected_bs',
    input_objects = 'jets_nofakes',
    filter_func = lambda ptc: ptc.tags['bf'] > 0
)

# create H boson candidates with photons
from heppy.analyzers.ResonanceBuilder import ResonanceBuilder
photon_higgses = cfg.Analyzer(
      ResonanceBuilder,
      output = 'photon_higgses',
      leg_collection = 'merged_photons',
      pdgid = 25
)

# create H boson candidates with bs
from heppy.analyzers.ResonanceBuilder import ResonanceBuilder
b_higgses = cfg.Analyzer(
      ResonanceBuilder,
      output = 'b_higgses',
      leg_collection = 'selected_bs',
      pdgid = 25
)

# produce flat root tree containing information after pre-selection
from heppy.FCChhAnalyses.FCChh.hhbbaa.TreeProducer import TreeProducer
tree = cfg.Analyzer(
    TreeProducer,
    photons = 'merged_photons',
    bs = 'selected_bs',
    haas = 'photon_higgses',
    hbbs = 'b_higgses',
)


# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence( [
    source,
    selected_muons,
    selected_electrons,
    selected_leptons,
    selected_photons,
    jets_25,
    match_jet_electrons,
    jets_noelectron,
    match_muon_jets,
    jets_nomuon,
    match_photon_jets,
    jets_nophoton,
    fake_photons,
    merged_photons,
    selected_bs,
    selected_lights,
    photon_higgses,
    b_higgses,
    tree
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
