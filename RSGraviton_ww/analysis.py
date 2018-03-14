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
     #files = ["/eos/experiment/fcc/hh/generation/DelphesEvents/fcc_v02/p8_pp_jj_lo_tagger/events_001556815.root"]
     files = ["/eos/experiment/fcc/hh/generation/DelphesEvents/fcc_v02/p8_pp_RSGraviton_20TeV_ww_tagger/events_002015707.root"]
)

selectedComponents = [
			sample.p8_pp_RSGraviton_10TeV_ww,
			sample.p8_pp_RSGraviton_15TeV_ww,
			sample.p8_pp_RSGraviton_20TeV_ww,
			sample.p8_pp_RSGraviton_25TeV_ww,
			sample.p8_pp_RSGraviton_30TeV_ww,
			sample.p8_pp_RSGraviton_35TeV_ww,
                        sample.mgp8_pp_jj_lo,
                        sample.mgp8_pp_tt_lo,
                        sample.mgp8_pp_vv_lo,
                        sample.mgp8_pp_vj_4f_M_5000_inf,
                        #sample.p8_pp_RSGraviton_20TeV_ww_qcdBDTtrain,
                        #sample.mgp8_pp_jj_lo_filter_pTjet7_5TeV,
		     ]


splitFac = 20
sample.p8_pp_RSGraviton_10TeV_ww.splitFactor = splitFac
sample.p8_pp_RSGraviton_15TeV_ww.splitFactor = splitFac
sample.p8_pp_RSGraviton_20TeV_ww.splitFactor = splitFac
sample.p8_pp_RSGraviton_25TeV_ww.splitFactor = splitFac
sample.p8_pp_RSGraviton_30TeV_ww.splitFactor = splitFac
sample.p8_pp_RSGraviton_35TeV_ww.splitFactor = splitFac
sample.p8_pp_RSGraviton_40TeV_ww.splitFactor = splitFac
sample.mgp8_pp_jj_lo.splitFactor = 350
sample.mgp8_pp_tt_lo.splitFactor = 80
sample.mgp8_pp_vv_lo.splitFactor = 80
sample.mgp8_pp_vj_4f_M_5000_inf.splitFactor = 80
comp.splitFactor = 10
#sample.p8_pp_RSGraviton_20TeV_ww_qcdBDTtrain.splitFactor = 10
#sample.mgp8_pp_jj_lo_filter_pTjet7_5TeV.splitFactor = 10

#selectedComponents = [comp]

