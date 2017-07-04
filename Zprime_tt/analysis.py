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
     files = ["root://eospublic.cern.ch///eos/fcc/hh/generation/DelphesEvents/fcc_v01/pp_Zprime_5TeV_ttbar/events0.root"]
)

from heppySampleList_fcc_v01 import *

selectedComponents = [
			pp_jj012j_5f_HT_0_500,
			pp_jj012j_5f_HT_500_1000,
			pp_jj012j_5f_HT_1000_2000,
			pp_jj012j_5f_HT_2000_4000,
			pp_jj012j_5f_HT_4000_7200,
			pp_jj012j_5f_HT_7200_15000,
			pp_jj012j_5f_HT_15000_25000,
			pp_jj012j_5f_HT_25000_35000,
			pp_jj012j_5f_HT_35000_100000,
                        pp_Zprime_5TeV_ttbar,
                        pp_Zprime_10TeV_ttbar,
                        pp_Zprime_15TeV_ttbar,
                        pp_Zprime_20TeV_ttbar,
                        pp_Zprime_25TeV_ttbar,
                        pp_Zprime_30TeV_ttbar,
                        pp_Zprime_35TeV_ttbar,
                        pp_Zprime_40TeV_ttbar,  
			pp_tt012j_5f_HT_0_600,
			pp_tt012j_5f_HT_600_1200,
			pp_tt012j_5f_HT_1200_2100,
			pp_tt012j_5f_HT_2100_3400,
			pp_tt012j_5f_HT_3400_5300,
			pp_tt012j_5f_HT_5300_8100,
			pp_tt012j_5f_HT_8100_15000,
			pp_tt012j_5f_HT_15000_25000,
			pp_tt012j_5f_HT_25000_35000,
			pp_tt012j_5f_HT_35000_100000,
		     ]

pp_Zprime_5TeV_ttbar.splitFactor = 5
pp_Zprime_10TeV_ttbar.splitFactor = 5
pp_Zprime_15TeV_ttbar.splitFactor = 5
pp_Zprime_20TeV_ttbar.splitFactor = 5
pp_Zprime_25TeV_ttbar.splitFactor = 5
pp_Zprime_30TeV_ttbar.splitFactor = 5
pp_Zprime_35TeV_ttbar.splitFactor = 5
pp_Zprime_40TeV_ttbar.splitFactor = 5

pp_tt012j_5f_HT_0_600.splitFactor = 5
pp_tt012j_5f_HT_600_1200.splitFactor = 5
pp_tt012j_5f_HT_1200_2100.splitFactor = 5
pp_tt012j_5f_HT_2100_3400.splitFactor = 5
pp_tt012j_5f_HT_3400_5300.splitFactor = 5
pp_tt012j_5f_HT_5300_8100.splitFactor = 5
pp_tt012j_5f_HT_8100_15000.splitFactor = 5
pp_tt012j_5f_HT_15000_25000.splitFactor = 5
pp_tt012j_5f_HT_25000_35000.splitFactor = 5
pp_tt012j_5f_HT_35000_100000.splitFactor = 5

pp_jj012j_5f_HT_0_500.splitFactor = 5
pp_jj012j_5f_HT_500_1000.splitFactor = 5
pp_jj012j_5f_HT_1000_2000.splitFactor = 5
pp_jj012j_5f_HT_2000_4000.splitFactor = 5
pp_jj012j_5f_HT_4000_7200.splitFactor = 5
pp_jj012j_5f_HT_7200_15000.splitFactor = 5
pp_jj012j_5f_HT_15000_25000.splitFactor = 5
pp_jj012j_5f_HT_25000_35000.splitFactor = 5
pp_jj012j_5f_HT_35000_100000.splitFactor = 5

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

)


from ROOT import gSystem
gSystem.Load("libdatamodelDict")
from EventStore import EventStore as Events

#############################
##   Reco Level Analysis   ##
#############################

#uncomment the following to go back to normal

from heppy.analyzers.Selector import Selector
# select jet above 500 GeV
fatjets_500 = cfg.Analyzer(
    Selector,
    'fatjets_500',
    output = 'fatjets_500',
    input_objects = 'fatjets',
    filter_func = lambda jet: jet.pt()>500.
)

# produce flat root tree containing jet substructure information
from heppy.FCChhAnalyses.Zprime_tt.TreeProducer import TreeProducer
tree = cfg.Analyzer(
    TreeProducer,
    fatjets = 'fatjets_500',
)


# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence( [
    source,
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
