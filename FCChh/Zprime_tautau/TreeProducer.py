from heppy.framework.analyzer import Analyzer
from heppy.statistics.tree import Tree
from heppy.analyzers.ntuple import *
from heppy.FCChhAnalyses.analyzers.TRFtautag import *
from numpy import sign
import ROOT
from ROOT import *

class TreeProducer(Analyzer):

    def beginLoop(self, setup):
        super(TreeProducer, self).beginLoop(setup)
        self.rootfile = TFile('/'.join([self.dirName,
                                        'tree.root']),
                              'recreate')
        self.tree = Tree( 'events', '')
        self.tree.var('weight', float)
        self.tree.var('weight_1tagex', float)
        self.tree.var('weight_2tagex', float)
        self.tree.var('weight_1tagin', float)

        bookParticle(self.tree, 'Jet1_pf04')
        bookParticle(self.tree, 'Jet2_pf04')
        self.tree.var('Mj1j2_pf04', float)
        self.tree.var('mt', float)
        self.tree.var('mr', float)
        self.tree.var('mr2', float)
        self.tree.var('mr3', float)
        self.tree.var('dr', float)
        self.tree.var('dphi', float)
        self.tree.var('dphi_met', float)
        self.tree.var('ntau', int)

        bookMet(self.tree, 'met')


    def fillMass(self, jet1, jet2):
        mj1j2 = ROOT.TLorentzVector()
        j1 = ROOT.TLorentzVector(); j2 = ROOT.TLorentzVector()
        j1.SetPtEtaPhiE(jet1.pt(), jet1.eta(), jet1.phi(), jet1.e())
        j2.SetPtEtaPhiE(jet2.pt(), jet2.eta(), jet2.phi(), jet2.e())
        mj1j2 = j1+j2
        return mj1j2.M()

    def process(self, event):

        self.tree.reset()
        jets_pf04 = getattr(event, self.cfg_ana.jets_pf04_trf)
        ntau=0
        for j in jets_pf04:

            if j.tags['tauf']>0:ntau+=1
        self.tree.fill('ntau' , ntau)
        if len(jets_pf04)<2:return

        weight_1tagex=getOneTagEx(jets_pf04[0],jets_pf04[1])
        weight_2tagex=getTwoTagEx(jets_pf04[0],jets_pf04[1])
        weight_1tagin = weight_1tagex+weight_2tagex

        self.tree.fill('weight_1tagex' , weight_1tagex)
        self.tree.fill('weight_2tagex' , weight_2tagex)
        self.tree.fill('weight_1tagin' , weight_1tagin)
        #print '1tagex: ',weight_1tagex,'    2tagex: ',weight_2tagex,'    1tagin: ',weight_1tagin

        mtautau= self.fillMass(jets_pf04[0],jets_pf04[1])
        self.tree.fill( 'Mj1j2_pf04', mtautau)

        Zprime=ROOT.TLorentzVector()
        j1 = ROOT.TLorentzVector(); j2 = ROOT.TLorentzVector()
        j1.SetPtEtaPhiE(jets_pf04[0].pt(), jets_pf04[0].eta(), jets_pf04[0].phi(), jets_pf04[0].e())
        j2.SetPtEtaPhiE(jets_pf04[1].pt(), jets_pf04[1].eta(), jets_pf04[1].phi(), jets_pf04[1].e())
        Zprime=j1+j2

        Zppx  = Zprime.Pt()*math.cos(Zprime.Phi())
        Zppy  = Zprime.Pt()*math.sin(Zprime.Phi())
        metx = event.met.pt()*math.cos(event.met.phi())
        mety = event.met.pt()*math.sin(event.met.phi())

        ptZp = math.sqrt((Zppx + metx)**2 + (Zppy + mety)**2)

        dphi_ll = TVector2.Phi_mpi_pi(j1.Phi() - j2.Phi())
        dphi_llmet = TVector2.Phi_mpi_pi(Zprime.Phi() - event.met.phi())
        self.tree.fill('dphi',dphi_ll)
        self.tree.fill('dphi_met',dphi_llmet)


        mt = math.sqrt(2*Zprime.Pt()*event.met.pt()*(1 - math.cos(dphi_llmet)))

        mll = Zprime.M()
        ptll = Zprime.Pt()
        met = event.met.pt()

        met_d_ptll = metx*Zppx + mety*Zppy
        mr = math.sqrt((mtautau**2 - met_d_ptll + math.sqrt( (mtautau**2 + ptll**2)*(mll**2 + met**2) )))

        pl1  = ROOT.TLorentzVector()
        pl2  = ROOT.TLorentzVector()
        pMet = ROOT.TVector3()
	    
        pl1.SetPtEtaPhiM(jets_pf04[0].pt(), jets_pf04[0].eta(), jets_pf04[0].phi(), jets_pf04[0].m())
        pl2.SetPtEtaPhiM(jets_pf04[1].pt(), jets_pf04[1].eta(), jets_pf04[1].phi(), jets_pf04[1].m())
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
            MR2 = 0.5*(PpQ*PpQ-vpt.Dot(vI)+PpQ*math.sqrt(PpQ*PpQ+vI.Dot(vI)-2.*vI.Dot(vpt)))
            return MR2

	mr3 = 2*math.sqrt(calcMRNEW(pl1, pl2, pMet))
        mr2 = calcMR(pl1, pl2)

        self.tree.fill('mt' , mt )
        self.tree.fill('mr' , mr )
        self.tree.fill('mr2' , mr2 )
        self.tree.fill('mr3' , mr3 )
        self.tree.fill('dr',pl1.DeltaR(pl2))

        fillParticle(self.tree, 'Jet1_pf04', jets_pf04[0])
        fillParticle(self.tree, 'Jet2_pf04', jets_pf04[1])

        self.tree.fill('weight' , sign(event.weight) )
        met = getattr(event, self.cfg_ana.met)
        fillMet(self.tree, 'met', met)

        self.tree.tree.Fill()

    def write(self, setup):
        self.rootfile.Write()
        self.rootfile.Close()
        
