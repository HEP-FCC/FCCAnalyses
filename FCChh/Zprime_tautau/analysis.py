import os, sys
import copy
import heppy.framework.config as cfg
import logging
import imp
# next 2 lines necessary to deal with reimports from ipython
logging.shutdown()
reload(logging)
logging.basicConfig(level=logging.WARNING)

sample=imp.load_source('heppylist', '/afs/cern.ch/work/h/helsens/public/FCCDicts/FCC_heppySampleList_fcc_v02.py')

comp = cfg.Component(
    'example',
    files = ["/eos/experiment/fcc/hh/generation/DelphesEvents/fcc_v02/p8_pp_ZprimeSSM_20TeV_ll/events_135275618.root"]
)

selectedComponents = [
                        sample.p8_pp_ZprimeSSM_2TeV_ll,
                        sample.p8_pp_ZprimeSSM_4TeV_ll,
                        sample.p8_pp_ZprimeSSM_5TeV_ll,
                        sample.p8_pp_ZprimeSSM_6TeV_ll,
                        sample.p8_pp_ZprimeSSM_8TeV_ll,
                        sample.p8_pp_ZprimeSSM_10TeV_ll,
                        sample.p8_pp_ZprimeSSM_12TeV_ll,
                        sample.p8_pp_ZprimeSSM_14TeV_ll,
                        sample.p8_pp_ZprimeSSM_15TeV_ll,
                        sample.p8_pp_ZprimeSSM_16TeV_ll,
                        sample.p8_pp_ZprimeSSM_18TeV_ll,
                        sample.p8_pp_ZprimeSSM_20TeV_ll,
                        sample.p8_pp_ZprimeSSM_25TeV_ll,
                        sample.p8_pp_ZprimeSSM_30TeV_ll,
                        sample.mgp8_pp_tautau_5f_HT_500_1000,
                        sample.mgp8_pp_tautau_5f_HT_1000_2000,
                        sample.mgp8_pp_tautau_5f_HT_2000_5000,
                        sample.mgp8_pp_tautau_5f_HT_5000_10000,
                        sample.mgp8_pp_tautau_5f_HT_10000_27000,
                        sample.mgp8_pp_tautau_5f_HT_27000_100000,
                        sample.mgp8_pp_jj_5f_HT_500_1000,
                        sample.mgp8_pp_jj_5f_HT_1000_2000,
                        sample.mgp8_pp_jj_5f_HT_2000_5000,
                        sample.mgp8_pp_jj_5f_HT_5000_10000,
                        sample.mgp8_pp_jj_5f_HT_10000_27000,
                        sample.mgp8_pp_jj_5f_HT_27000_100000,
                     ]

splitFac = 10
sample.p8_pp_ZprimeSSM_2TeV_ll.splitFactor  = splitFac
sample.p8_pp_ZprimeSSM_4TeV_ll.splitFactor  = splitFac
sample.p8_pp_ZprimeSSM_5TeV_ll.splitFactor  = splitFac
sample.p8_pp_ZprimeSSM_6TeV_ll.splitFactor  = splitFac
sample.p8_pp_ZprimeSSM_8TeV_ll.splitFactor  = splitFac
sample.p8_pp_ZprimeSSM_10TeV_ll.splitFactor = splitFac
sample.p8_pp_ZprimeSSM_12TeV_ll.splitFactor = splitFac
sample.p8_pp_ZprimeSSM_14TeV_ll.splitFactor = splitFac
sample.p8_pp_ZprimeSSM_15TeV_ll.splitFactor = splitFac
sample.p8_pp_ZprimeSSM_16TeV_ll.splitFactor = splitFac
sample.p8_pp_ZprimeSSM_18TeV_ll.splitFactor = splitFac
sample.p8_pp_ZprimeSSM_20TeV_ll.splitFactor = splitFac
sample.p8_pp_ZprimeSSM_25TeV_ll.splitFactor = splitFac
sample.p8_pp_ZprimeSSM_30TeV_ll.splitFactor = splitFac

