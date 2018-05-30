import os, sys
import copy, math
import heppy.framework.config as cfg
import logging
import imp
# next 2 lines necessary to deal with reimports from ipython
logging.shutdown()
reload(logging)
logging.basicConfig(level=logging.WARNING)

sample=imp.load_source('heppylist', '/afs/cern.ch/work/h/helsens/public/FCCDicts/HELHC_heppySampleList_helhc_v01.py')

comp = cfg.Component(
    'example',
     files = [""]
)

selectedComponents = [ # from 100 TeV
                       sample.mgp8_pp_tth01j_5f_hbb,
                       sample.mgp8_pp_ttj_4f,
                       sample.mgp8_pp_ttbb_4f,
                       sample.mgp8_pp_ttz_5f,
                     ]

sample.mgp8_pp_tth01j_5f_hbb.splitFactor = 60
sample.mgp8_pp_ttj_4f.splitFactor = 150
sample.mgp8_pp_ttbb_4f.splitFactor = 70
sample.mgp8_pp_ttz_5f.splitFactor = 150

#selectedComponents = [comp]


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

    jets = 'pfjets04',
    bTags = 'pfbTags04',
    jetsFlavor  = 'pfjetsFlavor04',
 
    photons = 'photons',
    
    pfphotons = 'pfphotons',
    pfcharged = 'pfcharged',
    pfneutrals = 'pfneutrals',

    met = 'met',
   
    
    pfjets15 = 'pfjets15',
    pfjetsOneSubJettiness15 = 'pfjetsOneSubJettiness15', 
    pfjetsTwoSubJettiness15 = 'pfjetsTwoSubJettiness15', 
    pfjetsThreeSubJettiness15 = 'pfjetsThreeSubJettiness15', 
    pfsubjetsSoftDropTagged15 = 'pfsubjetsSoftDropTagged15', 
    pfsubjetsSoftDrop15 = 'pfsubjetsSoftDrop15',
    pfjetConst15 = 'pfjetConst15',    
    
    #pfjets08 = 'pfjets08',
    #pfjetsOneSubJettiness08 = 'pfjetsOneSubJettiness08', 
    #pfjetsTwoSubJettiness08 = 'pfjetsTwoSubJettiness08', 
    #pfjetsThreeSubJettiness08 = 'pfjetsThreeSubJettiness08', 
    #pfsubjetsSoftDropTagged08 = 'pfsubjetsSoftDropTagged08', 
    #pfsubjetsSoftDrop08 = 'pfsubjetsSoftDrop08', 
    


)

from ROOT import gSystem
gSystem.Load("libdatamodelDict")
from EventStore import EventStore as Events

#############################
##   Gen Level Analysis    ##
#############################

# select stable electrons and muons
from heppy.analyzers.Selector import Selector
gen_higgses = cfg.Analyzer(
    Selector,
    'gen_higgses',
    output = 'gen_higgses',
    input_objects = 'gen_particles',
    filter_func = lambda ptc: (abs(ptc.pdgid()) == 25 and ptc.status() == 62)
)

# select stable electrons and muons
from heppy.analyzers.Selector import Selector
gen_tops = cfg.Analyzer(
    Selector,
    'gen_tops',
    output = 'gen_tops',
    input_objects = 'gen_particles',
    filter_func = lambda ptc: (abs(ptc.pdgid()) == 6 and ptc.status() == 62)
)

# select stable electrons and muons
from heppy.analyzers.Selector import Selector
gen_bs = cfg.Analyzer(
    Selector,
    'gen_bs',
    output = 'gen_bs',
    input_objects = 'gen_particles',
    filter_func = lambda ptc: (abs(ptc.pdgid()) == 5 and ptc.pt() > 50.)
)

# produce flat root tree containing information about stable leptons in the event
from heppy.FCChhAnalyses.HELHC.hh_boosted.GenTreeProducer import GenTreeProducer
gen_tree = cfg.Analyzer(
    GenTreeProducer,
    gen_higgses = 'gen_higgses',
)

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
    filter_func = lambda ptc: ptc.pt()>15 and ptc.iso.sumpt/ptc.pt()<0.2
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

# select jet above 30 GeV
untagged_jets = cfg.Analyzer(
    Selector,
    'untagged_jets',
    output = 'untagged_jets',
    input_objects = 'jets',
    filter_func = lambda jet: jet.pt()>30.
)

# apply jet flavour tagging

from heppy.FCChhAnalyses.analyzers.FlavourTagger import FlavourTagger
jets_30 = cfg.Analyzer(
    FlavourTagger,
    'jets_30',
    input_jets = 'untagged_jets',
    input_genparticles = 'gen_particles',
    output_jets = 'jets_30',
    dr_match = 0.4,
    pdg_tags = [5, 4, 0],
    ptr_min = 0.1,
)

from heppy.analyzers.Matcher import Matcher
match_lepton_jets = cfg.Analyzer(
    Matcher,
    'lepton_jets',
    delta_r = 0.4,
    match_particles = 'selected_leptons',
    particles = 'jets_30'
)

jets_nolepton = cfg.Analyzer(
    Selector,
    'jets_nolepton',
    output = 'jets_nolepton',
    input_objects = 'jets_30',
    filter_func = lambda jet: jet.match is None and jet.pt()>30
)

# select b's with pT > 30 GeV
selected_bs = cfg.Analyzer(
    Selector,
    'selected_bs',
    output = 'selected_bs',
    input_objects = 'jets_nolepton',
    filter_func = lambda ptc: ptc.pt()>30 and ptc.tags['bf'] > 0
)

from heppy.analyzers.Selector import Selector
# select jet above 200 GeV
fatjets_200 = cfg.Analyzer(
    Selector,
    'fatjets_200',
    output = 'fatjets_200',
    input_objects = 'pfjets15',
    filter_func = lambda jet: jet.pt()>200.
)


from heppy.analyzers.Matcher import Matcher
match_lepton_fatjets = cfg.Analyzer(
    Matcher,
    'lepton_fatjets',
    delta_r = 1.0,
    match_particles = 'selected_leptons',
    particles = 'fatjets_200'
)

fatjets_nolepton = cfg.Analyzer(
    Selector,
    'fatjets_nolepton',
    output = 'fatjets_nolepton',
    input_objects = 'fatjets_200',
    filter_func = lambda jet: jet.match is None
)

# produce flat root tree containing jet substructure information
from heppy.FCChhAnalyses.HELHC.tth_boosted.TreeProducer import TreeProducer
reco_tree = cfg.Analyzer(
    TreeProducer,
    gen_bs = 'gen_bs',
    gen_higgses = 'gen_higgses',
    gen_tops = 'gen_tops',
    fatjets = 'fatjets_nolepton',
    selected_leptons = 'selected_leptons',
)


# produce flat root tree containing jet substructure information for training
from heppy.FCChhAnalyses.HELHC.tth_boosted.TreeProducerBDT import TreeProducerBDT
reco_tree_bdt = cfg.Analyzer(
    TreeProducerBDT,
    gen_bs = 'gen_bs',
    gen_higgses = 'gen_higgses',
    gen_tops = 'gen_tops',
    fatjets = 'fatjets_nolepton',
    selected_leptons = 'selected_leptons',
)



# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence( [
    source,
    gen_higgses,
    gen_tops,
    gen_bs,
    #gen_tree,
    selected_muons,
    selected_electrons,
    selected_leptons,
    untagged_jets,
    jets_30,
    match_lepton_jets,
    jets_nolepton,
    selected_bs,
    fatjets_200,
    match_lepton_fatjets,
    fatjets_nolepton,
    reco_tree,
    reco_tree_bdt,
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
