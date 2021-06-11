 - Produce presel files for MVA training, using dedicated production. This will run `analysis_stage1.py` without MVA cut `python HEP-FCC/FCCAnalyses/examples/FCCee/flavour/Bc2TauNu/preSel_BatchTraining.py`

 - With the files produced for training, train the stage1 BDT `python HEP-FCC/FCCeePhysicsPerformance/case-studies/flavour/Bc2TauNu/train_xgb.py`

 - Produce presel files on the full `spring2021` statistics and evaluate the stage 1 MVA. `python examples/FCCee/flavour/Bc2TauNu/preSel_Batch.py`