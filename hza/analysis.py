import os, sys
import copy
import heppy.framework.config as cfg

import logging
# next 2 lines necessary to deal with reimports from ipython
logging.shutdown()
reload(logging)
logging.basicConfig(level=logging.WARNING)

sys.path.append('/afs/cern.ch/work/h/helsens/public/FCCDicts/')

comp = cfg.Component(
    'example',
     files = ["root://eospublic.cern.ch//eos/fcc/hh/generation/DelphesEvents/decay/pp_h012j_5f_za/events997.root"]
)

from heppySampleList import *

'''selectedComponents = [
                      pp_h012j_5f_HT_0_100_hlla,
                      pp_h012j_5f_HT_100_400_hlla,
                      pp_h012j_5f_HT_400_1000_hlla,
                      pp_h012j_5f_HT_1000_1900_hlla,
                      pp_h012j_5f_HT_1900_4400_hlla,
                      pp_h012j_5f_HT_4400_8500_hlla,
                      pp_h012j_5f_HT_8500_100000_hlla,
                      pp_h012j_5f_hlla,
                      pp_tth01j_5f_HT_0_1100_hlla,
                      pp_tth01j_5f_HT_1100_2700_hlla,
                      pp_tth01j_5f_HT_2700_4900_hlla,
                      pp_tth01j_5f_HT_4900_8100_hlla,
                      pp_tth01j_5f_HT_8100_100000_hlla,
                      pp_tth01j_5f_hlla,
                      pp_vbf_h01j_5f_HT_0_2000_hlla,
                      pp_vbf_h01j_5f_HT_2000_4000_hlla,
                      pp_vbf_h01j_5f_HT_4000_7200_hlla,
                      pp_vbf_h01j_5f_HT_7200_100000_hlla,
                      pp_vbf_h01j_5f_hlla,
                      pp_vh012j_5f_HT_0_300_hlla,
                      pp_vh012j_5f_HT_300_1400_hlla,
                      pp_vh012j_5f_HT_1400_2900_hlla,
                      pp_vh012j_5f_HT_2900_5300_hlla,
                      pp_vh012j_5f_HT_5300_8800_hlla,
                      pp_vh012j_5f_HT_8800_100000_hlla,
                      pp_vh012j_5f_hlla,
                      pp_llv01j_5f_HT_0_800,
                      pp_llv01j_5f_HT_800_2000,
                      pp_llv01j_5f_HT_2000_4000,
                      pp_llv01j_5f_HT_4000_100000,
                      pp_llv01j_5f,
                      pp_vv012j_5f_HT_0_300,
                      pp_vv012j_5f_HT_300_1400,
                      pp_vv012j_5f_HT_1400_2900,
                      pp_vv012j_5f_HT_2900_5300,
                      pp_vv012j_5f_HT_5300_8800,
                      pp_vv012j_5f_HT_8800_100000,
                      pp_vv012j_5f,
                      pp_tt012j_5f_HT_0_600,
                      pp_tt012j_5f_HT_600_1200,
                      pp_tt012j_5f_HT_1200_2100,
                      pp_tt012j_5f_HT_2100_3400,
                      pp_tt012j_5f_HT_3400_5300,
                      pp_tt012j_5f_HT_5300_8100,
                      pp_tt012j_5f_HT_8100_100000,
                      pp_tt012j_5f,
                      pp_vvv01j_5f_HT_0_1200,
                      pp_vvv01j_5f_HT_1200_3000,
                      pp_vvv01j_5f_HT_3000_6000,
                      pp_vvv01j_5f_HT_6000_100000,
                      pp_vvv01j_5f,
                      ]

#selectedComponents = [comp]

pp_h012j_5f_HT_0_100_hlla.splitFactor = 20
pp_h012j_5f_HT_100_400_hlla.splitFactor = 20
pp_h012j_5f_HT_400_1000_hlla.splitFactor = 20
pp_h012j_5f_HT_1000_1900_hlla.splitFactor = 20
pp_h012j_5f_HT_1900_4400_hlla.splitFactor = 20
pp_h012j_5f_HT_4400_8500_hlla.splitFactor = 20
pp_h012j_5f_HT_8500_100000_hlla.splitFactor = 20
pp_h012j_5f_hlla.splitFactor = 20
pp_tth01j_5f_HT_0_1100_hlla.splitFactor = 20
pp_tth01j_5f_HT_1100_2700_hlla.splitFactor = 20
pp_tth01j_5f_HT_2700_4900_hlla.splitFactor = 20
pp_tth01j_5f_HT_4900_8100_hlla.splitFactor = 20
pp_tth01j_5f_HT_8100_100000_hlla.splitFactor = 20
pp_tth01j_5f_hlla.splitFactor = 20
pp_vbf_h01j_5f_HT_0_2000_hlla.splitFactor = 20
pp_vbf_h01j_5f_HT_2000_4000_hlla.splitFactor = 20
pp_vbf_h01j_5f_HT_4000_7200_hlla.splitFactor = 20
pp_vbf_h01j_5f_HT_7200_100000_hlla.splitFactor = 20
pp_vbf_h01j_5f_hlla.splitFactor = 20
pp_vh012j_5f_HT_0_300_hlla.splitFactor = 20
pp_vh012j_5f_HT_300_1400_hlla.splitFactor = 20
pp_vh012j_5f_HT_1400_2900_hlla.splitFactor = 20
pp_vh012j_5f_HT_2900_5300_hlla.splitFactor = 20
pp_vh012j_5f_HT_5300_8800_hlla.splitFactor = 20
pp_vh012j_5f_HT_8800_100000_hlla.splitFactor = 20
pp_vh012j_5f_hlla.splitFactor = 20
pp_llv01j_5f_HT_0_800.splitFactor = 20
pp_llv01j_5f_HT_800_2000.splitFactor = 20
pp_llv01j_5f_HT_2000_4000.splitFactor = 20
pp_llv01j_5f_HT_4000_100000.splitFactor = 20
pp_llv01j_5f.splitFactor = 20
pp_vv012j_5f_HT_0_300.splitFactor = 20
pp_vv012j_5f_HT_300_1400.splitFactor = 20
pp_vv012j_5f_HT_1400_2900.splitFactor = 20
pp_vv012j_5f_HT_2900_5300.splitFactor = 20
pp_vv012j_5f_HT_5300_8800.splitFactor = 20
pp_vv012j_5f_HT_8800_100000.splitFactor = 20
pp_vv012j_5f.splitFactor = 20
pp_tt012j_5f_HT_0_600.splitFactor = 20
pp_tt012j_5f_HT_600_1200.splitFactor = 20
pp_tt012j_5f_HT_1200_2100.splitFactor = 20
pp_tt012j_5f_HT_2100_3400.splitFactor = 20
pp_tt012j_5f_HT_3400_5300.splitFactor = 20
pp_tt012j_5f_HT_5300_8100.splitFactor = 20
pp_tt012j_5f_HT_8100_100000.splitFactor = 20
pp_tt012j_5f.splitFactor = 20
pp_vvv01j_5f_HT_0_1200.splitFactor = 20
pp_vvv01j_5f_HT_1200_3000.splitFactor = 20
pp_vvv01j_5f_HT_3000_6000.splitFactor = 20
pp_vvv01j_5f_HT_6000_100000.splitFactor = 20
pp_vvv01j_5f.splitFactor = 20
'''
selectedComponents = [comp]

