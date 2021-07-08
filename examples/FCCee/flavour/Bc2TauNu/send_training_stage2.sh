# example call for standalone file
input=/eos/experiment/fcc/ee/analyses/case-studies/flavour/Bc2TauNu/flatNtuples/spring2021/prod_04/Batch_Training_4stage1
output=/eos/experiment/fcc/ee/analyses/case-studies/flavour/Bc2TauNu/flatNtuples/spring2021/prod_04/Training_4stage2
ana=examples/FCCee/flavour/Bc2TauNu/analysis_stage2.py


for process in p8_ee_Zbb_ecm91 p8_ee_Zcc_ecm91 p8_ee_Zuds_ecm91 p8_ee_Zbb_ecm91_EvtGen_Bc2TauNuTAUHADNU p8_ee_Zbb_ecm91_EvtGen_Bu2TauNuTAUHADNU;
do
    python $ana $output/$process.root "$input/$process/*.root"
done

