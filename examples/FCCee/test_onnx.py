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
_wea  = ROOT.WeaverInterface.get('/afs/cern.ch/work/s/selvaggi/public/4Laurent/ONNX/fccee_flavtagging_dummy.onnx')

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
               .Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
               .Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")
               .Define("RP_e",          "ReconstructedParticle::get_e(ReconstructedParticles)")
               .Define("RP_theta",      "ReconstructedParticle::get_theta(ReconstructedParticles)")
               .Define("RP_phi",        "ReconstructedParticle::get_phi(ReconstructedParticles)")
               .Define("RP_charge",     "ReconstructedParticle::get_charge(ReconstructedParticles)")
               .Define("RP_pid" ,       "myUtils::PID(ReconstructedParticles, MCRecoAssociations0, MCRecoAssociations1, Particle)")

               #.Define("MVAVec", "WeaverInterface::get()(RP_e, RP_theta, RP_phi, RP_pid, RP_charge)")
               #.Define("MVAVec", "WeaverInterface::get()(ROOT::VecOps::RVec<ROOT::VecOps::RVec<float> >{RP_theta, RP_phi}, ROOT::VecOps::RVec<ROOT::VecOps::RVec<float> >{RP_e, RP_theta, RP_phi, RP_pid, RP_charge}, ROOT::VecOps::RVec<ROOT::VecOps::RVec<float> >{})")
               #.Define("MVAVec", "WeaverInterface::get()({RP_e, RP_theta, RP_phi, RP_pid, RP_charge})")
        )
        print('after')
        # select branches for output file
        branchList = ROOT.vector('string')()
        for branchName in [
            'RP_theta', 'RP_phi',
            #'MVAVec',
            'RP_pid',
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
