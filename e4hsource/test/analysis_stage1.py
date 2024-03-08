'''
First stage
'''

# Mandatory:
# List of processes used in the analysis
processList = {
    # Run over the full statistics and save it to one output file named
    # <outputDir>/<process_name>.root
    'p8_ee_ZZ_ecm240': {'fraction': 0.005},
    # Run over 50% of the statistics and save output into two files named
    # <outputDir>/p8_ee_WW_ecm240/chunk<N>.root
    'p8_ee_WW_ecm240': {'fraction': 0.5, 'chunks': 2},
    # Run over 20% of the statistics and save output into one file named
    # <outputDir>/p8_ee_ZH_ecm240_out.root
    'p8_ee_ZH_ecm240': {'fraction': 0.2, 'output': 'p8_ee_ZH_ecm240_out'}
}

# Mandatory:
# Production tag when running over EDM4Hep centrally produced events, this
# points to the yaml files for getting sample statistics
prodTag = "FCCee/spring2021/IDEA/"

# Optional:
# Output directory, default is local running directory
outputDir = "outputs/source"

# Optional:
# Name of the analysis, default is ""
# analysisName = "My Analysis"

# Optional:
# Number of threads to run on, default is 4
# nCPUS = 4

# Optional:
# Optional running on HTCondor, default is False
# runBatch = False

# Optional:
# Batch queue name when running on HTCondor, default is workday
# batchQueue = "longlunch"

# Optional:
# Computing account when running on HTCondor, default is group_u_FCC.local_gen
# compGroup = "group_u_FCC.local_gen"

# Optional:
# How to read the input files
useDataSource = True

# Optional:
# Test file location
# testFile = 'https://fccsw.web.cern.ch/fccsw/testsamples/' \
#            'edm4hep1/p8_ee_WW_ecm240_edm4hep.root'
testFile = 'input/30k/p8_ee_ZH_ecm240_edm4hep.root'


# Mandatory:
# RDFanalysis class where the user defines the operations on the input
# collections
class RDFanalysis():
    '''
    Analysis class.
    '''
    def __init__(self):
        self.column_list = [
            "selected_muons_pt",
            "selected_muons_y",
            "selected_muons_p",
            "selected_muons_e",
            "zed_leptonic_pt",
            "zed_leptonic_m",
            "zed_leptonic_charge",
            "zed_leptonic_recoil_m"
        ]

    # Mandatory:
    # Analysers function to define the analysers to process, please make sure
    # you return the last dataframe, in this example it is dframe2
    def analysers(dframe):
        '''
        Defining operations on the dataframe.
        '''
        dframe2 = (
            dframe
            # select muons on pT
            .Define("selected_muons", "recoParticle::selPt(10.)(Muon)")
            # create column with muon transverse momentum
            .Define("selected_muons_pt", "recoParticle::getPt(selected_muons)")
            # create column with muon rapidity
            .Define("selected_muons_y", "recoParticle::getY(selected_muons)")
            # create column with muon total momentum
            .Define("selected_muons_p", "recoParticle::getP(selected_muons)")
            # create column with muon energy
            .Define("selected_muons_e", "recoParticle::getE(selected_muons)")
            # find zed candidates from  di-muon resonances
            .Define("zed_leptonic",
                    "recoParticle::resonanceBuilder(91)(selected_muons)")
            # create column with zed transverse momenta
            .Define("zed_leptonic_pt", "recoParticle::getPt(zed_leptonic)")
            # create column with zed mass
            .Define("zed_leptonic_m", "recoParticle::getMass(zed_leptonic)")
            # create column with leptonic charge
            .Define("zed_leptonic_charge",
                    "recoParticle::getCharge(zed_leptonic)")
            # calculate recoil of zed_leptonic
            .Define("zed_leptonic_recoil",
                    "recoParticle::recoilBuilder(240)(zed_leptonic)")
            # create column with recoil mass
            .Define("zed_leptonic_recoil_m",
                    "recoParticle::getMass(zed_leptonic_recoil)")
            # Filter on at least one candidate
            .Filter("zed_leptonic_recoil_m.size() > 0")
        )
        return dframe2

    # Mandatory:
    # Output function, please make sure you return the column list as a python
    # list
    def output():
        '''
        Which columns to snapshot.
        '''
        branchList = [
                "selected_muons_pt",
                "selected_muons_y",
                "selected_muons_p",
                "selected_muons_e",
                "zed_leptonic_pt",
                "zed_leptonic_m",
                "zed_leptonic_charge",
                "zed_leptonic_recoil_m"
            ]

        return branchList
