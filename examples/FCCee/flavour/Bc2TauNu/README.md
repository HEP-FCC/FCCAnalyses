 - 1) Produce stage1 files for MVA training, using dedicated production. Set the parameter `runTraining=True` in `analysis_stage1.py` to run without MVA stage1 cut `python HEP-FCC/FCCAnalyses/config/FCCAnalysisRun.py examples/FCCee/flavour/Bc2TauNu/analysis_stage1.py`. This will run over a billion events on batch.

 - 2) With the files produced in 1), train the stage1 BDT `python HEP-FCC/FCCeePhysicsPerformance/case-studies/flavour/Bc2TauNu/train_xgb.py`, produce a root file that can be interpreted in RDataFrame.

 - 3) Produce stage1 files on the full `spring2021` statistics and evaluate the stage 1 MVA from 2). Set the parameter `runTraining=False` in `analysis_stage1.py` and run `python HEP-FCC/FCCAnalyses/config/FCCAnalysisRun.py examples/FCCee/flavour/Bc2TauNu/analysis_stage1.py`. This will run over 9 billions events on batch, will take ~12h.

 - 4) Produce stage2 files for MVA training, using dedicated production. Set the parameter `runTraining=True` in `analysis_stage2.py` to run without MVA stage 2 cut `python HEP-FCC/FCCAnalyses/config/FCCAnalysisRun.py examples/FCCee/flavour/Bc2TauNu/analysis_stage2.py`. This will run locally over the files produced in 1).

 - 5) With the files produced in 4), train the stage2 BDT `python HEP-FCC/FCCeePhysicsPerformance/case-studies/flavour/Bc2TauNu/train_xgb_stage2.py`, produce a root file that can be interpreted in RDataFrame.

 - 6) Produce stage2 files on the full `spring2021` statistics and evaluate the stage 2 MVA from 5). Set the parameter `runTraining=False` in `analysis_stage2.py` and run `python HEP-FCC/FCCAnalyses/config/FCCAnalysisRun.py examples/FCCee/flavour/Bc2TauNu/analysis_stage2.py`. This will run locally over the files produced in 3). This will take ~30mins.


 - 7) Now that we have flat ntuples with all the information we need, we can run the analysis. Optimise cuts, fit MVA, run template fit etc...
