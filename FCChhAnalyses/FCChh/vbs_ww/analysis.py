from common_defaults import deffccdicts

import os, sys
import copy
import heppy.framework.config as cfg
import logging

# next 2 lines necessary to deal with reimports from ipython
logging.shutdown()
reload(logging)
logging.basicConfig(level=logging.WARNING)

sys.path.append(os.path.join(os.getenv('FCCDICTSDIR', deffccdicts), '') + '')

comp = cfg.Component(
    'example',
     files = ["/eos/experiment/fcc/hh/generation/DelphesEvents/fcc_v02/mgp8_pp_vbs_wwss_kw_090_TT/events_200758428.root"]
)

from FCC_heppySampleList_fcc_v02 import *

selectedComponents = [
                       mgp8_pp_wz012j_4f_wzlllv,
		       mgp8_pp_vbs_wwss_kw_050_TT,
		       mgp8_pp_vbs_wwss_kw_050_TL,
		       mgp8_pp_vbs_wwss_kw_050_LL,
		       mgp8_pp_vbs_wwss_kw_070_TT,
		       mgp8_pp_vbs_wwss_kw_070_TL,
		       mgp8_pp_vbs_wwss_kw_070_LL,
		       mgp8_pp_vbs_wwss_kw_080_TT,
		       mgp8_pp_vbs_wwss_kw_080_TL,
		       mgp8_pp_vbs_wwss_kw_080_LL,
		       mgp8_pp_vbs_wwss_kw_090_TT,
		       mgp8_pp_vbs_wwss_kw_090_TL,
		       mgp8_pp_vbs_wwss_kw_090_LL,
		       mgp8_pp_vbs_wwss_kw_090_TT,
		       mgp8_pp_vbs_wwss_kw_090_TL,
		       mgp8_pp_vbs_wwss_kw_090_LL,
		       mgp8_pp_vbs_wwss_kw_095_TT,
		       mgp8_pp_vbs_wwss_kw_095_TL,
		       mgp8_pp_vbs_wwss_kw_095_LL,
                       mgp8_pp_vbs_wwss_kw_100_TT,
		       mgp8_pp_vbs_wwss_kw_100_TL,
		       mgp8_pp_vbs_wwss_kw_100_LL,
		       mgp8_pp_vbs_wwss_kw_102_TT,
		       mgp8_pp_vbs_wwss_kw_102_TL,
		       mgp8_pp_vbs_wwss_kw_102_LL,
		       mgp8_pp_vbs_wwss_kw_105_TT,
		       mgp8_pp_vbs_wwss_kw_105_TL,
		       mgp8_pp_vbs_wwss_kw_105_LL,
		       mgp8_pp_vbs_wwss_kw_110_TT,
		       mgp8_pp_vbs_wwss_kw_110_TL,
		       mgp8_pp_vbs_wwss_kw_110_LL,
		       mgp8_pp_vbs_wwss_kw_120_TT,
		       mgp8_pp_vbs_wwss_kw_120_TL,
		       mgp8_pp_vbs_wwss_kw_120_LL,
		       mgp8_pp_vbs_wwss_kw_130_TT,
		       mgp8_pp_vbs_wwss_kw_130_TL,
		       mgp8_pp_vbs_wwss_kw_130_LL,
		       mgp8_pp_vbs_wwss_kw_150_TT,
		       mgp8_pp_vbs_wwss_kw_150_TL,
		       mgp8_pp_vbs_wwss_kw_150_LL,
                     ]


