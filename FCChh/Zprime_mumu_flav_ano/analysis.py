import os
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
    files = ["/eos/experiment/fcc/hh/generation/DelphesEvents/fcc_v02/mgp8_pp_Zprime_mumu_5f_Mzp_10TeV/events_000000095.root"]
)

selectedComponents = [
                        sample.mgp8_pp_Zprime_mumu_5f_Mzp_4TeV,
                        sample.mgp8_pp_Zprime_mumu_5f_Mzp_6TeV,
                        sample.mgp8_pp_Zprime_mumu_5f_Mzp_8TeV,
                        sample.mgp8_pp_Zprime_mumu_5f_Mzp_10TeV,
                        sample.mgp8_pp_Zprime_mumu_5f_Mzp_12TeV,
                        sample.mgp8_pp_Zprime_mumu_5f_Mzp_14TeV,
                        sample.mgp8_pp_Zprime_mumu_5f_Mzp_15TeV,
                        sample.mgp8_pp_Zprime_mumu_5f_Mzp_16TeV,
                        sample.mgp8_pp_Zprime_mumu_5f_Mzp_18TeV,
                        sample.mgp8_pp_Zprime_mumu_5f_Mzp_20TeV,
                        sample.mgp8_pp_Zprime_mumu_5f_Mzp_25TeV,
                        sample.mgp8_pp_Zprime_mumu_5f_Mzp_30TeV,
                        sample.mgp8_pp_Zprime_mumu_5f_Mzp_35TeV,
                        sample.mgp8_pp_Zprime_mumu_5f_Mzp_40TeV,
                        sample.mgp8_pp_Zprime_mumu_5f_Mzp_45TeV,
                        sample.mgp8_pp_LQ_mumu_5f_MLQ_4TeV,
                        sample.mgp8_pp_LQ_mumu_5f_MLQ_6TeV,
                        sample.mgp8_pp_LQ_mumu_5f_MLQ_8TeV,
                        sample.mgp8_pp_LQ_mumu_5f_MLQ_10TeV,
                        sample.mgp8_pp_LQ_mumu_5f_MLQ_12TeV,
                        sample.mgp8_pp_LQ_mumu_5f_MLQ_14TeV,
                        sample.mgp8_pp_LQ_mumu_5f_MLQ_16TeV,
                        sample.mgp8_pp_LQ_mumu_5f_MLQ_18TeV,
                        sample.mgp8_pp_LQ_mumu_5f_MLQ_20TeV,
                        sample.mgp8_pp_LQ_mumu_5f_MLQ_22TeV,
                        sample.mgp8_pp_LQ_mumu_5f_MLQ_24TeV,
                        sample.mgp8_pp_LQ_mumu_5f_MLQ_26TeV,
                        sample.mgp8_pp_LQ_mumu_5f_MLQ_28TeV,
                        sample.mgp8_pp_LQ_mumu_5f_MLQ_30TeV,
                        sample.mgp8_pp_LQ_mumu_5f_MLQ_32TeV,
                        sample.mgp8_pp_LQ_mumu_5f_MLQ_34TeV,
                        sample.mgp8_pp_LQ_mumu_5f_MLQ_36TeV,
                        sample.mgp8_pp_LQ_mumu_5f_MLQ_38TeV,
                        sample.mgp8_pp_LQ_mumu_5f_MLQ_40TeV,
                        sample.mgp8_pp_mumu_5f_HT_500_1000,
                        sample.mgp8_pp_mumu_5f_HT_1000_2000,
                        sample.mgp8_pp_mumu_5f_HT_2000_5000,
                        sample.mgp8_pp_mumu_5f_HT_5000_10000,
                        sample.mgp8_pp_mumu_5f_HT_10000_27000,
                        sample.mgp8_pp_mumu_5f_HT_27000_100000,
                     ]