from heppy.FCChhAnalyses.analyzers.Reader import Reader
source = cfg.Analyzer(
    Reader,

    weights = 'mcEventWeights',
    

    electrons = 'electrons',
    muons = 'muons',

    #main jets trk02
    trkjets02  = 'trkjets02',
    trkbTags02 = 'trkbTags02',

    trkjetsOneSubJettiness02    = 'trkjetsOneSubJettiness02',
    trkjetsTwoSubJettiness02    = 'trkjetsTwoSubJettiness02',
    trkjetsThreeSubJettiness02  = 'trkjetsThreeSubJettiness02',
    trksubjetsSoftDropTagged02  = 'trksubjetsSoftDropTagged02',
    trksubjetsSoftDrop02        = 'trksubjetsSoftDrop02',
    #
    trksubjetsSoftDropTagged04  = 'trksubjetsSoftDropTagged04',
    trksubjetsSoftDrop04        = 'trksubjetsSoftDrop04',
    trksubjetsSoftDropTagged08  = 'trksubjetsSoftDropTagged08',
    trksubjetsSoftDrop08        = 'trksubjetsSoftDrop08',
  
    #pf jets pf02 for correction
    pfjets02  = 'pfjets02',
    pfbTags02 = 'pfbTags02',

    pfjetsOneSubJettiness02    = 'pfjetsOneSubJettiness02',
    pfjetsTwoSubJettiness02    = 'pfjetsTwoSubJettiness02',
    pfjetsThreeSubJettiness02  = 'pfjetsThreeSubJettiness02',
    pfsubjetsSoftDropTagged02  = 'pfsubjetsSoftDropTagged02',
    pfsubjetsSoftDrop02        = 'pfsubjetsSoftDrop02',


    # used for b-tagging
    pfjets04  = 'pfjets04',
    pfbTags04 = 'pfbTags04',

    # used for mreco
    pfjets08  = 'pfjets08',
    pfbTags08 = 'pfbTags08',
    pfjetConst08 = 'pfjetConst08',

    trkjets04  = 'trkjets04',
    trkjets08  = 'trkjets08',
    trkjetConst08 = 'trkjetConst08',

    electronITags = 'electronITags',
    electronsToMC = 'electronsToMC',


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



from heppy.analyzers.Selector import Selector
# select pf02 jets above 1500 GeV
jets_pf02_1500 = cfg.Analyzer(
    Selector,
    'jets_pf02_1500',
    output = 'jets_pf02_1500',
    input_objects = 'pfjets02',
    filter_func = lambda fatjet: fatjet.pt()>1500.
)

jets_trk02_1000 = cfg.Analyzer(
    Selector,
    'jets_trk02_1000',
    output = 'jets_trk02_1000',
    input_objects = 'trkjets02',
    filter_func = lambda jet: jet.pt()>1000
)

jets_trk04_1000 = cfg.Analyzer(
    Selector,
    'jets_trk04_1000',
    output = 'jets_trk04_1000',
    input_objects = 'trkjets04',
    filter_func = lambda jet: jet.pt()>1000
)

jets_trk08_1000 = cfg.Analyzer(
    Selector,
    'jets_trk08_1000',
    output = 'jets_trk08_1000',
    input_objects = 'trkjets08',
    filter_func = lambda jet: jet.pt()>1000
)


# select pf04 jets above 1000 GeV for b-tagging
jets_pf04_1000 = cfg.Analyzer(
    Selector,
    'jets_pf04_1000',
    output = 'jets_pf04_1000',
    input_objects = 'pfjets04',
    filter_func = lambda jet: jet.pt()>1000
)

# select pf04 jets above 1500 GeV for jet correction
jets_pf04_1500 = cfg.Analyzer(
    Selector,
    'jets_pf04_1500',
    output = 'jets_pf04_1500',
    input_objects = 'pfjets04',
    filter_func = lambda jet: jet.pt()>1500
)

# select pf08 jets above 1500 GeV
jets_pf08_1500 = cfg.Analyzer(
    Selector,
    'jets_pf08_1500',
    output = 'jets_pf08_1500',
    input_objects = 'pfjets08',
    filter_func = lambda jet: jet.pt()>1500
)

# select electrons above 500 GeV
electrons_500 = cfg.Analyzer(
    Selector,
    'electrons_500',
    output = 'electrons_500',
    input_objects = 'electrons',
    filter_func = lambda electron: electron.pt()>500. and electron.iso.sumpt/electron.pt()<0.4

)

# select muons above 500 GeV
muons_500 = cfg.Analyzer(
    Selector,
    'muons_500',
    output = 'muons_500',
    input_objects = 'muons',
    filter_func = lambda muon: muon.pt()>500. and muon.iso.sumpt/muon.pt()<0.4
)

# produce flat root tree containing jet substructure information
from heppy.FCChhAnalyses.RSGraviton_ww.TreeProducer import TreeProducer
tree = cfg.Analyzer(
    TreeProducer,
    jets_trk02_1000 = 'jets_trk02_1000',
    jets_trk04_1000 = 'jets_trk04_1000',
    jets_trk08_1000 = 'jets_trk08_1000',

    jets_pf02_1500  = 'jets_pf02_1500',
    jets_pf04_1000  = 'jets_pf04_1000',
    jets_pf04_1500  = 'jets_pf04_1500',
    jets_pf08_1500  = 'jets_pf08_1500',

    electrons = 'electrons_500',
    muons = 'muons_500',
)


# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence( [
    source,
    jets_pf02_1500,
    jets_pf04_1000,
    jets_pf04_1500,
    jets_pf08_1500,

    jets_trk02_1000,
    jets_trk04_1000,
    jets_trk08_1000,

    electrons_500,
    muons_500,
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
