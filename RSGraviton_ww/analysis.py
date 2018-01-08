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

from heppySampleList_fcc_v02 import *

selectedComponents = [
#			pp_RSGraviton_2TeV_ww,
#			pp_RSGraviton_5TeV_ww,
			pp_RSGraviton_10TeV_ww,
#			pp_RSGraviton_15TeV_ww,
			pp_RSGraviton_20TeV_ww,
#			pp_RSGraviton_25TeV_ww,
#			pp_RSGraviton_30TeV_ww,
#			pp_RSGraviton_35TeV_ww,
#			pp_RSGraviton_40TeV_ww,

                        pp_tt_Pt2500toInf,
                        pp_jj_Pt2500toInf,
                        pp_vv_Pt2500toInf,
                        pp_ll_Pt5000toInf,

#			pp_jj012j_5f_HT_0_500,
#			pp_jj012j_5f_HT_500_1000,
#			pp_jj012j_5f_HT_1000_2000,
#			pp_jj012j_5f_HT_2000_4000,
#			pp_jj012j_5f_HT_4000_7200,
#			pp_jj012j_5f_HT_7200_15000,
#			pp_jj012j_5f_HT_15000_25000,
#			pp_jj012j_5f_HT_25000_35000,
#			pp_jj012j_5f_HT_35000_100000,
#			pp_tt012j_5f_HT_0_600,
#			pp_tt012j_5f_HT_600_1200,
#			pp_tt012j_5f_HT_1200_2100,
#			pp_tt012j_5f_HT_2100_3400,
#			pp_tt012j_5f_HT_3400_5300,
#			pp_tt012j_5f_HT_5300_8100,
#			pp_tt012j_5f_HT_8100_15000,
#			pp_tt012j_5f_HT_15000_25000,
#			pp_tt012j_5f_HT_25000_35000,
#			pp_tt012j_5f_HT_35000_100000,
#			pp_vv012j_4f_HT_0_300,
#			pp_vv012j_4f_HT_300_1400,
#			pp_vv012j_4f_HT_1400_2900,
#			pp_vv012j_4f_HT_2900_5300,
#			pp_vv012j_4f_HT_5300_8800,
#			pp_vv012j_4f_HT_8800_15000,
#			pp_vv012j_4f_HT_15000_25000,
#			pp_vv012j_4f_HT_25000_35000,
#			pp_vv012j_4f_HT_35000_100000,
		     ]


#pp_RSGraviton_2TeV_ww.splitFactor = 10
#pp_RSGraviton_5TeV_ww.splitFactor = 10
pp_RSGraviton_10TeV_ww.splitFactor = 10
#pp_RSGraviton_15TeV_ww.splitFactor = 10
pp_RSGraviton_20TeV_ww.splitFactor = 10
#pp_RSGraviton_25TeV_ww.splitFactor = 10
#pp_RSGraviton_30TeV_ww.splitFactor = 10
#pp_RSGraviton_35TeV_ww.splitFactor = 10
#pp_RSGraviton_40TeV_ww.splitFactor = 10

#pp_tt012j_5f_HT_0_600.splitFactor = 10
#pp_tt012j_5f_HT_600_1200.splitFactor = 10
#pp_tt012j_5f_HT_1200_2100.splitFactor = 10
#pp_tt012j_5f_HT_2100_3400.splitFactor = 10
#pp_tt012j_5f_HT_3400_5300.splitFactor = 10
#pp_tt012j_5f_HT_5300_8100.splitFactor = 10
#pp_tt012j_5f_HT_8100_15000.splitFactor = 10
#pp_tt012j_5f_HT_15000_25000.splitFactor = 10
#pp_tt012j_5f_HT_25000_35000.splitFactor = 10
#pp_tt012j_5f_HT_35000_100000.splitFactor = 10

#pp_jj012j_5f_HT_0_500.splitFactor = 10
#pp_jj012j_5f_HT_500_1000.splitFactor = 10
#pp_jj012j_5f_HT_1000_2000.splitFactor = 10
#pp_jj012j_5f_HT_2000_4000.splitFactor = 10
#pp_jj012j_5f_HT_4000_7200.splitFactor = 10
#pp_jj012j_5f_HT_7200_15000.splitFactor = 10
#pp_jj012j_5f_HT_15000_25000.splitFactor = 10
#pp_jj012j_5f_HT_25000_35000.splitFactor = 10
#pp_jj012j_5f_HT_35000_100000.splitFactor = 10

#pp_vv012j_4f_HT_0_300.splitFactor = 10
#pp_vv012j_4f_HT_300_1400.splitFactor = 10
#pp_vv012j_4f_HT_1400_2900.splitFactor = 10
#pp_vv012j_4f_HT_2900_5300.splitFactor = 10
#pp_vv012j_4f_HT_5300_8800.splitFactor = 10
#pp_vv012j_4f_HT_8800_15000.splitFactor = 10
#pp_vv012j_4f_HT_15000_25000.splitFactor = 10
#pp_vv012j_4f_HT_25000_35000.splitFactor = 10
#pp_vv012j_4f_HT_35000_100000.splitFactor = 10

#selectedComponents = [comp]

#from heppy.analyzers.fcc.Reader import Reader
#for fcc_v02
from heppy.FCChhAnalyses.Reader import Reader

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
from heppy.FCChhAnalyses.RSGraviton_ww.TreeProducer import TreeProducer
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
