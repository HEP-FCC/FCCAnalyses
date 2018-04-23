import os, sys
import copy, math
import heppy.framework.config as cfg
import logging

# next 2 lines necessary to deal with reimports from ipython
logging.shutdown()
reload(logging)
logging.basicConfig(level=logging.WARNING)

sys.path.append('/afs/cern.ch/work/h/helsens/public/FCCDicts/')

comp = cfg.Component(
    'example',
     files = ["/eos/experiment/fcc/hh/generation/DelphesEvents/fcc_v02/mgp8_pp_hhj_lambda100_5f_hhbbbb/events_000000486.root"]
)

from FCC_heppySampleList_fcc_v02 import *

selectedComponents = [
                       mgp8_pp_hhj_lambda050_5f_hhbbbb,
                       mgp8_pp_hhj_lambda090_5f_hhbbbb,
                       mgp8_pp_hhj_lambda095_5f_hhbbbb,
                       mgp8_pp_hhj_lambda100_5f_hhbbbb,
                       mgp8_pp_hhj_lambda105_5f_hhbbbb,
                       mgp8_pp_hhj_lambda110_5f_hhbbbb,
                       mgp8_pp_hhj_lambda150_5f_hhbbbb,
                       mgp8_pp_hhj_lambda200_5f_hhbbbb,
                       mgp8_pp_bbbbj_QCD,
                       mgp8_pp_bbbbj_QCDQED,
                       mgp8_pp_bbbbj_QED,
                       ]

mgp8_pp_hhj_lambda050_5f_hhbbbb.splitFactor = 60
mgp8_pp_hhj_lambda090_5f_hhbbbb.splitFactor = 60
mgp8_pp_hhj_lambda095_5f_hhbbbb.splitFactor = 60
mgp8_pp_hhj_lambda100_5f_hhbbbb.splitFactor = 60
mgp8_pp_hhj_lambda105_5f_hhbbbb.splitFactor = 60
mgp8_pp_hhj_lambda110_5f_hhbbbb.splitFactor = 60
mgp8_pp_hhj_lambda150_5f_hhbbbb.splitFactor = 60
mgp8_pp_hhj_lambda200_5f_hhbbbb.splitFactor = 60
mgp8_pp_bbbbj_QCD.splitFactor = 130
mgp8_pp_bbbbj_QCDQED.splitFactor = 130
mgp8_pp_bbbbj_QED.splitFactor = 50

#selectedComponents = [comp]

from heppy.analyzers.fcc.Reader import Reader
source = cfg.Analyzer(
    Reader,

    weights = 'mcEventWeights',

    gen_particles = 'skimmedGenParticles',
    
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
   
    #fatjets = 'fatjets',
    pfjets08 = 'pfjets08',
    pfjetsOneSubJettiness08 = 'pfjetsOneSubJettiness08', 
    pfjetsTwoSubJettiness08 = 'pfjetsTwoSubJettiness08', 
    pfjetsThreeSubJettiness08 = 'pfjetsThreeSubJettiness08', 
    pfsubjetsSoftDropTagged08 = 'pfsubjetsSoftDropTagged08', 
    pfsubjetsSoftDrop08 = 'pfsubjetsSoftDrop08', 

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
gen_bs = cfg.Analyzer(
    Selector,
    'gen_bs',
    output = 'gen_bs',
    input_objects = 'gen_particles',
    filter_func = lambda ptc: (abs(ptc.pdgid()) == 5 and ptc.pt() > 50.)
)

# produce flat root tree containing information about stable leptons in the event
from heppy.FCChhAnalyses.FCChh.hh_boosted.GenTreeProducer import GenTreeProducer
gen_tree = cfg.Analyzer(
    GenTreeProducer,
    gen_higgses = 'gen_higgses',
)

#############################
##   Reco Level Analysis   ##
#############################

from heppy.analyzers.Selector import Selector
# select jet above 200 GeV
fatjets_200 = cfg.Analyzer(
    Selector,
    'fatjets_200',
    output = 'fatjets_200',
    input_objects = 'pfjets08',
    filter_func = lambda jet: jet.pt()>200.
)

# produce flat root tree containing jet substructure information
from heppy.FCChhAnalyses.FCChh.hh_boosted.TreeProducer import TreeProducer
reco_tree = cfg.Analyzer(
    TreeProducer,
    gen_bs = 'gen_bs',
    gen_higgses = 'gen_higgses',
    fatjets = 'fatjets_200',
)


# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence( [
    source,
    gen_higgses,
    gen_bs,
    #gen_tree,
    fatjets_200,
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
