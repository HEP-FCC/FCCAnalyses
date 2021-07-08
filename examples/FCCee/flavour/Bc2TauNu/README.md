 - 1) Produce stage1 files for MVA training, using dedicated production. This will run `analysis_stage1.py` without MVA stage1 cut `python HEP-FCC/FCCAnalyses/examples/FCCee/flavour/Bc2TauNu/preSel_BatchTraining.py`. This will run over a billion events on batch.

 - 2) With the files produced in 1), train the stage1 BDT `python HEP-FCC/FCCeePhysicsPerformance/case-studies/flavour/Bc2TauNu/train_xgb.py`, produce a root file that can be interpreted in RDataFrame.

 - 3) Produce stage1 files on the full `spring2021` statistics and evaluate the stage 1 MVA from 2). `python examples/FCCee/flavour/Bc2TauNu/preSel_Batch.py`. This will run over 9 billions events on batch, will take ~12h.

 - 4) Produce stage2 files for MVA training, using dedicated production. This will run `analysis_stage2.py` without MVA stage 2 cut `./HEP-FCC/FCCAnalyses/examples/FCCee/flavour/Bc2TauNu/send_training_stage2.sh`. This will run locally over the files produced in 1).

 - 5) With the files produced in 4), train the stage2 BDT `python HEP-FCC/FCCeePhysicsPerformance/case-studies/flavour/Bc2TauNu/train_xgb_stage2.py`, produce a root file that can be interpreted in RDataFrame.

 - 6) Produce stage2 files on the full `spring2021` statistics and evaluate the stage 2 MVA from 5). 
`./HEP-FCC/FCCAnalyses/examples/FCCee/flavour/Bc2TauNu/send_bg_stage2.sh`, `./HEP-FCC/FCCAnalyses/examples/FCCee/flavour/Bc2TauNu/send_bgexdec_stage2_Bu.sh`, `./HEP-FCC/FCCAnalyses/examples/FCCee/flavour/Bc2TauNu/send_bgexdec_stage2_Bd.sh`, `./HEP-FCC/FCCAnalyses/examples/FCCee/flavour/Bc2TauNu/send_bgexdec_stage2_Bs.sh`, `./HEP-FCC/FCCAnalyses/examples/FCCee/flavour/Bc2TauNu/send_bgexdec_stage2_Lb.sh`, `./HEP-FCC/FCCAnalyses/examples/FCCee/flavour/Bc2TauNu/send_signal_stage2.sh`. This will run locally over the files produced in 3). This will take ~30mins.


 - 7) Now that we have flat ntuples with all the information we need, we can run the analysis. Optimise cuts, fit MVA, run template fit etc...
