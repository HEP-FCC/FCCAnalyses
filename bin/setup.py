import sys
import ROOT

def setup():
    print ("Load cxx analyzers ... ",)
    ROOT.gSystem.Load("libedm4hep")
    ROOT.gSystem.Load("libpodio")
    ROOT.gSystem.Load("libFCCAnalyses")
    ROOT.gErrorIgnoreLevel = ROOT.kFatal
    _edm  = ROOT.edm4hep.ReconstructedParticleData()
    _pod  = ROOT.podio.ObjectID()
    _fcc  = ROOT.getMC_px
    
    print ('edm4hep  ',_edm)
    print ('podio    ',_pod)
    print ('fccana   ',_fcc)
    
    print ('setup done properly')
