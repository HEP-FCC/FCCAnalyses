import os
import copy
import heppy.framework.config as cfg
import sys
import logging
# next 2 lines necessary to deal with reimports from ipython
logging.shutdown()
reload(logging)
logging.basicConfig(level=logging.WARNING)
sys.path.append('/afs/cern.ch/work/h/helsens/public/FCCDicts/')
comp = cfg.Component(
    'example',
     files = ["root://eospublic.cern.ch///eos/fcc/hh/generation/DelphesEvents/fcc_v01/pp_RSGraviton_30TeV_ww/events0.root"]
)

from heppySampleList_fcc_v01 import *

selectedComponents = [
			pp_RSGraviton_5TeV_ww,
			pp_RSGraviton_10TeV_ww,
			pp_RSGraviton_15TeV_ww,
			pp_RSGraviton_20TeV_ww,
			pp_RSGraviton_25TeV_ww,
			pp_RSGraviton_30TeV_ww,
			pp_RSGraviton_35TeV_ww,
			pp_RSGraviton_40TeV_ww,
			pp_jj_M_5000_10000,
			pp_jj_M_10000_15000,
			pp_jj_M_15000_100000,
                        pp_tt_M_5000_10000,
                        pp_tt_M_10000_15000,
                        pp_tt_M_15000_100000,
                        pp_vv_M_5000_10000,
                        pp_vv_M_10000_15000,
                        pp_vv_M_15000_100000,
                        pp_vv_nlo,
			pp_wj_4f_M_5000_inf,
		     ]


pp_RSGraviton_5TeV_ww.splitFactor = 20
pp_RSGraviton_10TeV_ww.splitFactor = 20
pp_RSGraviton_15TeV_ww.splitFactor = 20
pp_RSGraviton_20TeV_ww.splitFactor = 20
pp_RSGraviton_25TeV_ww.splitFactor = 20
pp_RSGraviton_30TeV_ww.splitFactor = 20
pp_RSGraviton_35TeV_ww.splitFactor = 20
pp_RSGraviton_40TeV_ww.splitFactor = 20

pp_jj_M_5000_10000.splitFactor = 100
pp_jj_M_10000_15000.splitFactor = 100
pp_jj_M_15000_100000.splitFactor = 100

pp_tt_M_5000_10000.splitFactor = 10
pp_tt_M_10000_15000.splitFactor = 10
pp_tt_M_15000_100000.splitFactor = 10

pp_vv_M_5000_10000.splitFactor = 10
pp_vv_M_10000_15000.splitFactor = 10
pp_vv_M_15000_100000.splitFactor = 10
pp_vv_nlo.splitFactor = 50

pp_wj_4f_M_5000_inf.splitFactor = 50

#selectedComponents = [comp]

from heppy.analyzers.fcc.Reader import Reader
source = cfg.Analyzer(
    Reader,

    weights = 'mcEventWeights',
    
    fatjets = 'fatjets',
    jetsOneSubJettiness = 'jetsOneSubJettiness', 
    jetsTwoSubJettiness = 'jetsTwoSubJettiness', 
    jetsThreeSubJettiness = 'jetsThreeSubJettiness', 
    subjetsTrimmingTagged = 'subjetsTrimmingTagged', 
    subjetsTrimming = 'subjetsTrimming', 
    subjetsPruningTagged = 'subjetsPruningTagged', 
    subjetsPruning = 'subjetsPruning', 
    subjetsSoftDropTagged = 'subjetsSoftDropTagged', 
    subjetsSoftDrop = 'subjetsSoftDrop', 
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

# select isolated muons with pT > 5 GeV and relIso < 0.4
from heppy.analyzers.Selector import Selector
selected_muons = cfg.Analyzer(
    Selector,
    'selected_muons',
    output = 'selected_muons',
    input_objects = 'muons',
    filter_func = lambda ptc: ptc.pt()>500 and ptc.iso.sumpt/ptc.pt()<0.4
)

# select electrons with pT > 7 GeV and relIso < 0.4
selected_electrons = cfg.Analyzer(
    Selector,
    'selected_electrons',
    output = 'selected_electrons',
    input_objects = 'electrons',
    filter_func = lambda ptc: ptc.pt()>500 and ptc.iso.sumpt/ptc.pt()<0.4
)
'''
# merge electrons and muons into a single lepton collection
from heppy.analyzers.Merger import Merger
selected_leptons = cfg.Analyzer(
      Merger,
      instance_label = 'selected_leptons', 
      inputs = ['selected_electrons','selected_muons'],
      output = 'selected_leptons'
)
'''
fatjets_500 = cfg.Analyzer(
    Selector,
    'fatjets_500',
    output = 'fatjets_500',
    input_objects = 'fatjets',
    filter_func = lambda jet: jet.pt()>500.
)


# select jet above 500 GeV
'''fatjets_500_noclean = cfg.Analyzer(
    Selector,
    'fatjets_500_noclean',
    output = 'fatjets_500_noclean',
    input_objects = 'fatjets',
    filter_func = lambda jet: jet.pt()>2000.
)

from heppy.analyzers.Matcher import Matcher
match_lepton_jets = cfg.Analyzer(
    Matcher,
    'lepton_jets',
    delta_r = 0.8,
    match_particles = 'selected_leptons',
    particles = 'fatjets_500_noclean'
)

fatjets_500 = cfg.Analyzer(
    Selector,
    'fatjets_500',
    output = 'fatjets_500',
    input_objects = 'fatjets_500_noclean',
    filter_func = lambda jet: jet.match is None
)
'''

# produce flat root tree containing jet substructure information
from heppy.FCChhAnalyses.RSGraviton_ww.TreeProducer import TreeProducer
tree = cfg.Analyzer(
    TreeProducer,
    fatjets = 'fatjets_500',
    muons = 'selected_muons',
    electrons = 'selected_electrons',
)


# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence( [
    source,
    selected_muons,
    selected_electrons,
    #selected_leptons,
    #fatjets_500_noclean,
    #match_lepton_jets,
    #jets_nolepton,
    fatjets_500,
    tree,
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