#from heppy.analyzers.fcc.Reader import Reader
#for fcc_v02
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

    jets = 'jets',
    bTags = 'bTags',

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


# select isolated muons with pT > 5 GeV and relIso < 0.4
from heppy.analyzers.Selector import Selector
selected_muons = cfg.Analyzer(
    Selector,
    'selected_muons',
    output = 'selected_muons',
    input_objects = 'muons',
    filter_func = lambda ptc: ptc.pt()>10 and ptc.iso.sumpt/ptc.pt()<0.15
)

# select electrons with pT > 7 GeV and relIso < 0.4
selected_electrons = cfg.Analyzer(
    Selector,
    'selected_electrons',
    output = 'selected_electrons',
    input_objects = 'electrons',
    filter_func = lambda ptc: ptc.pt()>10 and ptc.iso.sumpt/ptc.pt()<0.15
)

# select isolated photons with pT > 35 GeV and relIso < 0.4
from heppy.analyzers.Selector import Selector
selected_photons = cfg.Analyzer(
    Selector,
    'selected_photons',
    output = 'selected_photons',
    input_objects = 'photons',
    filter_func = lambda ptc: ptc.pt()> 15. and ptc.iso.sumpt/ptc.pt()<0.15
)

# merge electrons and muons into a single lepton collection
from heppy.analyzers.Merger import Merger
selected_leptons = cfg.Analyzer(
      Merger,
      instance_label = 'selected_leptons', 
      inputs = ['selected_electrons','selected_muons'],
      output = 'selected_leptons'
)

# create Z boson candidates with leptons
from heppy.FCChhAnalyses.analyzers.LeptonicZedBuilder import LeptonicZedBuilder
zeds = cfg.Analyzer(
      LeptonicZedBuilder,
      output = 'zeds',
      leptons = 'selected_leptons',
)


# store interesting quantities into flat ROOT tree
from heppy.FCChhAnalyses.hza.TreeProducer import TreeProducer
reco_tree = cfg.Analyzer(
    TreeProducer,
    zeds = 'zeds',
    photons = 'selected_photons',
)

# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence( [
    source,
    selected_muons,
    selected_electrons,
    selected_leptons,
    selected_photons,
    zeds,
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
