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
     #files = ["/eos/experiment/fcc/hh/generation/DelphesEvents/fcc_v02/mgp8_pp_hhj_lambda100_5f_hhbbbb/events_000000486.root"]
     files = ["/eos/experiment/fcc/hh/generation/DelphesEvents/fcc_v03/pwp8_pp_hh_lambda098_5f_hhbbbb/events_000021883.root"]

)

from FCC_heppySampleList_fcc_v03 import *

selectedComponents = [
                     mgp8_pp_vbfhh_lambda000_5f_hhbbbb,
                     mgp8_pp_vbfhh_lambda020_5f_hhbbbb,
                     mgp8_pp_vbfhh_lambda040_5f_hhbbbb,
                     mgp8_pp_vbfhh_lambda060_5f_hhbbbb,
                     mgp8_pp_vbfhh_lambda070_5f_hhbbbb,
                     mgp8_pp_vbfhh_lambda080_5f_hhbbbb,
                     mgp8_pp_vbfhh_lambda085_5f_hhbbbb,
                     mgp8_pp_vbfhh_lambda090_5f_hhbbbb,
                     mgp8_pp_vbfhh_lambda092_5f_hhbbbb,
                     mgp8_pp_vbfhh_lambda094_5f_hhbbbb,
                     mgp8_pp_vbfhh_lambda096_5f_hhbbbb,
                     mgp8_pp_vbfhh_lambda097_5f_hhbbbb,
                     mgp8_pp_vbfhh_lambda098_5f_hhbbbb,
                     mgp8_pp_vbfhh_lambda099_5f_hhbbbb,
                     mgp8_pp_vbfhh_lambda100_5f_hhbbbb,
                     mgp8_pp_vbfhh_lambda101_5f_hhbbbb,
                     mgp8_pp_vbfhh_lambda102_5f_hhbbbb,
                     mgp8_pp_vbfhh_lambda103_5f_hhbbbb,
                     mgp8_pp_vbfhh_lambda104_5f_hhbbbb,
                     mgp8_pp_vbfhh_lambda106_5f_hhbbbb,
                     mgp8_pp_vbfhh_lambda108_5f_hhbbbb,
                     mgp8_pp_vbfhh_lambda110_5f_hhbbbb,
                     mgp8_pp_vbfhh_lambda120_5f_hhbbbb,
                     mgp8_pp_vbfhh_lambda130_5f_hhbbbb,
                     mgp8_pp_vbfhh_lambda140_5f_hhbbbb,
                     mgp8_pp_vbfhh_lambda145_5f_hhbbbb,
                     mgp8_pp_vbfhh_lambda150_5f_hhbbbb,
                     mgp8_pp_vbfhh_lambda155_5f_hhbbbb,
                     mgp8_pp_vbfhh_lambda160_5f_hhbbbb,
                     mgp8_pp_vbfhh_lambda170_5f_hhbbbb,
                     mgp8_pp_vbfhh_lambda180_5f_hhbbbb,
                     mgp8_pp_vbfhh_lambda190_5f_hhbbbb,
                     mgp8_pp_vbfhh_lambda200_5f_hhbbbb,
                     mgp8_pp_vbfhh_lambda220_5f_hhbbbb,
                     mgp8_pp_vbfhh_lambda240_5f_hhbbbb,
                     mgp8_pp_vbfhh_lambda260_5f_hhbbbb,
                     mgp8_pp_vbfhh_lambda280_5f_hhbbbb,
                     mgp8_pp_vbfhh_lambda300_5f_hhbbbb,
                     mgp8_pp_tthh_lambda000_5f_hhbbbb,
                     mgp8_pp_tthh_lambda020_5f_hhbbbb,
                     mgp8_pp_tthh_lambda040_5f_hhbbbb,
                     mgp8_pp_tthh_lambda060_5f_hhbbbb,
                     mgp8_pp_tthh_lambda070_5f_hhbbbb,
                     mgp8_pp_tthh_lambda080_5f_hhbbbb,
                     mgp8_pp_tthh_lambda085_5f_hhbbbb,
                     mgp8_pp_tthh_lambda090_5f_hhbbbb,
                     mgp8_pp_tthh_lambda092_5f_hhbbbb,
                     mgp8_pp_tthh_lambda094_5f_hhbbbb,
                     mgp8_pp_tthh_lambda096_5f_hhbbbb,
                     mgp8_pp_tthh_lambda097_5f_hhbbbb,
                     mgp8_pp_tthh_lambda098_5f_hhbbbb,
                     mgp8_pp_tthh_lambda099_5f_hhbbbb,
                     mgp8_pp_tthh_lambda100_5f_hhbbbb,
                     mgp8_pp_tthh_lambda101_5f_hhbbbb,
                     mgp8_pp_tthh_lambda102_5f_hhbbbb,
                     mgp8_pp_tthh_lambda103_5f_hhbbbb,
                     mgp8_pp_tthh_lambda104_5f_hhbbbb,
                     mgp8_pp_tthh_lambda106_5f_hhbbbb,
                     mgp8_pp_tthh_lambda108_5f_hhbbbb,
                     mgp8_pp_tthh_lambda110_5f_hhbbbb,
                     mgp8_pp_tthh_lambda120_5f_hhbbbb,
                     mgp8_pp_tthh_lambda130_5f_hhbbbb,
                     mgp8_pp_tthh_lambda140_5f_hhbbbb,
                     mgp8_pp_tthh_lambda145_5f_hhbbbb,
                     mgp8_pp_tthh_lambda150_5f_hhbbbb,
                     mgp8_pp_tthh_lambda155_5f_hhbbbb,
                     mgp8_pp_tthh_lambda160_5f_hhbbbb,
                     mgp8_pp_tthh_lambda170_5f_hhbbbb,
                     mgp8_pp_tthh_lambda180_5f_hhbbbb,
                     mgp8_pp_tthh_lambda190_5f_hhbbbb,
                     mgp8_pp_tthh_lambda200_5f_hhbbbb,
                     mgp8_pp_tthh_lambda220_5f_hhbbbb,
                     mgp8_pp_tthh_lambda240_5f_hhbbbb,
                     mgp8_pp_tthh_lambda260_5f_hhbbbb,
                     mgp8_pp_tthh_lambda280_5f_hhbbbb,
                     mgp8_pp_tthh_lambda300_5f_hhbbbb,
                     mgp8_pp_vhh_lambda000_5f_hhbbbb,
                     mgp8_pp_vhh_lambda020_5f_hhbbbb,
                     mgp8_pp_vhh_lambda040_5f_hhbbbb,
                     mgp8_pp_vhh_lambda060_5f_hhbbbb,
                     mgp8_pp_vhh_lambda070_5f_hhbbbb,
                     mgp8_pp_vhh_lambda080_5f_hhbbbb,
                     mgp8_pp_vhh_lambda085_5f_hhbbbb,
                     mgp8_pp_vhh_lambda090_5f_hhbbbb,
                     mgp8_pp_vhh_lambda092_5f_hhbbbb,
                     mgp8_pp_vhh_lambda094_5f_hhbbbb,
                     mgp8_pp_vhh_lambda096_5f_hhbbbb,
                     mgp8_pp_vhh_lambda097_5f_hhbbbb,
                     mgp8_pp_vhh_lambda098_5f_hhbbbb,
                     mgp8_pp_vhh_lambda099_5f_hhbbbb,
                     mgp8_pp_vhh_lambda100_5f_hhbbbb,
                     mgp8_pp_vhh_lambda101_5f_hhbbbb,
                     mgp8_pp_vhh_lambda102_5f_hhbbbb,
                     mgp8_pp_vhh_lambda103_5f_hhbbbb,
                     mgp8_pp_vhh_lambda104_5f_hhbbbb,
                     mgp8_pp_vhh_lambda106_5f_hhbbbb,
                     mgp8_pp_vhh_lambda108_5f_hhbbbb,
                     mgp8_pp_vhh_lambda110_5f_hhbbbb,
                     mgp8_pp_vhh_lambda120_5f_hhbbbb,
                     mgp8_pp_vhh_lambda130_5f_hhbbbb,
                     mgp8_pp_vhh_lambda140_5f_hhbbbb,
                     mgp8_pp_vhh_lambda145_5f_hhbbbb,
                     mgp8_pp_vhh_lambda150_5f_hhbbbb,
                     mgp8_pp_vhh_lambda155_5f_hhbbbb,
                     mgp8_pp_vhh_lambda160_5f_hhbbbb,
                     mgp8_pp_vhh_lambda170_5f_hhbbbb,
                     mgp8_pp_vhh_lambda180_5f_hhbbbb,
                     mgp8_pp_vhh_lambda190_5f_hhbbbb,
                     mgp8_pp_vhh_lambda200_5f_hhbbbb,
                     mgp8_pp_vhh_lambda220_5f_hhbbbb,
                     mgp8_pp_vhh_lambda240_5f_hhbbbb,
                     mgp8_pp_vhh_lambda260_5f_hhbbbb,
                     mgp8_pp_vhh_lambda280_5f_hhbbbb,
                     mgp8_pp_vhh_lambda300_5f_hhbbbb,
                     pwp8_pp_hh_lambda000_5f_hhbbbb,
                     pwp8_pp_hh_lambda020_5f_hhbbbb,
                     pwp8_pp_hh_lambda040_5f_hhbbbb,
                     pwp8_pp_hh_lambda060_5f_hhbbbb,
                     pwp8_pp_hh_lambda070_5f_hhbbbb,
                     pwp8_pp_hh_lambda080_5f_hhbbbb,
                     pwp8_pp_hh_lambda085_5f_hhbbbb,
                     pwp8_pp_hh_lambda090_5f_hhbbbb,
                     pwp8_pp_hh_lambda092_5f_hhbbbb,
                     pwp8_pp_hh_lambda094_5f_hhbbbb,
                     pwp8_pp_hh_lambda096_5f_hhbbbb,
                     pwp8_pp_hh_lambda097_5f_hhbbbb,
                     pwp8_pp_hh_lambda098_5f_hhbbbb,
                     pwp8_pp_hh_lambda099_5f_hhbbbb,
                     pwp8_pp_hh_lambda100_5f_hhbbbb,
                     pwp8_pp_hh_lambda101_5f_hhbbbb,
                     pwp8_pp_hh_lambda102_5f_hhbbbb,
                     pwp8_pp_hh_lambda103_5f_hhbbbb,
                     pwp8_pp_hh_lambda104_5f_hhbbbb,
                     pwp8_pp_hh_lambda106_5f_hhbbbb,
                     pwp8_pp_hh_lambda108_5f_hhbbbb,
                     pwp8_pp_hh_lambda110_5f_hhbbbb,
                     pwp8_pp_hh_lambda120_5f_hhbbbb,
                     pwp8_pp_hh_lambda130_5f_hhbbbb,
                     pwp8_pp_hh_lambda140_5f_hhbbbb,
                     pwp8_pp_hh_lambda145_5f_hhbbbb,
                     pwp8_pp_hh_lambda150_5f_hhbbbb,
                     pwp8_pp_hh_lambda155_5f_hhbbbb,
                     pwp8_pp_hh_lambda160_5f_hhbbbb,
                     pwp8_pp_hh_lambda170_5f_hhbbbb,
#                     pwp8_pp_hh_lambda180_5f_hhbbbb,
                     pwp8_pp_hh_lambda190_5f_hhbbbb,
                     pwp8_pp_hh_lambda200_5f_hhbbbb,
                     pwp8_pp_hh_lambda220_5f_hhbbbb,
                     pwp8_pp_hh_lambda240_5f_hhbbbb,
                     pwp8_pp_hh_lambda260_5f_hhbbbb,
                     pwp8_pp_hh_lambda280_5f_hhbbbb,
                     pwp8_pp_hh_lambda300_5f_hhbbbb,
                       
                     mgp8_pp_h012j_5f,
                     mgp8_pp_vbf_h01j_5f,
                     mgp8_pp_tth01j_5f,
                     mgp8_pp_vh012j_5f,

                     mgp8_pp_bbjj_QCD_5f,  
                     mgp8_pp_bbjj_QED_5f,   
                     mgp8_pp_bbjj_QCDQED_5f, 
                     mgp8_pp_tt012j_5f,  

                     mgp8_pp_bbbb_QCD_5f,  
                     mgp8_pp_bbbb_QED_5f,    
                     mgp8_pp_bbbb_QCDQED_5f, 


]

