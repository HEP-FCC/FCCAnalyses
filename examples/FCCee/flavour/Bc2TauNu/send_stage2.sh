# example call for standalone file
input=/eos/experiment/fcc/ee/analyses/case-studies/flavour/Bc2TauNu/flatNtuples/27042021/Batch_Analysis_stage1
output=/eos/experiment/fcc/ee/analyses/case-studies/flavour/Bc2TauNu/flatNtuples/27042021/Analysis_stage2
ana=examples/FCCee/flavour/Bc2TauNu


for process in p8_ee_Zbb_ecm91_EvtGen_Bc2TauNuTAUHADNU p8_ee_Zbb_ecm91_EvtGen_Bu2TauNuTAUHADNU;
do
    python $ana/analysis_stage2.py $output/$process.root "$input/$process/*.root"
done

for process in p8_ee_Zbb_ecm91 p8_ee_Zcc_ecm91 p8_ee_Zuds_ecm91;
do
    python $ana/analysis_stage2.py $output/$process.root "$input/$process/*.root"
done


for process in p8_ee_Zbb_ecm91_EvtGen_Bd2D3Pi p8_ee_Zbb_ecm91_EvtGen_Bd2DDs p8_ee_Zbb_ecm91_EvtGen_Bd2DTauNu p8_ee_Zbb_ecm91_EvtGen_Bd2Dst3Pi p8_ee_Zbb_ecm91_EvtGen_Bd2DstDs p8_ee_Zbb_ecm91_EvtGen_Bd2DstDsst p8_ee_Zbb_ecm91_EvtGen_Bd2DstTauNu;
do
    python $ana/analysis_stage2.py $output/$process.root "$input/$process/*.root"
done


for process in p8_ee_Zbb_ecm91_EvtGen_Bs2Ds3Pi p8_ee_Zbb_ecm91_EvtGen_Bs2DsDs p8_ee_Zbb_ecm91_EvtGen_Bs2DsTauNu p8_ee_Zbb_ecm91_EvtGen_Bs2Dsst3Pi p8_ee_Zbb_ecm91_EvtGen_Bs2DsstDs p8_ee_Zbb_ecm91_EvtGen_Bs2DsstDsst p8_ee_Zbb_ecm91_EvtGen_Bs2DsstTauNu;
do
    python $ana/analysis_stage2.py $output/$process.root "$input/$process/*.root"
done


for process in p8_ee_Zbb_ecm91_EvtGen_Bu2D03Pi p8_ee_Zbb_ecm91_EvtGen_Bu2D0Ds p8_ee_Zbb_ecm91_EvtGen_Bu2D0TauNu p8_ee_Zbb_ecm91_EvtGen_Bu2Dst03Pi p8_ee_Zbb_ecm91_EvtGen_Bu2Dst0Ds p8_ee_Zbb_ecm91_EvtGen_Bu2Dst0Dsst p8_ee_Zbb_ecm91_EvtGen_Bu2Dst0TauNu;
do
    python $ana/analysis_stage2.py $output/$process.root "$input/$process/*.root"
done


for process in p8_ee_Zbb_ecm91_EvtGen_Lb2Lc3Pi p8_ee_Zbb_ecm91_EvtGen_Lb2LcDs p8_ee_Zbb_ecm91_EvtGen_Lb2LcTauNu p8_ee_Zbb_ecm91_EvtGen_Lb2Lcst3Pi p8_ee_Zbb_ecm91_EvtGen_Lb2LcstDs p8_ee_Zbb_ecm91_EvtGen_Lb2LcstDsst p8_ee_Zbb_ecm91_EvtGen_Lb2LcstTauNu;
do
    python $ana/analysis_stage2.py $output/$process.root "$input/$process/*.root"
done
