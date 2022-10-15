if [ "${0}" != "${BASH_SOURCE}" ]; then
  if ! [[ $# -eq 1 ]] ; then
    echo "Usage: source ./${0} <ANALYSISNAME>"
    echo "Where <ANALYSISNAME> is the local path where the extra analyses will be installed."
    echo "Example: source ./${0} myAnalysis"
    return 1
  fi

  if [ -d "${1}" ]; then
    echo "User analysis ${1} already exists, please use an other one or remove it before running this script (this is to prevent you from deleting code you have already writen)"
    return 1
  fi

  export OUTPUT_DIR=${LOCAL_DIR}/${1}
  fccanalysis init ${1} --output-dir ${OUTPUT_DIR} --name ${1} --standalone
  mkdir -p ${OUTPUT_DIR}/build
else
  echo "ERROR: This script is meant to be sourced!"
fi
