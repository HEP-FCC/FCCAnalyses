if [ "${0}" != "${BASH_SOURCE}" ]; then
  if ! [[ $# -eq 1 ]] ; then
    echo "Usage: source ${0} <ANALYSISNAME>"
    echo "Where <ANALYSISNAME> is the local path where the extra analyses will be installed."
    echo "Example local path (with absolute path): /afs/cern.ch/user/x/xyz/FCCsoft/FCCeePhysicsPerformance/case-studies/flavour/tools/localPythonTools"
    return 1
  fi
  export OUTPUT_DIR=${LOCAL_DIR}/${1}
  fccanalysis init ${1} --output-dir ${OUTPUT_DIR} --name ${1} --standalone
  mkdir -p ${OUTPUT_DIR}/build
else
  echo "ERROR: This script is meant to be sourced!"
fi