splitFac2 = 60
sample.mgp8_pp_tautau_5f_HT_500_1000.splitFactor     = splitFac2
sample.mgp8_pp_tautau_5f_HT_1000_2000.splitFactor    = splitFac2
sample.mgp8_pp_tautau_5f_HT_2000_5000.splitFactor    = splitFac2
sample.mgp8_pp_tautau_5f_HT_5000_10000.splitFactor   = splitFac2
sample.mgp8_pp_tautau_5f_HT_10000_27000.splitFactor  = splitFac2
sample.mgp8_pp_tautau_5f_HT_27000_100000.splitFactor = splitFac2
sample.mgp8_pp_jj_5f_HT_500_1000.splitFactor     = splitFac2
sample.mgp8_pp_jj_5f_HT_1000_2000.splitFactor    = splitFac2
sample.mgp8_pp_jj_5f_HT_2000_5000.splitFactor    = splitFac2
sample.mgp8_pp_jj_5f_HT_5000_10000.splitFactor   = splitFac2
sample.mgp8_pp_jj_5f_HT_10000_27000.splitFactor  = splitFac2
sample.mgp8_pp_jj_5f_HT_27000_100000.splitFactor = splitFac2


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

    # used for tau-tagging
    pfjets04  = 'pfjets04',
    pftauTags04 = 'pftauTags04',

    met = 'met',

)

from ROOT import gSystem
gSystem.Load("libdatamodelDict")
from EventStore import EventStore as Events

#############################
##   Reco Level Analysis   ##
#############################


# select isolated muons with pT > 50 GeV and relIso < 0.4
from heppy.analyzers.Selector import Selector
selected_muons = cfg.Analyzer(
    Selector,
    'selected_muons',
    output = 'selected_muons',
    input_objects = 'muons',
    filter_func = lambda ptc: ptc.pt()>100 and ptc.iso.sumpt/ptc.pt()<0.4

)

# select electrons with pT > 50 GeV and relIso < 0.4
selected_electrons = cfg.Analyzer(
    Selector,
    'selected_electrons',
    output = 'selected_electrons',
    input_objects = 'electrons',
    filter_func = lambda ptc: ptc.pt()>100 and ptc.iso.sumpt/ptc.pt()<0.4

)

# merge electrons and muons into a single lepton collection
from heppy.analyzers.Merger import Merger
selected_leptons = cfg.Analyzer(
      Merger,
      instance_label = 'selected_leptons', 
      inputs = ['selected_electrons','selected_muons'],
      output = 'selected_leptons'
)


# select pf04 jets above 700 GeV for b-tagging
jets_pf04 = cfg.Analyzer(
    Selector,
    'jets_pf04',
    output = 'jets_pf04',
    input_objects = 'pfjets04',
    filter_func = lambda jet: jet.pt()>700
)

from heppy.analyzers.Matcher import Matcher
match_lepton_jets = cfg.Analyzer(
    Matcher,
    'lepton_jets',
    delta_r = 0.2,
    match_particles = 'selected_leptons',
    particles = 'jets_pf04'
)


jets_nolepton = cfg.Analyzer(
    Selector,
    'jets_nolepton',
    output = 'jets_nolepton',
    input_objects = 'jets_pf04',
    filter_func = lambda jet: jet.match is None
    #filter_func = lambda jet: 1

)



from heppy.FCChhAnalyses.analyzers.FlavourTagger import FlavourTagger
jets_pf04_trf = cfg.Analyzer(
    FlavourTagger,
    'jets_pf04_trf',
    input_jets = 'jets_nolepton',
    input_genparticles = 'gen_particles',
    output_jets = 'jets_pf04_trf',
    dr_match = 0.4,
    ptr_min = 0.15,
    pdg_tags = [15, 11, 0],
    )

from heppy.FCChhAnalyses.analyzers.FlavourReweighter import FlavourReweighter
jets_pf04_rew = cfg.Analyzer(
    FlavourReweighter,
    'jets_pf04_rew',
    input_jets = 'jets_nolepton',
    output_jets = 'jets_pf04_rew',
    tag_rates = [[15,0.7], [11,0.2], [0,0.1]],
    )



# store interesting quantities into flat ROOT tree
from heppy.FCChhAnalyses.FCChh.Zprime_tautau.TreeProducer import TreeProducer
reco_tree = cfg.Analyzer(
    TreeProducer,
    jets_pf04_trf  = 'jets_pf04_trf',
    leptons='selected_leptons',
    met='met',
)




# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence( [
    source,
    selected_muons,
    selected_electrons,
    selected_leptons,
    jets_pf04,
    match_lepton_jets,
    jets_nolepton,
    jets_pf04_trf,
    #jets_pf04_rew,
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
