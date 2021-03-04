if ! [[ $# -eq 1 ]] ; then
    echo "Usage: source ${0} <LOCALPATH>"
    echo "Where <LOCALPATH> is the local path where the extra python packages have been installed."
    echo "Example local path (with absolute path): /afs/cern.ch/user/x/xyz/FCCsoft/FCCeePhysicsPerformance/case-studies/flavour/tools/localPythonTools"
    return 1
fi

export COMMON=$PWD/python
export PATH=${1}/.local/bin:$PATH
export PYTHONPATH=${1}/.local/lib/python3.7/site-packages:$COMMON:$PYTHONPATH
