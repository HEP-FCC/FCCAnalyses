#!/bin/bash
#BSUB -q 8nm
# ulimit -v 3000000 # NO
unset LD_LIBRARY_PATH
unset PYTHONHOME
export PYTHONPATH=/afs/cern.ch/work/h/helsens/FCC/soft/heppy
echo 'copying job dir to worker'
source /cvmfs/fcc.cern.ch/sw/0.8.3/init_fcc_stack.sh  
cd $HEPPY
source ./init.sh
echo 'environment:'
echo
env | sort
echo
which python
cd -
cp -rf $LS_SUBCWD .
ls
cd `find . -type d | grep /`
echo 'running'
python /afs/cern.ch/user/h/helsens/FCCsoft/heppy/framework/looper.pyc config.pck --nevents=9223372036854775807
echo
echo 'sending the logs back'  # will send also root files if copy failed
cp -r Loop/* $LS_SUBCWD
if [ $? -ne 0 ]; then
   echo 'ERROR: problem copying job directory back'
else
   echo 'job directory copy succeeded'
fi
