if ! [[ $# -eq 1 ]] ; then
    echo "Usage: source ${0} <LOCALPATH>"
    echo "Where <LOCALPATH> is the local path where to install the extra packages"
    echo "Example local path (with absolute path): /afs/cern.ch/user/x/xyz/FCCsoft/FCCeePhysicsPerformance/case-studies/flavour/tools/localPythonTools"
    return 1
fi

mkdir -p ${1}
export PYTHONUSERBASE=${1}/.local
export PATH=${1}/.local/bin:$PATH

echo "> getting latest pip"
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py --user

rm get-pip.py

echo "> getting tools for local running"
pip3 install -U setuptools --user
#pip3 install --user seaborn
#pip3 install --user uproot
pip3 install --user awkward
#pip3 install --user zfit
#pip3 install --user xgboost
#pip3 install --user root-pandas
#pip3 install --user scikit-learn

export PYTHONPATH=${1}/.local/lib/python3.7/site-packages:$PYTHONPATH

echo "> source the localSetup"
source ./localSetup.sh ${1}
