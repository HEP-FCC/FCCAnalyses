## Example search for Bu and Bc to tau nu decay

### Overview
This example is a spin-off of the Bc2TauNu search, adding Bu as a separate signal.
Current steps are based on Bc2TauNu scripts. Further developments will be made specific to this analysis.

### Scripts
`preSel_BatchTraining.py` prepares partial samples for stage 1 training.
`preSel_Batch.py` process all samples to be used in later stages. 
`send_training_stage2.sh` prepares files for stage2 MVA training. 

### Development log
31.03.2022 Initial setup of this analysis. Add scripts to prepare samples for stage2 training.
01.04.2022 Add stage1 steps.
