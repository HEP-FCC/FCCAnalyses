from root_numpy import fill_hist
import pyarrow.parquet as pq
import pandas as pd
import ROOT
import numpy as np

##setup needed:
#first start container:
# source /cvmfs/cms.cern.ch/cmsset_default.sh
# cmssw-cc7
#In container source LCG
# source /cvmfs/sft.cern.ch/lcg/views/LCG_101/x86_64-centos7-gcc11-opt/setup.sh

#source /cvmfs/sft.cern.ch/lcg/views/LCG_107/x86_64-el9-gcc13-opt/setup.sh

#make the histograms file for combine, using the output parquet of the DNN analysis

# np.array(df_bkg.loc[(df_bkg.process.str.contains("ttw") | df_bkg.process.str.contains("ttz")) ,:]['prediction_ttbar'])
# np.array(df_bkg.loc[(df_bkg.process.str.contains("ttw") | df_bkg.process.str.contains("ttz")),:]['weight_total'])

def get_array(df, proc_string, var_name):
    if "|" in proc_string:
        print("found or:", proc_string)
        if len(proc_string.split("|")) == 2:
            # print("splitting in two")
            str_1 = proc_string.split("|")[0].strip()
            str_2 = proc_string.split("|")[1].strip()
            # print(str_1, str_2)
            array = np.array(df.loc[(df.process.str.contains(str_1) | df.process.str.contains(str_2)),:][var_name])
            # print(len(array))
        elif len(proc_string.split("|")) == 3:
            # print("splitting in three")
            str_1 = proc_string.split("|")[0].strip()
            str_2 = proc_string.split("|")[1].strip()
            str_3 = proc_string.split("|")[2].strip()
            array = np.array(df.loc[(df.process.str.contains(str_1) | df.process.str.contains(str_2) | df.process.str.contains(str_3)),:][var_name])  
            # print(len(array))
    else:
        array = np.array(df.loc[(df.process.str.contains(proc_string)),:][var_name])
    return array

if __name__ == '__main__':

    mbbyy_bins = np.arange(start = 100, stop = 1500, step = 50)

    skim_pq = pq.read_table("/eos/user/b/bistapf/SWAN_projects/H_to_hh_bbyy/CUTBASED_df_Sel_All_haa_Mbtag_84_Res.parquet")
    df = skim_pq.to_pandas() 
    out_file = ROOT.TFile("/eos/user/b/bistapf/SWAN_projects/H_to_hh_bbyy/resonant_Htohh_bbyy_analysis_hists.root","RECREATE")
    # for i in df.process.unique():
    # 	histo = ROOT.TH1D("mT2_"+str(i) ,"mgg_"+str(i), len(np.array(edges_dict[kdf]))-1,np.array(edges_dict[kdf]))

