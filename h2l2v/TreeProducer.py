from heppy.framework.analyzer import Analyzer
from heppy.statistics.tree import Tree
from heppy.analyzers.ntuple import *
from heppy.particles.tlv.resonance import Resonance2 as Resonance
from heppy.analyzers.LeptonicHiggsBuilder import *
from ROOT import TFile, TVector2, TVector3, TLorentzVector
import math, ROOT
from math import sqrt

class TreeProducer(Analyzer):

    def beginLoop(self, setup):
        super(TreeProducer, self).beginLoop(setup)
        self.rootfile = TFile('/'.join([self.dirName,
                                        'tree.root']),
                              'recreate')
        self.tree = Tree( 'events', '')
        self.tree.var('weight', float)
        #self.tree.var('met', float)
        self.tree.var('nljets', float)
        self.tree.var('nbjets', float)
        self.tree.var('njets', float)

        self.tree.var('is_sf', float)
        self.tree.var('is_of', float)

        self.tree.var('mt', float)
        self.tree.var('mr', float)
        self.tree.var('higgs_pt', float)
        self.tree.var('dphi_ll', float)
        self.tree.var('dphi_llmet', float)

        bookParticle(self.tree, 'l1')
        bookParticle(self.tree, 'l2')
        bookParticle(self.tree, 'll')

        bookMet(self.tree, 'met')

    
    def process(self, event):
        self.tree.reset()
        higgses = getattr(event, self.cfg_ana.higgses)

        if len(higgses) > 0:  
            self.tree.fill('weight' , event.weight )
            print len(higgses)
           
            # Reco Higgs
            higgs = higgses[0]
            l1 = higgs.legs[0]
            l2 = higgs.legs[1]
	    
	    fillParticle(self.tree, 'll', higgs)
            fillMet(self.tree, 'met', event.met)

            fillLepton(self.tree, 'l1', l1)
            fillLepton(self.tree, 'l2', l2)

            if abs(l1.pdgid()) == abs(l2.pdgid()):
                self.tree.fill('is_sf' , 1.0 )
                self.tree.fill('is_of' , 0.0 )
            else:
                self.tree.fill('is_sf' , 0.0 )
                self.tree.fill('is_of' , 1.0 )

            hpx  = higgs.pt()*math.cos(higgs.phi())
            hpy  = higgs.pt()*math.sin(higgs.phi())
            metx = event.met.pt()*math.cos(event.met.phi())
            mety = event.met.pt()*math.sin(event.met.phi())
	    
	    pth = math.sqrt((hpx + metx)**2 + (hpy + mety)**2)

            dphi_ll = TVector2.Phi_mpi_pi(l1.phi() - l2.phi())
            dphi_llmet = TVector2.Phi_mpi_pi(higgs.phi() - event.met.phi())
           
	    mt = math.sqrt(2*higgs.pt()*event.met.pt()*(1 - math.cos(dphi_llmet)))

            mll = higgs.m()
            ptll = higgs.pt()
	    met = event.met.pt()
	    
	    met_d_ptll = metx*hpx + mety*hpy
            mr = math.sqrt((mll**2 - met_d_ptll + math.sqrt( (mll**2 + ptll**2)*(mll**2 + met**2) )))
            
	    pl1  = ROOT.TLorentzVector()
	    pl2  = ROOT.TLorentzVector()
	    pMet = ROOT.TVector3()
	    
	    pl1.SetPtEtaPhiM(l1.pt(), l1.eta(), l1.phi(), l1.m())
	    pl2.SetPtEtaPhiM(l2.pt(), l2.eta(), l2.phi(), l2.m())
	    pMet.SetPtEtaPhi(event.met.pt(), 0.0, event.met.phi())
	    
	        
	    def calcMR(L1, L2):
        	E = L1.P()+L2.P()
        	Pz = L1.Pz()+L2.Pz()
        	MR = math.sqrt(E*E-Pz*Pz)
        	return MR

	    def calcMRNEW(L1, L2, M):
        	vI = M + L1.Vect() + L2.Vect()
        	vI.SetZ(0.0)
        	PpQ = calcMR(L1,L2)
        	vptx = (L1+L2).Px()
        	vpty = (L1+L2).Py()
        	vpt = ROOT.TVector3()
        	vpt.SetXYZ(vptx,vpty,0.0)
        	MR2 = 0.5*(PpQ*PpQ-vpt.Dot(vI)+PpQ*sqrt(PpQ*PpQ+vI.Dot(vI)-2.*vI.Dot(vpt)))
                return MR2

	    mr = 2*math.sqrt(calcMRNEW(pl1, pl2, pMet))

            self.tree.fill('mt' , mt )
            self.tree.fill('mr' , mr )
            self.tree.fill('higgs_pt' , pth )
            self.tree.fill('dphi_ll' , abs(dphi_ll) )
            self.tree.fill('dphi_llmet' , abs(dphi_llmet) )
	    self.tree.fill('nbjets' , len(event.selected_bs) )
            self.tree.fill('nljets' , len(event.selected_lights) )
            self.tree.fill('njets' , len(event.selected_lights) + len(event.selected_bs))

            self.tree.tree.Fill()
        
    def write(self, setup):
        self.rootfile.Write()
        self.rootfile.Close()

