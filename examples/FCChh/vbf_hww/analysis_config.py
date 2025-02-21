# This propagates config from one to stage to the next
# Mandatory: List of processes to run over
fraction = 1.0
testconfig = False
version='gentest'

if version=='private':
    process_list = {
        # # Add your processes like this: 
        ## '<name of process>':{'fraction':<fraction of events to run over>, 'chunks':<number of chunks to split the output into>, 'output':<name of the output file> }, 
        # # - <name of process> needs to correspond either the name of the input .root file, or the name of a directory containing root files 
        # # If you want to process only part of the events, split the output into chunks or give a different name to the output use the optional arguments
        # # or leave blank to use defaults = run the full statistics in one output file named the same as the process:
        'vbf_hww_llvv': {'fraction':fraction, 'chunks': 1},
        'vv_lep': {'fraction':fraction, 'chunks': 8},
        'ggh_hww_llvv' : {'fraction':fraction, 'chunks': 10},
        'ttbar_lep'    : {'fraction':fraction,'chunks': 26},
        'z_tautau'   : {'fraction':fraction, 'chunks': 10},
        'vbf_z_tautau' : {'fraction':fraction, 'chunks': 1},                
    }
    if testconfig:
        process_list = {'ttbar_lep': {'fraction':0.01}}
    input_dir = '/afs/cern.ch/user/l/lipeles/FCC/data/datasets_v3/'
elif version =='gentest':
    process_list = {
        # # Add your processes like this: 
        ## '<name of process>':{'fraction':<fraction of events to run over>, 'chunks':<number of chunks to split the output into>, 'output':<name of the output file> }, 
        # # - <name of process> needs to correspond either the name of the input .root file, or the name of a directory containing root files 
        # # If you want to process only part of the events, split the output into chunks or give a different name to the output use the optional arguments
        # # or leave blank to use defaults = run the full statistics in one output file named the same as the process:
        #'mgp8_pp_vbf_h01j_5f_hww_lvlv' : { 'fraction':0.01},
        #'mgp8_pp_vbf_h01j_5f_hwwlvlv' : { 'fraction': 0.01 },
        #'mgp8_pp_tt012j_5f_blvblv' : { 'fraction' : 0.01 },
        'mgp8_pp_z0123j_4f_ztautau' : { 'fraction' : 1.0, 'chunks': 30},
    }
    input_dir = '/eos/user/l/lipeles/FCC/hh/generation/DelphesEvents/fcc_v07/II'
elif version =='official':
    process_list = {
        # # Add your processes like this: 
        ## '<name of process>':{'fraction':<fraction of events to run over>, 'chunks':<number of chunks to split the output into>, 'output':<name of the output file> }, 
        # # - <name of process> needs to correspond either the name of the input .root file, or the name of a directory containing root files 
        # # If you want to process only part of the events, split the output into chunks or give a different name to the output use the optional arguments
        # # or leave blank to use defaults = run the full statistics in one output file named the same as the process:
        #'mgp8_pp_vbf_h01j_5f_hww_lvlv' : { 'fraction':0.01},
        #'mgp8_pp_vbf_h01j_5f_hwwlvlv' : { 'fraction': 0.01 },
        #'mgp8_pp_tt012j_5f_blvblv' : { 'fraction' : 0.01 },
        #'mgp8_pp_z0123j_4f_ztautau' : { 'fraction' : 1.0},
    }
    input_dir = '/eos/experiment/fcc/hh/generation/DelphesEvents/fcc_v07/II'

stage1_output = '/afs/cern.ch/user/l/lipeles/FCC/FCCAnalyses/examples/FCChh/outputs/FCChh/vbf_hww/presel_{}'.format(version)
final_output  = "/afs/cern.ch/user/l/lipeles/FCC/FCCAnalyses/examples/FCChh/outputs/FCChh/vbf_hww/final_{}/".format(version)
plots_output  = "/afs/cern.ch/user/l/lipeles/FCC/FCCAnalyses/examples/FCChh/outputs/FCChh/vbf_hww/plots_{}/".format(version)

