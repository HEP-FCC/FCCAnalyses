Universe                = vanilla
Environment             = CONDORJOBID=$(Process)
when_to_transfer_output = ON_EXIT
transfer_output_files   = ""
should_transfer_files   = YES
executable              = run_the_skim.sh
arguments               = $(ProcID)
output                  = logs/$Fn(executable).$(ClusterId).$(ProcId).out
error                   = logs/$Fn(executable).$(ClusterId).$(ProcId).err
log                     = logs/$Fn(executable).$(ClusterId).$(ProcId).log
+JobFlavour             = "espresso"
queue 50