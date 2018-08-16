from heppy.framework.analyzer import Analyzer
from heppy.statistics.tree import Tree
from heppy.analyzers.ntuple import *
from heppy.FCChhAnalyses.analyzers.TRFtautag import *
from heppy.particles.tlv.particle import Particle
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
        self.tree.var('Mj1j2_pf04_MetCorr', float)
        self.tree.var('Mj1j2_pf04_MetCorr2', float)
        self.tree.var('mt', float)
        self.tree.var('mr', float)
        self.tree.var('mr2', float)
        self.tree.var('mr3', float)
        self.tree.var('dr', float)
        self.tree.var('dphi', float)
        self.tree.var('dphi_met', float)
        self.tree.var('ntau', int)

        bookMet(self.tree, 'met')


    def corrMET(self, jet1, jet2, met):
        dphi1 = abs(jet1.p4().DeltaPhi(met.p4()))
        dphi2 = abs(jet2.p4().DeltaPhi(met.p4()))

        metp4 = ROOT.TLorentzVector()
        px = met.p4().Px()
        py = met.p4().Py()
            
        if (dphi1 < dphi2):
            pz = jet1.p4().Pz()/2.
            e = math.sqrt(px**2 + py**2 + pz**2)
            metp4.SetPxPyPzE(px, py, pz, e) 
            jetcorr1   = Particle(15, 0, jet1.p4() + metp4, 1)
            jetcorr2   = Particle(15, 0, jet2.p4(), 1)
        else:
            pz = jet2.p4().Pz()/2.
            e = math.sqrt(px**2 + py**2 + pz**2)
            metp4.SetPxPyPzE(px, py, pz, e) 
            jetcorr1  = Particle(15, 0, jet1.p4(), 1)
            jetcorr2  = Particle(15, 0, jet2.p4() + metp4, 1)
        return jetcorr1,jetcorr2

    def corrMET2(self, jet1 , jet2, met):

        metp4 = ROOT.TLorentzVector()
        px = met.p4().Px()
        py = met.p4().Py()
            
        if (jet1.p4().Pt()>jet2.p4().Pt()):
            pz = jet2.p4().Pz()/2.
            e = math.sqrt(px**2 + py**2 + pz**2)
            metp4.SetPxPyPzE(px, py, pz, e) 
            jetcorr2   = Particle(15, 0, jet1.p4() + metp4, 1)
            jetcorr1   = Particle(15, 0, jet2.p4(), 1)
        else:
            pz = jet2.p4().Pz()/2.
            e = math.sqrt(px**2 + py**2 + pz**2)
            metp4.SetPxPyPzE(px, py, pz, e) 
            jetcorr2  = Particle(15, 0, jet1.p4(), 1)
            jetcorr1  = Particle(15, 0, jet2.p4() + metp4, 1)
        return jetcorr1,jetcorr2

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

        jetmet1, jetmet2 = self.corrMET(jets_pf04[0], jets_pf04[1], event.met)
        mtautaumet= self.fillMass(jetmet1,jetmet2)
        self.tree.fill( 'Mj1j2_pf04_MetCorr', mtautaumet)

        jetmet1, jetmet2 = self.corrMET2(jets_pf04[0], jets_pf04[1], event.met)
        mtautaumet= self.fillMass(jetmet1,jetmet2)
        self.tree.fill( 'Mj1j2_pf04_MetCorr2', mtautaumet)

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

        self.tree.fill('mt' , mt )
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
        
