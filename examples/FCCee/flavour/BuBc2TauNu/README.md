## Example search for Bu and Bc to tau nu decay

### Overview
This example is a spin-off of the Bc2TauNu search, adding Bu as a separate signal.
Current steps are based on Bc2TauNu scripts. Further developments will be made specific to this analysis.

### Scripts
`analysis_stage1.py` with `runTraining=False` prepares partial samples for stage 1 training.
`analysis_stage1.py` with `runTraining=True` process all samples to be used in later stages.
`analysis_stage2.py` with `runTraining=False` prepares files for stage2 MVA training.
`analysis_stage2.py` with `runTraining=True` process all samples to be used for final analysis.
`analysis_final.py` prepares files for categorization and final fit

### Development log
31.03.2022 Initial setup of this analysis. Add scripts to prepare samples for stage2 training.
01.04.2022 Add stage1 steps.
13.04.2022 Add final stage scripts.
03.05.2022 (CH) Move to new running scheme
