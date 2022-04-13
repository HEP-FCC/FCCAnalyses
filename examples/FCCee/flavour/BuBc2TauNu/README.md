## Example search for Bu and Bc to tau nu decay

### Overview
This example is a spin-off of the Bc2TauNu search, adding Bu as a separate signal.
Current steps are based on Bc2TauNu scripts. Further developments will be made specific to this analysis.

### Scripts
`preSel_BatchTraining.py` prepares partial samples for stage 1 training.
`preSel_Batch.py` process all samples to be used in later stages. 
`send_training_stage2.sh` prepares files for stage2 MVA training. 
`finalSel.py` prepares files for categorization and final fit
`send_bgexdec_stage2_*.sh`, `send_bg_stage2.sh`, and `send_signal_stage2.sh` calls `finalSel.py` to run over exclusive bkgs, inclusive bkgs, and signals.

### Development log
31.03.2022 Initial setup of this analysis. Add scripts to prepare samples for stage2 training.
01.04.2022 Add stage1 steps.
13.04.2022 Add final stage scripts.
