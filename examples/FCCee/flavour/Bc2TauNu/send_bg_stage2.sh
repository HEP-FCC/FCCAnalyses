# example call for standalone file
input=/eos/experiment/fcc/ee/analyses/case-studies/flavour/Bc2TauNu/flatNtuples/27042021/Batch_Analysis_stage1
output=/eos/experiment/fcc/ee/analyses/case-studies/flavour/Bc2TauNu/flatNtuples/27042021/Analysis_stage2
ana=examples/FCCee/flavour/Bc2TauNu



for process in p8_ee_Zbb_ecm91 p8_ee_Zcc_ecm91 p8_ee_Zuds_ecm91;
do
    python $ana/analysis_stage2.py $output/$process.root "$input/$process/*.root"
done

