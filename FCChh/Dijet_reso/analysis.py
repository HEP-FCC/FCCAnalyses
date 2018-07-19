import os
import copy
import heppy.framework.config as cfg
import sys
import logging
import imp

# next 2 lines necessary to deal with reimports from ipython
logging.shutdown()
reload(logging)
logging.basicConfig(level=logging.WARNING)
sys.path.append('/afs/cern.ch/work/h/helsens/public/FCCDicts/')
comp = cfg.Component(
    'example',
     files = ["/eos/experiment/fcc/hh/generation/DelphesEvents/fcc_v02/p8_pp_ExcitedQ_30TeV_qq/events_113722907.root"]
)

sample=imp.load_source('heppylist', '/afs/cern.ch/work/h/helsens/public/FCCDicts/FCC_heppySampleList_fcc_v02.py')

selectedComponents = [

#    sample.p8_pp_ExcitedQ_15TeV_qq,
#    sample.p8_pp_ExcitedQ_20TeV_qq,
#    sample.p8_pp_ExcitedQ_25TeV_qq,
#    sample.p8_pp_ExcitedQ_30TeV_qq,
#    sample.p8_pp_ExcitedQ_35TeV_qq,
#    sample.p8_pp_ExcitedQ_40TeV_qq,
#    sample.p8_pp_ExcitedQ_45TeV_qq,
#    sample.p8_pp_ExcitedQ_50TeV_qq,

    sample.p8_pp_ZprimeSSM_10TeV_jj,
    sample.p8_pp_ZprimeSSM_15TeV_jj,
    sample.p8_pp_ZprimeSSM_20TeV_jj,
    sample.p8_pp_ZprimeSSM_25TeV_jj,
    sample.p8_pp_ZprimeSSM_30TeV_jj,
    sample.p8_pp_ZprimeSSM_35TeV_jj,
    sample.p8_pp_ZprimeSSM_40TeV_jj,
    sample.p8_pp_ZprimeSSM_45TeV_jj,
    sample.p8_pp_ZprimeSSM_50TeV_jj,


#    sample.mgp8_pp_jj_5f_HT_500_1000,
#    sample.mgp8_pp_jj_5f_HT_1000_2000,
#    sample.mgp8_pp_jj_5f_HT_2000_5000,
#    sample.mgp8_pp_jj_5f_HT_5000_10000,
#    sample.mgp8_pp_jj_5f_HT_10000_27000,
#    sample.mgp8_pp_jj_5f_HT_27000_100000,
                     ]



splitFac = 10
sample.p8_pp_ExcitedQ_15TeV_qq.splitFactor = splitFac
sample.p8_pp_ExcitedQ_20TeV_qq.splitFactor = splitFac
sample.p8_pp_ExcitedQ_25TeV_qq.splitFactor = splitFac
sample.p8_pp_ExcitedQ_30TeV_qq.splitFactor = splitFac
sample.p8_pp_ExcitedQ_35TeV_qq.splitFactor = splitFac
sample.p8_pp_ExcitedQ_40TeV_qq.splitFactor = splitFac
sample.p8_pp_ExcitedQ_45TeV_qq.splitFactor = splitFac
sample.p8_pp_ExcitedQ_50TeV_qq.splitFactor = splitFac

sample.p8_pp_ZprimeSSM_10TeV_jj.splitFactor = splitFac
sample.p8_pp_ZprimeSSM_15TeV_jj.splitFactor = splitFac
sample.p8_pp_ZprimeSSM_20TeV_jj.splitFactor = splitFac
sample.p8_pp_ZprimeSSM_25TeV_jj.splitFactor = splitFac
sample.p8_pp_ZprimeSSM_30TeV_jj.splitFactor = splitFac
sample.p8_pp_ZprimeSSM_35TeV_jj.splitFactor = splitFac
sample.p8_pp_ZprimeSSM_40TeV_jj.splitFactor = splitFac
sample.p8_pp_ZprimeSSM_45TeV_jj.splitFactor = splitFac
sample.p8_pp_ZprimeSSM_50TeV_jj.splitFactor = splitFac

splitFac2 = 60
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
    met = 'met',   

    #main jets trk02
    calojets04  = 'calojets04',
    pfjets04  = 'pfjets04',

)


from ROOT import gSystem
gSystem.Load("libdatamodelDict")
from EventStore import EventStore as Events

#############################
##   Reco Level Analysis   ##
#############################

#uncomment the following to go back to normal

from heppy.analyzers.Selector import Selector
# select pf04 jets above 2000 GeV
jets_pf04_2000 = cfg.Analyzer(
    Selector,
    'jets_pf04_2000',
    output = 'jets_pf04_2000',
    input_objects = 'pfjets04',
    filter_func = lambda jet: jet.pt()>2000.
)

# select calo02 jets above 2000 GeV
jets_calo04_2000 = cfg.Analyzer(
    Selector,
    'jets_calo04_2000',
    output = 'jets_calo04_2000',
    input_objects = 'calojets04',
    filter_func = lambda jet: jet.pt()>2000.
)





# produce flat root tree containing jet substructure information
from heppy.FCChhAnalyses.FCChh.Dijet_reso.TreeProducer import TreeProducer
tree = cfg.Analyzer(
    TreeProducer,
    jets_pf04_2000    = 'jets_pf04_2000',
    jets_calo04_2000  = 'jets_calo04_2000',

)


# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence( [
    source,
    jets_pf04_2000,
    jets_calo04_2000,
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