mgp8_pp_wz012j_4f_wzlllv.splitFactor = 150
mgp8_pp_vbs_wwss_kw_050_TT.splitFactor = 10
mgp8_pp_vbs_wwss_kw_050_TL.splitFactor = 6
mgp8_pp_vbs_wwss_kw_050_LL.splitFactor = 4
mgp8_pp_vbs_wwss_kw_070_TT.splitFactor = 7
mgp8_pp_vbs_wwss_kw_070_TL.splitFactor = 4
mgp8_pp_vbs_wwss_kw_070_LL.splitFactor = 1
mgp8_pp_vbs_wwss_kw_080_TT.splitFactor = 6
mgp8_pp_vbs_wwss_kw_080_TL.splitFactor = 3
mgp8_pp_vbs_wwss_kw_080_LL.splitFactor = 1
mgp8_pp_vbs_wwss_kw_090_TT.splitFactor = 5
mgp8_pp_vbs_wwss_kw_090_TL.splitFactor = 3
mgp8_pp_vbs_wwss_kw_090_LL.splitFactor = 1
mgp8_pp_vbs_wwss_kw_095_TT.splitFactor = 3
mgp8_pp_vbs_wwss_kw_095_TL.splitFactor = 4
mgp8_pp_vbs_wwss_kw_095_LL.splitFactor = 1
mgp8_pp_vbs_wwss_kw_100_TT.splitFactor = 35
mgp8_pp_vbs_wwss_kw_100_TL.splitFactor = 1
mgp8_pp_vbs_wwss_kw_100_LL.splitFactor = 4
mgp8_pp_vbs_wwss_kw_102_TT.splitFactor = 35
mgp8_pp_vbs_wwss_kw_102_TL.splitFactor = 20
mgp8_pp_vbs_wwss_kw_102_LL.splitFactor = 5
mgp8_pp_vbs_wwss_kw_105_TT.splitFactor = 35
mgp8_pp_vbs_wwss_kw_105_TL.splitFactor = 20
mgp8_pp_vbs_wwss_kw_105_LL.splitFactor = 5
mgp8_pp_vbs_wwss_kw_110_TT.splitFactor = 30
mgp8_pp_vbs_wwss_kw_110_TL.splitFactor = 20
mgp8_pp_vbs_wwss_kw_110_LL.splitFactor = 5
mgp8_pp_vbs_wwss_kw_120_TT.splitFactor = 6
mgp8_pp_vbs_wwss_kw_120_TL.splitFactor = 5
mgp8_pp_vbs_wwss_kw_120_LL.splitFactor = 1
mgp8_pp_vbs_wwss_kw_130_TT.splitFactor = 10
mgp8_pp_vbs_wwss_kw_130_TL.splitFactor = 7
mgp8_pp_vbs_wwss_kw_130_LL.splitFactor = 3
mgp8_pp_vbs_wwss_kw_150_TT.splitFactor = 20
mgp8_pp_vbs_wwss_kw_150_TL.splitFactor = 10
mgp8_pp_vbs_wwss_kw_150_LL.splitFactor = 10


#selectedComponents = [comp]


from FCChhAnalyses.analyzers.Reader import Reader
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

# select jet above 20 GeV
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

from FCChhAnalyses.FCChh.vbs_ww.selection import Selection
selected_bs = cfg.Analyzer(
    Selector,
    'selected_bs',
    output = 'selected_bs',
    input_objects = 'jets_nolepton',
    filter_func = lambda ptc: ptc.tags['bf'] > 0
)

selected_lights = cfg.Analyzer(
    Selector,
    'selected_lights',
    output = 'selected_lights',
    input_objects = 'jets_nolepton',
    filter_func = lambda ptc: ptc.tags['bf'] == 0
)

# create H boson candidates with bs
from heppy.FCChhAnalyses.analyzers.LeptonicHiggsBuilder import LeptonicHiggsBuilder
higgses = cfg.Analyzer(
      LeptonicHiggsBuilder,
      output = 'higgses',
      leptons = 'selected_leptons',
      pdgid = 25
)

selection = cfg.Analyzer(
    Selection,
    instance_label='cuts'
)

# store interesting quantities into flat ROOT tree
from FCChhAnalyses.FCChh.vbs_ww.TreeProducer import TreeProducer
reco_tree = cfg.Analyzer(
    TreeProducer,
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
    selected_bs,
    selected_lights,
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