#     mgp8_pp_Htohh_mH_300GeV_84TeV_hhbbaa
# mgp8_pp_Htohh_mH_350GeV_84TeV_hhbbaa
# mgp8_pp_Htohh_mH_400GeV_84TeV_hhbbaa
# mgp8_pp_Htohh_mH_450GeV_84TeV_hhbbaa
# mgp8_pp_Htohh_mH_500GeV_84TeV_hhbbaa
# mgp8_pp_Htohh_mH_550GeV_84TeV_hhbbaa
# mgp8_pp_Htohh_mH_600GeV_84TeV_hhbbaa
# mgp8_pp_Htohh_mH_650GeV_84TeV_hhbbaa
# mgp8_pp_Htohh_mH_700GeV_84TeV_hhbbaa
# mgp8_pp_Htohh_mH_750GeV_84TeV_hhbbaa
# mgp8_pp_Htohh_mH_800GeV_84TeV_hhbbaa
# mgp8_pp_Htohh_mH_850GeV_84TeV_hhbbaa
# mgp8_pp_Htohh_mH_900GeV_84TeV_hhbbaa
# mgp8_pp_Htohh_mH_950GeV_84TeV_hhbbaa
# mgp8_pp_Htohh_mH_1000GeV_84TeV_hhbbaa


    #get the processes by grouping samples:
    mbbyy_signal_mH300 = get_array(df, "Htohh_mH_300GeV", "hh_m")
    weight_signal_mH300 = get_array(df, "Htohh_mH_300GeV", "weight")

    mbbyy_signal_mH350 = get_array(df, "Htohh_mH_350GeV", "hh_m")
    weight_signal_mH350 = get_array(df, "Htohh_mH_350GeV", "weight")

    mbbyy_signal_mH400 = get_array(df, "Htohh_mH_400GeV", "hh_m")
    weight_signal_mH400 = get_array(df, "Htohh_mH_400GeV", "weight")

    mbbyy_signal_mH450 = get_array(df, "Htohh_mH_450GeV", "hh_m")
    weight_signal_mH450 = get_array(df, "Htohh_mH_450GeV", "weight")

    mbbyy_signal_mH500 = get_array(df, "Htohh_mH_500GeV", "hh_m")
    weight_signal_mH500 = get_array(df, "Htohh_mH_500GeV", "weight")

    mbbyy_signal_mH550 = get_array(df, "Htohh_mH_550GeV", "hh_m")
    weight_signal_mH550 = get_array(df, "Htohh_mH_550GeV", "weight")

    mbbyy_signal_mH600 = get_array(df, "Htohh_mH_600GeV", "hh_m")
    weight_signal_mH600 = get_array(df, "Htohh_mH_600GeV", "weight")

    mbbyy_signal_mH650 = get_array(df, "Htohh_mH_650GeV", "hh_m")
    weight_signal_mH650 = get_array(df, "Htohh_mH_650GeV", "weight")

    mbbyy_signal_mH700 = get_array(df, "Htohh_mH_700GeV", "hh_m")
    weight_signal_mH700 = get_array(df, "Htohh_mH_700GeV", "weight")

    mbbyy_signal_mH750 = get_array(df, "Htohh_mH_750GeV", "hh_m")
    weight_signal_mH750 = get_array(df, "Htohh_mH_750GeV", "weight")

    mbbyy_signal_mH800 = get_array(df, "Htohh_mH_800GeV", "hh_m")
    weight_signal_mH800 = get_array(df, "Htohh_mH_800GeV", "weight")

    mbbyy_signal_mH850 = get_array(df, "Htohh_mH_850GeV", "hh_m")
    weight_signal_mH850 = get_array(df, "Htohh_mH_850GeV", "weight")

    mbbyy_signal_mH900 = get_array(df, "Htohh_mH_900GeV", "hh_m")
    weight_signal_mH900 = get_array(df, "Htohh_mH_900GeV", "weight")

    mbbyy_signal_mH950 = get_array(df, "Htohh_mH_950GeV", "hh_m")
    weight_signal_mH950 = get_array(df, "Htohh_mH_950GeV", "weight")

    mbbyy_signal_mH1000 = get_array(df, "Htohh_mH_1000GeV", "hh_m")
    weight_signal_mH1000 = get_array(df, "Htohh_mH_1000GeV", "weight")

    mbbyy_ggjets = get_array(df, "jjaa", "hh_m")
    weight_ggjets = get_array(df, "jjaa", "weight")

    mbbyy_gjets = get_array(df, "jjaa", "hh_m")
    weight_gjets = get_array(df, "jjaa", "weight")

    #dict to loop
    proc_dict ={
        #data_obs placeholder
        "data_obs":(mbbyy_ggjets, weight_ggjets),
        #bkgs
        "mgp8_pp_ggjets_84TeV":(mbbyy_ggjets, weight_ggjets),
        "mgp8_pp_gjets_84TeV":(mbbyy_gjets, weight_gjets),
        #signals
        "mgp8_pp_Htohh_mH_300GeV_84TeV_hhbbaa":(mbbyy_signal_mH300, weight_signal_mH300),
        "mgp8_pp_Htohh_mH_350GeV_84TeV_hhbbaa": (mbbyy_signal_mH350, weight_signal_mH350),
        "mgp8_pp_Htohh_mH_400GeV_84TeV_hhbbaa": (mbbyy_signal_mH400, weight_signal_mH400),
        "mgp8_pp_Htohh_mH_450GeV_84TeV_hhbbaa": (mbbyy_signal_mH450, weight_signal_mH450),
        "mgp8_pp_Htohh_mH_500GeV_84TeV_hhbbaa": (mbbyy_signal_mH500, weight_signal_mH500),
        "mgp8_pp_Htohh_mH_550GeV_84TeV_hhbbaa": (mbbyy_signal_mH550, weight_signal_mH550),
        "mgp8_pp_Htohh_mH_600GeV_84TeV_hhbbaa": (mbbyy_signal_mH600, weight_signal_mH600),
        "mgp8_pp_Htohh_mH_650GeV_84TeV_hhbbaa": (mbbyy_signal_mH650, weight_signal_mH650),
        "mgp8_pp_Htohh_mH_700GeV_84TeV_hhbbaa": (mbbyy_signal_mH700, weight_signal_mH700),
        "mgp8_pp_Htohh_mH_750GeV_84TeV_hhbbaa": (mbbyy_signal_mH750, weight_signal_mH750),
        "mgp8_pp_Htohh_mH_800GeV_84TeV_hhbbaa": (mbbyy_signal_mH800, weight_signal_mH800),
        "mgp8_pp_Htohh_mH_850GeV_84TeV_hhbbaa": (mbbyy_signal_mH850, weight_signal_mH850),
        "mgp8_pp_Htohh_mH_900GeV_84TeV_hhbbaa": (mbbyy_signal_mH900, weight_signal_mH900),
        "mgp8_pp_Htohh_mH_950GeV_84TeV_hhbbaa": (mbbyy_signal_mH950, weight_signal_mH950),
        "mgp8_pp_Htohh_mH_1000GeV_84TeV_hhbbaa": (mbbyy_signal_mH1000, weight_signal_mH1000),

    }

    for proc_name, proc_tuple in proc_dict.items():
        print("Processing: ", proc_name)
        histo = ROOT.TH1D(proc_name, proc_name, 25, 150., 1400.)
        # histo = ROOT.TH1D(proc_name, proc_name, len(np.array(mbbyy_bins))-1, np.array(mbbyy_bins))
        histo.Sumw2()
        fill_hist(histo, (proc_tuple[0]),
                  weights=(proc_tuple[1]))
        histo.Write()