mgp8_pp_vbfhh_lambda000_5f_hhbbbb.splitFactor = 5
mgp8_pp_vbfhh_lambda020_5f_hhbbbb.splitFactor = 5
mgp8_pp_vbfhh_lambda040_5f_hhbbbb.splitFactor = 5
mgp8_pp_vbfhh_lambda060_5f_hhbbbb.splitFactor = 5
mgp8_pp_vbfhh_lambda070_5f_hhbbbb.splitFactor = 5
mgp8_pp_vbfhh_lambda080_5f_hhbbbb.splitFactor = 5
mgp8_pp_vbfhh_lambda085_5f_hhbbbb.splitFactor = 5
mgp8_pp_vbfhh_lambda090_5f_hhbbbb.splitFactor = 5
mgp8_pp_vbfhh_lambda092_5f_hhbbbb.splitFactor = 5
mgp8_pp_vbfhh_lambda094_5f_hhbbbb.splitFactor = 5
mgp8_pp_vbfhh_lambda096_5f_hhbbbb.splitFactor = 5
mgp8_pp_vbfhh_lambda097_5f_hhbbbb.splitFactor = 5
mgp8_pp_vbfhh_lambda098_5f_hhbbbb.splitFactor = 5
mgp8_pp_vbfhh_lambda099_5f_hhbbbb.splitFactor = 5
mgp8_pp_vbfhh_lambda100_5f_hhbbbb.splitFactor = 5
mgp8_pp_vbfhh_lambda101_5f_hhbbbb.splitFactor = 5
mgp8_pp_vbfhh_lambda102_5f_hhbbbb.splitFactor = 5
mgp8_pp_vbfhh_lambda103_5f_hhbbbb.splitFactor = 5
mgp8_pp_vbfhh_lambda104_5f_hhbbbb.splitFactor = 5
mgp8_pp_vbfhh_lambda106_5f_hhbbbb.splitFactor = 5
mgp8_pp_vbfhh_lambda108_5f_hhbbbb.splitFactor = 5
mgp8_pp_vbfhh_lambda110_5f_hhbbbb.splitFactor = 5
mgp8_pp_vbfhh_lambda120_5f_hhbbbb.splitFactor = 5
mgp8_pp_vbfhh_lambda130_5f_hhbbbb.splitFactor = 5
mgp8_pp_vbfhh_lambda140_5f_hhbbbb.splitFactor = 5
mgp8_pp_vbfhh_lambda145_5f_hhbbbb.splitFactor = 5
mgp8_pp_vbfhh_lambda150_5f_hhbbbb.splitFactor = 5
mgp8_pp_vbfhh_lambda155_5f_hhbbbb.splitFactor = 5
mgp8_pp_vbfhh_lambda160_5f_hhbbbb.splitFactor = 5
mgp8_pp_vbfhh_lambda170_5f_hhbbbb.splitFactor = 5
mgp8_pp_vbfhh_lambda180_5f_hhbbbb.splitFactor = 5
mgp8_pp_vbfhh_lambda190_5f_hhbbbb.splitFactor = 5
mgp8_pp_vbfhh_lambda200_5f_hhbbbb.splitFactor = 5
mgp8_pp_vbfhh_lambda220_5f_hhbbbb.splitFactor = 5
mgp8_pp_vbfhh_lambda240_5f_hhbbbb.splitFactor = 5
mgp8_pp_vbfhh_lambda260_5f_hhbbbb.splitFactor = 5
mgp8_pp_vbfhh_lambda280_5f_hhbbbb.splitFactor = 5
mgp8_pp_vbfhh_lambda300_5f_hhbbbb.splitFactor = 5
mgp8_pp_tthh_lambda000_5f_hhbbbb.splitFactor = 5
mgp8_pp_tthh_lambda020_5f_hhbbbb.splitFactor = 5
mgp8_pp_tthh_lambda040_5f_hhbbbb.splitFactor = 5
mgp8_pp_tthh_lambda060_5f_hhbbbb.splitFactor = 5
mgp8_pp_tthh_lambda070_5f_hhbbbb.splitFactor = 5
mgp8_pp_tthh_lambda080_5f_hhbbbb.splitFactor = 5
mgp8_pp_tthh_lambda085_5f_hhbbbb.splitFactor = 5
mgp8_pp_tthh_lambda090_5f_hhbbbb.splitFactor = 5
mgp8_pp_tthh_lambda092_5f_hhbbbb.splitFactor = 5
mgp8_pp_tthh_lambda094_5f_hhbbbb.splitFactor = 5
mgp8_pp_tthh_lambda096_5f_hhbbbb.splitFactor = 5
mgp8_pp_tthh_lambda097_5f_hhbbbb.splitFactor = 5
mgp8_pp_tthh_lambda098_5f_hhbbbb.splitFactor = 5
mgp8_pp_tthh_lambda099_5f_hhbbbb.splitFactor = 5
mgp8_pp_tthh_lambda100_5f_hhbbbb.splitFactor = 5
mgp8_pp_tthh_lambda101_5f_hhbbbb.splitFactor = 5
mgp8_pp_tthh_lambda102_5f_hhbbbb.splitFactor = 5
mgp8_pp_tthh_lambda103_5f_hhbbbb.splitFactor = 5
mgp8_pp_tthh_lambda104_5f_hhbbbb.splitFactor = 5
mgp8_pp_tthh_lambda106_5f_hhbbbb.splitFactor = 5
mgp8_pp_tthh_lambda108_5f_hhbbbb.splitFactor = 5
mgp8_pp_tthh_lambda110_5f_hhbbbb.splitFactor = 5
mgp8_pp_tthh_lambda120_5f_hhbbbb.splitFactor = 5
mgp8_pp_tthh_lambda130_5f_hhbbbb.splitFactor = 5
mgp8_pp_tthh_lambda140_5f_hhbbbb.splitFactor = 5
mgp8_pp_tthh_lambda145_5f_hhbbbb.splitFactor = 5
mgp8_pp_tthh_lambda150_5f_hhbbbb.splitFactor = 5
mgp8_pp_tthh_lambda155_5f_hhbbbb.splitFactor = 5
mgp8_pp_tthh_lambda160_5f_hhbbbb.splitFactor = 5
mgp8_pp_tthh_lambda170_5f_hhbbbb.splitFactor = 5
mgp8_pp_tthh_lambda180_5f_hhbbbb.splitFactor = 5
mgp8_pp_tthh_lambda190_5f_hhbbbb.splitFactor = 5
mgp8_pp_tthh_lambda200_5f_hhbbbb.splitFactor = 5
mgp8_pp_tthh_lambda220_5f_hhbbbb.splitFactor = 5
mgp8_pp_tthh_lambda240_5f_hhbbbb.splitFactor = 5
mgp8_pp_tthh_lambda260_5f_hhbbbb.splitFactor = 5
mgp8_pp_tthh_lambda280_5f_hhbbbb.splitFactor = 5
mgp8_pp_tthh_lambda300_5f_hhbbbb.splitFactor = 5
mgp8_pp_vhh_lambda000_5f_hhbbbb.splitFactor = 5 
mgp8_pp_vhh_lambda020_5f_hhbbbb.splitFactor = 5 
mgp8_pp_vhh_lambda040_5f_hhbbbb.splitFactor = 5 
mgp8_pp_vhh_lambda060_5f_hhbbbb.splitFactor = 5 
mgp8_pp_vhh_lambda070_5f_hhbbbb.splitFactor = 5 
mgp8_pp_vhh_lambda080_5f_hhbbbb.splitFactor = 5 
mgp8_pp_vhh_lambda085_5f_hhbbbb.splitFactor = 5 
mgp8_pp_vhh_lambda090_5f_hhbbbb.splitFactor = 5 
mgp8_pp_vhh_lambda092_5f_hhbbbb.splitFactor = 5 
mgp8_pp_vhh_lambda094_5f_hhbbbb.splitFactor = 5 
mgp8_pp_vhh_lambda096_5f_hhbbbb.splitFactor = 5 
mgp8_pp_vhh_lambda097_5f_hhbbbb.splitFactor = 5 
mgp8_pp_vhh_lambda098_5f_hhbbbb.splitFactor = 5 
mgp8_pp_vhh_lambda099_5f_hhbbbb.splitFactor = 5 
mgp8_pp_vhh_lambda100_5f_hhbbbb.splitFactor = 5 
mgp8_pp_vhh_lambda101_5f_hhbbbb.splitFactor = 5 
mgp8_pp_vhh_lambda102_5f_hhbbbb.splitFactor = 5 
mgp8_pp_vhh_lambda103_5f_hhbbbb.splitFactor = 5 
mgp8_pp_vhh_lambda104_5f_hhbbbb.splitFactor = 5 
mgp8_pp_vhh_lambda106_5f_hhbbbb.splitFactor = 5 
mgp8_pp_vhh_lambda108_5f_hhbbbb.splitFactor = 5 
mgp8_pp_vhh_lambda110_5f_hhbbbb.splitFactor = 5 
mgp8_pp_vhh_lambda120_5f_hhbbbb.splitFactor = 5 
mgp8_pp_vhh_lambda130_5f_hhbbbb.splitFactor = 5 
mgp8_pp_vhh_lambda140_5f_hhbbbb.splitFactor = 5 
mgp8_pp_vhh_lambda145_5f_hhbbbb.splitFactor = 5 
mgp8_pp_vhh_lambda150_5f_hhbbbb.splitFactor = 5 
mgp8_pp_vhh_lambda155_5f_hhbbbb.splitFactor = 5 
mgp8_pp_vhh_lambda160_5f_hhbbbb.splitFactor = 5 
mgp8_pp_vhh_lambda170_5f_hhbbbb.splitFactor = 5 
mgp8_pp_vhh_lambda180_5f_hhbbbb.splitFactor = 5 
mgp8_pp_vhh_lambda190_5f_hhbbbb.splitFactor = 5 
mgp8_pp_vhh_lambda200_5f_hhbbbb.splitFactor = 5 
mgp8_pp_vhh_lambda220_5f_hhbbbb.splitFactor = 5 
mgp8_pp_vhh_lambda240_5f_hhbbbb.splitFactor = 5 
mgp8_pp_vhh_lambda260_5f_hhbbbb.splitFactor = 5 
mgp8_pp_vhh_lambda280_5f_hhbbbb.splitFactor = 5 
mgp8_pp_vhh_lambda300_5f_hhbbbb.splitFactor = 5 
pwp8_pp_hh_lambda000_5f_hhbbbb.splitFactor = 5
pwp8_pp_hh_lambda020_5f_hhbbbb.splitFactor = 5
pwp8_pp_hh_lambda040_5f_hhbbbb.splitFactor = 5
pwp8_pp_hh_lambda060_5f_hhbbbb.splitFactor = 5
pwp8_pp_hh_lambda070_5f_hhbbbb.splitFactor = 5
pwp8_pp_hh_lambda080_5f_hhbbbb.splitFactor = 5
pwp8_pp_hh_lambda085_5f_hhbbbb.splitFactor = 5
pwp8_pp_hh_lambda090_5f_hhbbbb.splitFactor = 5
pwp8_pp_hh_lambda092_5f_hhbbbb.splitFactor = 5
pwp8_pp_hh_lambda094_5f_hhbbbb.splitFactor = 5
pwp8_pp_hh_lambda096_5f_hhbbbb.splitFactor = 5
pwp8_pp_hh_lambda097_5f_hhbbbb.splitFactor = 5
pwp8_pp_hh_lambda098_5f_hhbbbb.splitFactor = 5
pwp8_pp_hh_lambda099_5f_hhbbbb.splitFactor = 5
pwp8_pp_hh_lambda100_5f_hhbbbb.splitFactor = 5
pwp8_pp_hh_lambda101_5f_hhbbbb.splitFactor = 5
pwp8_pp_hh_lambda102_5f_hhbbbb.splitFactor = 5
pwp8_pp_hh_lambda103_5f_hhbbbb.splitFactor = 5
pwp8_pp_hh_lambda104_5f_hhbbbb.splitFactor = 5
pwp8_pp_hh_lambda106_5f_hhbbbb.splitFactor = 5
pwp8_pp_hh_lambda108_5f_hhbbbb.splitFactor = 5
pwp8_pp_hh_lambda110_5f_hhbbbb.splitFactor = 5
pwp8_pp_hh_lambda120_5f_hhbbbb.splitFactor = 5
pwp8_pp_hh_lambda130_5f_hhbbbb.splitFactor = 5
pwp8_pp_hh_lambda140_5f_hhbbbb.splitFactor = 5
pwp8_pp_hh_lambda145_5f_hhbbbb.splitFactor = 5
pwp8_pp_hh_lambda150_5f_hhbbbb.splitFactor = 5
pwp8_pp_hh_lambda155_5f_hhbbbb.splitFactor = 5
pwp8_pp_hh_lambda160_5f_hhbbbb.splitFactor = 5
pwp8_pp_hh_lambda170_5f_hhbbbb.splitFactor = 5
#pwp8_pp_hh_lambda180_5f_hhbbbb.splitFactor = 5
pwp8_pp_hh_lambda190_5f_hhbbbb.splitFactor = 5
pwp8_pp_hh_lambda200_5f_hhbbbb.splitFactor = 5
pwp8_pp_hh_lambda220_5f_hhbbbb.splitFactor = 5
pwp8_pp_hh_lambda240_5f_hhbbbb.splitFactor = 5
pwp8_pp_hh_lambda260_5f_hhbbbb.splitFactor = 5
pwp8_pp_hh_lambda280_5f_hhbbbb.splitFactor = 5
pwp8_pp_hh_lambda300_5f_hhbbbb.splitFactor = 5


