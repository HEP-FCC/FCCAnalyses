import sys
import ROOT
from array import array

print ("Load cxx analyzers ... ",)
ROOT.gSystem.Load("libedm4hep")
ROOT.gSystem.Load("libpodio")
ROOT.gSystem.Load("libawkward")
ROOT.gSystem.Load("libawkward-cpu-kernels")
ROOT.gSystem.Load("libFCCAnalyses")

ROOT.gErrorIgnoreLevel = ROOT.kFatal
_edm  = ROOT.edm4hep.ReconstructedParticleData()
_pod  = ROOT.podio.ObjectID()
_fcc  = ROOT.dummyLoader
_wea  = ROOT.WeaverInterface.get('/afs/cern.ch/work/s/selvaggi/public/4Laurent/ONNX/fccee_flavtagging_dummy.onnx',
                                 '/afs/cern.ch/work/s/selvaggi/public/4Laurent/ONNX/preprocess.json')

print ('edm4hep  ',_edm)
print ('podio    ',_pod)
print ('fccana   ',_fcc)

class analysis():

    #__________________________________________________________
    def __init__(self, inputlist, outname, ncpu):
        self.outname = outname
        if ".root" not in outname:
            self.outname+=".root"

        ROOT.ROOT.EnableImplicitMT(ncpu)
        ROOT.EnableThreadSafety()
        self.df = ROOT.RDataFrame("events", inputlist)
        print (" init done, about to run")
        translation = {'pfcand_e': '', 'pfcand_theta': '', 'pfcand_phi': '', 'pfcand_pid': '', 'pfcand_charge': ''}
        #exit(0)

    #__________________________________________________________
    def run(self):
        #df2 = (self.df.Range(1000)
        print('before')
        df2 = (self.df
               .Define("JetsConstituents", "JetConstituentsUtils::build_constituents(Jet, ReconstructedParticles)")

               .Define("RP_e",          "JetConstituentsUtils::get_e(JetsConstituents)")
               .Define("RP_theta",      "JetConstituentsUtils::get_theta(JetsConstituents)")
               .Define("RP_phi",        "JetConstituentsUtils::get_phi(JetsConstituents)")
               .Define("RP_charge",     "JetConstituentsUtils::get_charge(JetsConstituents)")

               .Define("MVAVec", "WeaverInterface::get()(RP_e, RP_theta, RP_phi, RP_phi, RP_charge).at(0)")
               #.Define("MVAVec", _wea, ("RP_e", "RP_theta", "RP_phi", "RP_phi", "RP_charge"))

               .Define("MVAb", "MVAVec.at(0)")
        )
        print('after')
        # select branches for output file
        branchList = ROOT.vector('string')()
        for branchName in [
            'MVAb',
            ]:
            branchList.push_back(branchName)
        df2.Snapshot("events", self.outname, branchList)

if __name__ == '__main__':
    if len(sys.argv)==1:
        print ("usage:")
        print ("python ",sys.argv[0]," file.root")
        sys.exit(3)
    infile = sys.argv[1]
    outDir = 'FCCee/'+sys.argv[0].split('/')[1]+'/'
    import os
    os.system("mkdir -p {}".format(outDir))
    outfile = outDir+infile.split('/')[-1]
    ncpus = 0
    analysis = analysis(infile, outfile, ncpus)
    analysis.run()

    print(outfile)

    tf = ROOT.TFile(infile)
    entries = tf.events.GetEntries()
    p = ROOT.TParameter(int)( "eventsProcessed", entries)
    outf=ROOT.TFile(outfile,"UPDATE")
    p.Write()
