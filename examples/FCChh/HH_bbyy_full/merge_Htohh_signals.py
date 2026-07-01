#
#
#Careful, it work only in a cmsenv
#
#
file_name = [
            'mgp8_pp_Htohh_mH_300GeV_84TeV_hhbbaa', 'mgp8_pp_Htohh_mH_350GeV_84TeV_hhbbaa', 
            'mgp8_pp_Htohh_mH_400GeV_84TeV_hhbbaa', 'mgp8_pp_Htohh_mH_450GeV_84TeV_hhbbaa',
            'mgp8_pp_Htohh_mH_500GeV_84TeV_hhbbaa', 'mgp8_pp_Htohh_mH_550GeV_84TeV_hhbbaa',
            'mgp8_pp_Htohh_mH_600GeV_84TeV_hhbbaa', 'mgp8_pp_Htohh_mH_650GeV_84TeV_hhbbaa',
            'mgp8_pp_Htohh_mH_700GeV_84TeV_hhbbaa', 'mgp8_pp_Htohh_mH_750GeV_84TeV_hhbbaa',
            'mgp8_pp_Htohh_mH_800GeV_84TeV_hhbbaa', 'mgp8_pp_Htohh_mH_850GeV_84TeV_hhbbaa',
            'mgp8_pp_Htohh_mH_800GeV_84TeV_hhbbaa', 'mgp8_pp_Htohh_mH_850GeV_84TeV_hhbbaa',
            'mgp8_pp_Htohh_mH_900GeV_84TeV_hhbbaa', 'mgp8_pp_Htohh_mH_950GeV_84TeV_hhbbaa',
            'mgp8_pp_Htohh_mH_1000GeV_84TeV_hhbbaa', 
]

import os
for name in file_name:
         print(name)
         os.system('hadd /eos/experiment/fcc/hh/analysis_ntuples/fcc_v07/II/bbyy_analysis/merged/'+name+'.root $(find /eos/experiment/fcc/hh/analysis_ntuples/fcc_v07/II/bbyy_analysis/'+ name + ' -name "processed*.root")')
