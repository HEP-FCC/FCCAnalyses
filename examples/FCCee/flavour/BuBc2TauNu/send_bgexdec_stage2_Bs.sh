# example call for standalone file
input=/eos/experiment/fcc/ee/analyses/case-studies/flavour/Bc2TauNu/flatNtuples/spring2021/prod_04/Batch_Analysis_stage1
output=/eos/experiment/fcc/ee/analyses/case-studies/flavour/Bc2TauNu/flatNtuples/spring2021/prod_04/Analysis_stage2_BuBc2TauNu
ana=examples/FCCee/flavour/BuBc2TauNu/analysis_stage2.py


for process in p8_ee_Zbb_ecm91_EvtGen_Bs2Ds3Pi p8_ee_Zbb_ecm91_EvtGen_Bs2DsDs p8_ee_Zbb_ecm91_EvtGen_Bs2DsTauNu p8_ee_Zbb_ecm91_EvtGen_Bs2Dsst3Pi p8_ee_Zbb_ecm91_EvtGen_Bs2DsstDs p8_ee_Zbb_ecm91_EvtGen_Bs2DsstDsst p8_ee_Zbb_ecm91_EvtGen_Bs2DsstTauNu;
do
    python $ana $output/$process.root "$input/$process/*.root"
done