mgp8_pp_h012j_5f.splitFactor = 35 
mgp8_pp_vbf_h01j_5f.splitFactor = 20
mgp8_pp_tth01j_5f.splitFactor = 60
mgp8_pp_vh012j_5f.splitFactor = 60

mgp8_pp_bbjj_QCD_5f.splitFactor = 50
mgp8_pp_bbjj_QED_5f.splitFactor = 50
mgp8_pp_bbjj_QCDQED_5f.splitFactor = 50
mgp8_pp_tt012j_5f.splitFactor = 150

mgp8_pp_bbbb_QCD_5f.splitFactor = 50
mgp8_pp_bbbb_QED_5f.splitFactor = 50
mgp8_pp_bbbb_QCDQED_5f.splitFactor = 50

#selectedComponents = [comp]

from heppy.analyzers.fcc.Reader import Reader
source = cfg.Analyzer(
    Reader,

    weights = 'mcEventWeights',

    gen_particles = 'skimmedGenParticles',

    jets = 'pfjets04',
    bTags = 'pfbTags04',

    photons = 'photons',
    photonsToMC = 'photonsToMC',
    photonITags = 'photonITags',

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
from FCChhAnalyses.FCChh.hh_boosted.GenTreeProducer import GenTreeProducer
gen_tree = cfg.Analyzer(
    GenTreeProducer,
    gen_higgses = 'gen_higgses',
)


#############################
##   Reco Level Analysis   ##
#############################

# select isolated muons with pT > 25 GeV and relIso < 0.2
from heppy.analyzers.Selector import Selector
selected_muons = cfg.Analyzer(
    Selector,
    'selected_muons',
    output = 'selected_muons',
    input_objects = 'muons',
    filter_func = lambda ptc: ptc.pt()>20 and ptc.iso.sumpt/ptc.pt()<0.15
)

# select electrons with pT > 25 GeV and relIso < 0.1
selected_electrons = cfg.Analyzer(
    Selector,
    'selected_electrons',
    output = 'selected_electrons',
    input_objects = 'electrons',
    filter_func = lambda ptc: ptc.pt()>20 and ptc.iso.sumpt/ptc.pt()<0.15
)

# merge electrons and muons into a single lepton collection
from heppy.analyzers.Merger import Merger
selected_leptons = cfg.Analyzer(
      Merger,
      instance_label = 'selected_leptons', 
      inputs = ['selected_electrons','selected_muons'],
      output = 'selected_leptons'
)

# select isolated photons with pT > 35 GeV and relIso < 0.4
from heppy.analyzers.Selector import Selector
selected_photons = cfg.Analyzer(
    Selector,
    'selected_photons',
    output = 'selected_photons',
    input_objects = 'photons',
    filter_func = lambda ptc: ptc.pt()> 30. and ptc.iso.sumpt/ptc.pt()<0.15
)


# select jet above 20 GeV
jets_25 = cfg.Analyzer(
    Selector,
    'jets_25',
    output = 'jets_25',
    input_objects = 'jets',
    filter_func = lambda jet: jet.pt()>30.
)

# clean jets from isolated electrons, muons and photons

from heppy.analyzers.Matcher import Matcher
match_jet_electrons = cfg.Analyzer(
    Matcher,
    'electron_jets',
    delta_r = 0.4,
    match_particles = 'selected_electrons',
    particles = 'jets_25'
)

jets_noelectron = cfg.Analyzer(
    Selector,
    'jets_noelectron',
    output = 'jets_noelectron',
    input_objects = 'jets_25',
    filter_func = lambda jet: jet.match is None
)

match_muon_jets = cfg.Analyzer(
    Matcher,
    'muon_jets',
    delta_r = 0.4,
    match_particles = 'selected_muons',
    particles = 'jets_noelectron'
)

jets_nomuon = cfg.Analyzer(
    Selector,
    'jets_nomuon',
    output = 'jets_nomuon',
    input_objects = 'jets_noelectron',
    filter_func = lambda jet: jet.match is None
)

match_photon_jets = cfg.Analyzer(
    Matcher,
    'photon_jets',
    delta_r = 0.4,
    match_particles = 'selected_photons',
    particles = 'jets_nomuon'
)

jets_nophoton = cfg.Analyzer(
    Selector,
    'jets_nophoton',
    output = 'jets_nophoton',
    input_objects = 'jets_nomuon',
    filter_func = lambda jet: jet.match is None
)

# select lights with pT > 30 GeV and relIso < 0.4
selected_lights = cfg.Analyzer(
    Selector,
    'selected_lights',
    output = 'selected_lights',
    input_objects = 'jets_nophoton',
    filter_func = lambda ptc: ptc.tags['bf'] == 0
)

# select b's with pT > 35 GeV and relIso < 0.4
selected_bs = cfg.Analyzer(
    Selector,
    'selected_bs',
    output = 'selected_bs',
    input_objects = 'jets_nophoton',
    filter_func = lambda ptc: ptc.tags['bf'] > 0
)

# create H boson candidates with bs
from FCChhAnalyses.analyzers.HbbBuilder import HbbBuilder
b_higgses = cfg.Analyzer(
      HbbBuilder,
      output = 'b_higgses',
      leg_collection = 'selected_bs',
      pdgid = 25
)

from FCChhAnalyses.FCChh.hhbbbb.selection import Selection
selection = cfg.Analyzer(
    Selection,
    instance_label='cuts'
)

# produce flat root tree containing information after pre-selection
from FCChhAnalyses.FCChh.hhbbbb.TreeProducer import TreeProducer
tree = cfg.Analyzer(
    TreeProducer,
    bs = 'selected_bs',
    hbbs = 'b_higgses',
)

# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence( [
    source,
    selected_muons,
    selected_electrons,
    selected_leptons,
    selected_photons,
    jets_25,
    match_jet_electrons,
    jets_noelectron,
    match_muon_jets,
    jets_nomuon,
    match_photon_jets,
    jets_nophoton,
    selected_bs,
    selected_lights,
    b_higgses,
    tree
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