splitFac = 10
sample.mgp8_pp_Zprime_mumu_5f_Mzp_4TeV.splitFactor  = splitFac
sample.mgp8_pp_Zprime_mumu_5f_Mzp_6TeV.splitFactor  = splitFac
sample.mgp8_pp_Zprime_mumu_5f_Mzp_8TeV.splitFactor  = splitFac
sample.mgp8_pp_Zprime_mumu_5f_Mzp_10TeV.splitFactor = splitFac
sample.mgp8_pp_Zprime_mumu_5f_Mzp_12TeV.splitFactor = splitFac
sample.mgp8_pp_Zprime_mumu_5f_Mzp_14TeV.splitFactor = splitFac
sample.mgp8_pp_Zprime_mumu_5f_Mzp_15TeV.splitFactor = splitFac
sample.mgp8_pp_Zprime_mumu_5f_Mzp_16TeV.splitFactor = splitFac
sample.mgp8_pp_Zprime_mumu_5f_Mzp_18TeV.splitFactor = splitFac
sample.mgp8_pp_Zprime_mumu_5f_Mzp_20TeV.splitFactor = splitFac
sample.mgp8_pp_Zprime_mumu_5f_Mzp_25TeV.splitFactor = splitFac
sample.mgp8_pp_Zprime_mumu_5f_Mzp_30TeV.splitFactor = splitFac
sample.mgp8_pp_Zprime_mumu_5f_Mzp_35TeV.splitFactor = splitFac
sample.mgp8_pp_Zprime_mumu_5f_Mzp_40TeV.splitFactor = splitFac
sample.mgp8_pp_Zprime_mumu_5f_Mzp_45TeV.splitFactor = splitFac
sample.mgp8_pp_LQ_mumu_5f_MLQ_4TeV.splitFactor  = splitFac
sample.mgp8_pp_LQ_mumu_5f_MLQ_6TeV.splitFactor  = splitFac
sample.mgp8_pp_LQ_mumu_5f_MLQ_8TeV.splitFactor  = splitFac
sample.mgp8_pp_LQ_mumu_5f_MLQ_10TeV.splitFactor = splitFac
sample.mgp8_pp_LQ_mumu_5f_MLQ_12TeV.splitFactor = splitFac
sample.mgp8_pp_LQ_mumu_5f_MLQ_14TeV.splitFactor = splitFac
sample.mgp8_pp_LQ_mumu_5f_MLQ_16TeV.splitFactor = splitFac
sample.mgp8_pp_LQ_mumu_5f_MLQ_18TeV.splitFactor = splitFac
sample.mgp8_pp_LQ_mumu_5f_MLQ_20TeV.splitFactor = splitFac
sample.mgp8_pp_LQ_mumu_5f_MLQ_22TeV.splitFactor = splitFac
sample.mgp8_pp_LQ_mumu_5f_MLQ_24TeV.splitFactor = splitFac
sample.mgp8_pp_LQ_mumu_5f_MLQ_26TeV.splitFactor = splitFac
sample.mgp8_pp_LQ_mumu_5f_MLQ_28TeV.splitFactor = splitFac
sample.mgp8_pp_LQ_mumu_5f_MLQ_30TeV.splitFactor = splitFac
sample.mgp8_pp_LQ_mumu_5f_MLQ_32TeV.splitFactor = splitFac
sample.mgp8_pp_LQ_mumu_5f_MLQ_34TeV.splitFactor = splitFac
sample.mgp8_pp_LQ_mumu_5f_MLQ_36TeV.splitFactor = splitFac
sample.mgp8_pp_LQ_mumu_5f_MLQ_38TeV.splitFactor = splitFac
sample.mgp8_pp_LQ_mumu_5f_MLQ_40TeV.splitFactor = splitFac

splitFac2 = 60
sample.mgp8_pp_mumu_5f_HT_500_1000.splitFactor     = splitFac2
sample.mgp8_pp_mumu_5f_HT_1000_2000.splitFactor    = splitFac2
sample.mgp8_pp_mumu_5f_HT_2000_5000.splitFactor    = splitFac2
sample.mgp8_pp_mumu_5f_HT_5000_10000.splitFactor   = splitFac2
sample.mgp8_pp_mumu_5f_HT_10000_27000.splitFactor  = splitFac2
sample.mgp8_pp_mumu_5f_HT_27000_100000.splitFactor = splitFac2

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


# select isolated muons with pT > 50 GeV and relIso < 0.4
from heppy.analyzers.Selector import Selector
selected_muons = cfg.Analyzer(
    Selector,
    'selected_muons',
    output = 'selected_muons',
    input_objects = 'muons',
    filter_func = lambda ptc: ptc.pt()>50 and ptc.iso.sumpt/ptc.pt()<0.4
    #filter_func = lambda ptc: ptc.pt()>5

)

# select electrons with pT > 50 GeV and relIso < 0.4
selected_electrons = cfg.Analyzer(
    Selector,
    'selected_electrons',
    output = 'selected_electrons',
    input_objects = 'electrons',
    filter_func = lambda ptc: ptc.pt()>50 and ptc.iso.sumpt/ptc.pt()<0.4
    #filter_func = lambda ptc: ptc.pt()>5

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



from heppy.FCChhAnalyses.FCChh.Zprime_mumu_flav_ano.selection import Selection
selection = cfg.Analyzer(
    Selection,
    instance_label='cuts'
)

# create Z' boson candidates
from heppy.FCChhAnalyses.analyzers.ResonanceBuilder import ResonanceBuilder
zprime_ele = cfg.Analyzer(
      ResonanceBuilder,
      output = 'zprime_ele',
      leg_collection = 'selected_electrons',
      pdgid = 32
)

# create Z' boson candidates
from heppy.FCChhAnalyses.analyzers.ResonanceBuilder import ResonanceBuilder
zprime_muon = cfg.Analyzer(
      ResonanceBuilder,
      output = 'zprime_muon',
      leg_collection = 'selected_muons',
      pdgid = 32
)

# apply event selection. 
from heppy.FCChhAnalyses.FCChh.Zprime_mumu_flav_ano.selection import Selection
selection = cfg.Analyzer(
    Selection,
    instance_label='cuts'
)

# store interesting quantities into flat ROOT tree
from heppy.FCChhAnalyses.FCChh.Zprime_mumu_flav_ano.TreeProducer import TreeProducer
reco_tree = cfg.Analyzer(
    TreeProducer,
    jets='jets_nolepton',
    leptons='selected_leptons',
    met='met',
    zprime_ele='zprime_ele',
    zprime_muon='zprime_muon',

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
    selection,
    zprime_ele,
    zprime_muon,
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
