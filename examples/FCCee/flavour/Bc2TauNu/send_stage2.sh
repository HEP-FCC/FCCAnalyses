# example call for standalone file
input=/eos/experiment/fcc/ee/analyses/case-studies/flavour/Bc2TauNu/flatNtuples/21042021/Batch_Analysis_stage1
output=/eos/experiment/fcc/ee/analyses/case-studies/flavour/Bc2TauNu/flatNtuples/21042021/Analysis_stage2
ana=examples/FCCee/flavour/Bc2TauNu

#python $ana/analysis_stage2.py $output/p8_ee_Zbb_ecm91_EvtGen_Bc2TauNuTAUHADNU.root "$input/p8_ee_Zbb_ecm91_EvtGen_Bc2TauNuTAUHADNU/*.root"
#python $ana/analysis_stage2.py $output/p8_ee_Zbb_ecm91_EvtGen_Bu2TauNuTAUHADNU.root "$input/p8_ee_Zbb_ecm91_EvtGen_Bu2TauNuTAUHADNU/*.root"

python $ana/analysis_stage2.py $output/p8_ee_Zbb_ecm91.root "$input/p8_ee_Zbb_ecm91/*.root"
python $ana/analysis_stage2.py $output/p8_ee_Zcc_ecm91.root "$input/p8_ee_Zcc_ecm91/*.root"
python $ana/analysis_stage2.py $output/p8_ee_Zuds_ecm91.root "$input/p8_ee_Zuds_ecm91/*.root"


python $ana/analysis_stage2.py $output/p8_ee_Zbb_ecm91_EvtGen_BuCocktail.root "$input/p8_ee_Zbb_ecm91_EvtGen_BuCocktail/*.root"
python $ana/analysis_stage2.py $output/p8_ee_Zbb_ecm91_EvtGen_BdCocktail.root "$input/p8_ee_Zbb_ecm91_EvtGen_BdCocktail/*.root"
python $ana/analysis_stage2.py $output/p8_ee_Zbb_ecm91_EvtGen_BsCocktail.root "$input/p8_ee_Zbb_ecm91_EvtGen_BsCocktail/*.root"
python $ana/analysis_stage2.py $output/p8_ee_Zbb_ecm91_EvtGen_LbCocktail.root "$input/p8_ee_Zbb_ecm91_EvtGen_LbCocktail/*.root"

#python examples/FCCee/flavour/Bc2TauNu/analysis_stage2.py p8_ee_Zbb_ecm91_EvtGen_Bu2TauNuTAUHADNU.root "/eos/experiment/fcc/ee/analyses/case-studies/flavour/Bc2TauNu/flatNtuples/21042021/Batch_Analysis_stage1/p8_ee_Zbb_ecm91_EvtGen_Bu2TauNuTAUHADNU/*.root"

#python examples/FCCee/flavour/Bc2TauNu/analysis_stage2.py p8_ee_Zbb_ecm91.root "/eos/experiment/fcc/ee/analyses/case-studies/flavour/Bc2TauNu/flatNtuples/21042021/Batch_Analysis_stage1/p8_ee_Zbb_ecm91/*.root"

#python examples/FCCee/flavour/Bc2TauNu/analysis_stage2.py p8_ee_Zcc_ecm91.root "/eos/experiment/fcc/ee/analyses/case-studies/flavour/Bc2TauNu/flatNtuples/21042021/Batch_Analysis_stage1/p8_ee_Zcc_ecm91/*.root"

#python examples/FCCee/flavour/Bc2TauNu/analysis_stage2.py p8_ee_Zuds_ecm91.root "/eos/experiment/fcc/ee/analyses/case-studies/flavour/Bc2TauNu/flatNtuples/21042021/Batch_Analysis_stage1/p8_ee_Zuds_ecm91/*.root"
