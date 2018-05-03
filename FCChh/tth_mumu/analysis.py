import os, sys
import copy
import heppy.framework.config as cfg

import logging
# next 2 lines necessary to deal with reimports from ipython
logging.shutdown()
reload(logging)
logging.basicConfig(level=logging.WARNING)

# for the sample lists
sys.path.append('/afs/cern.ch/work/h/helsens/public/FCCDicts/')


# pre-produced input files
comp = cfg.Component(
    'example',
     files = ["root://eospublic.cern.ch///eos/experiment/fcc/hh/generation/DelphesEvents/fcc_v01/pp_ll012j_5f/events100.root"]
     files = ["root://eospublic.cern.ch///eos/experiment/fcc/hh/generation/DelphesEvents/fcc_v01/pp_tth01j_5f_hmumu/events0.root"]
)

from heppySampleList_fcc_v01 import *

selectedComponents = [
    pp_ll012j_5f,
    pp_tth01j_5f_hmumu,
                       ]



pp_ll012j_5f.splitFactor = 10
pp_tth01j_5f_hmumu.splitFactor = 10


# uncomment to try with local file 
selectedComponents = [comp]

#from heppy.analyzers.fcc.Reader import Reader
#for fcc_v02
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

from heppy.analyzers.Selector import Selector
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


# select isolated muons with pT > 20 GeV and relIso < 0.4
selected_muons = cfg.Analyzer(
    Selector,
    'selected_muons',
    output = 'selected_muons',
    input_objects = 'muons',
    filter_func = lambda ptc: ptc.pt()>20 and ptc.iso.sumpt/ptc.pt()<0.4

)

# select electrons with pT > 20 GeV and relIso < 0.4
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

from heppy.analyzers.Selector import Selector
jets_nolepton = cfg.Analyzer(
    Selector,
    'jets_nolepton',
    output = 'jets_nolepton',
    input_objects = 'jets_30',
    filter_func = lambda jet: jet.match is None
)



from heppy.FCChhAnalyses.FCChh.tth_mumu.selection import Selection
selection = cfg.Analyzer(
    Selection,
    instance_label='cuts'
)


# create H boson candidates with bs
from heppy.FCChhAnalyses.analyzers.LeptonicHiggsBuilder import LeptonicHiggsBuilder
higgses = cfg.Analyzer(
      LeptonicHiggsBuilder,
      output = 'higgses',
      leptons = 'selected_muons',
      pdgid = 25
)

# apply event selection. 
from heppy.FCChhAnalyses.FCChh.tth_mumu.selection import Selection
selection = cfg.Analyzer(
    Selection,
    instance_label='cuts'
)

# store interesting quantities into flat ROOT tree
from heppy.FCChhAnalyses.FCChh.tth_mumu.TreeProducer import TreeProducer
reco_tree = cfg.Analyzer(
    TreeProducer,
    higgses="higgses",

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
    jets_nomuon,
    selected_lights,
    selected_bs,
    selection,
    higgses,
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
