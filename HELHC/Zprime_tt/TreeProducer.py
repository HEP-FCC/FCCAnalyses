from __future__ import division
from heppy.framework.analyzer import Analyzer
from heppy.statistics.tree import Tree
from heppy.analyzers.ntuple import *
from heppy.particles.tlv.resonance import Resonance2 as Resonance
from heppy.particles.tlv.particle import Particle
from heppy.FCChhAnalyses.analyzers.TRFbtag import *

import math
import ROOT
from ROOT import *
import collections
#from array import array
import array
import os

#For TMVA >>>>>>>>>>>>>>>>>>>>>
#ROOT.gROOT.ProcessLine('.L /afs/cern.ch/user/r/rasmith/fcc/heppy/FCChhAnalyses/Zprime_tt/BDT_QCD.class.C+')

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
        self.tree.var('missingET', float)
        self.tree.var('numberOfElectrons', int)
        self.tree.var('numberOfMuons', int)

        #trk02 no SD
        self.tree.var('Jet1_trk02_tau1', float)       
        self.tree.var('Jet1_trk02_tau2', float)
        self.tree.var('Jet1_trk02_tau3', float)
        self.tree.var('Jet2_trk02_tau1', float)
        self.tree.var('Jet2_trk02_tau2', float)
        self.tree.var('Jet2_trk02_tau3', float)
        self.tree.var('Jet1_trk02_tau32', float)
        self.tree.var('Jet1_trk02_tau31', float)
        self.tree.var('Jet1_trk02_tau21', float)
        self.tree.var('Jet2_trk02_tau32', float)
        self.tree.var('Jet2_trk02_tau31', float)
        self.tree.var('Jet2_trk02_tau21', float)
 
        #bookParticle(self.tree, 'Jet1_trk02_Corr')
        #bookParticle(self.tree, 'Jet2_trk02_Corr')

        #bookParticle(self.tree, 'Jet1_trk02_MetCorr')
        #bookParticle(self.tree, 'Jet2_trk02_MetCorr')

        bookParticle(self.tree, 'Jet1_trk02_Corr_MetCorr')
        bookParticle(self.tree, 'Jet2_trk02_Corr_MetCorr')

        self.tree.var('rapiditySeparation_trk02', float)
        self.tree.var('transverseMomentumAsymmetry_trk02', float)
        self.tree.var('topJetMassDifference', float)


        #trk02 SD
        #bookParticle(self.tree, 'Jet1_trk02_SD')
        #bookParticle(self.tree, 'Jet2_trk02_SD')

        bookParticle(self.tree, 'Jet1_trk02_SD_Corr')
        bookParticle(self.tree, 'Jet2_trk02_SD_Corr')

        bookParticle(self.tree, 'Jet1_trk02_SD_MetCorr')
        bookParticle(self.tree, 'Jet2_trk02_SD_MetCorr')
        
        bookParticle(self.tree, 'Jet1_trk02_SD_Corr_MetCorr')
        bookParticle(self.tree, 'Jet2_trk02_SD_Corr_MetCorr')

        self.tree.var('Jet1_trk04_SD_Corr_m', float)
        self.tree.var('Jet2_trk04_SD_Corr_m', float)

        self.tree.var('Jet1_trk08_SD_Corr_m', float)
        self.tree.var('Jet2_trk08_SD_Corr_m', float)
 
        bookParticle(self.tree, 'Electron1')
        bookParticle(self.tree, 'Electron2')

        bookParticle(self.tree, 'Muon1')
        bookParticle(self.tree, 'Muon2')

        #self.tree.var('BDTvariable_qcd', float)

        self.tree.var('Mj1j2_trk02', float)
        self.tree.var('Mj1j2_trk02_Corr', float)
        self.tree.var('Mj1j2_trk02_MetCorr', float)
        self.tree.var('Mj1j2_trk02_Corr_MetCorr', float)

        self.tree.var('Mj1j2_pf02', float)
        self.tree.var('Mj1j2_pf02_MetCorr', float)

        self.tree.var('Mj1j2_pf04', float)
        self.tree.var('Mj1j2_pf04_MetCorr', float)

        self.tree.var('Mj1j2_pf08', float)
        self.tree.var('Mj1j2_pf08_MetCorr', float)

        self.tree.var('Jet1_trk02_dR_lep', float)
        self.tree.var('Jet2_trk02_dR_lep', float)

        # for MVA
        self.reader = ROOT.TMVA.Reader()
        self.bdt_Jet_trk02_tau1 = array.array('f',[0])
        self.bdt_Jet_trk02_tau2 = array.array('f',[0])
        self.bdt_Jet_trk02_tau3 = array.array('f',[0])
        self.bdt_Jet_trk02_tau21 = array.array('f',[0])
        self.bdt_Jet_trk02_tau31 = array.array('f',[0])
        self.bdt_Jet_trk02_tau32 = array.array('f',[0])
        self.bdt_Jet_trk02_SD_Corr_m = array.array('f',[0])
        self.bdt_Jet_trk04_SD_Corr_m = array.array('f',[0])
        self.bdt_Jet_trk08_SD_Corr_m = array.array('f',[0])
        self.reader.AddVariable("Jet_trk02_tau1",      self.bdt_Jet_trk02_tau1     )
        self.reader.AddVariable("Jet_trk02_tau2",      self.bdt_Jet_trk02_tau2     )
        self.reader.AddVariable("Jet_trk02_tau3",      self.bdt_Jet_trk02_tau3     )
        self.reader.AddVariable("Jet_trk02_tau21",     self.bdt_Jet_trk02_tau21    )
        self.reader.AddVariable("Jet_trk02_tau31",     self.bdt_Jet_trk02_tau31    )
        self.reader.AddVariable("Jet_trk02_tau32",     self.bdt_Jet_trk02_tau32    )
        self.reader.AddVariable("Jet_trk02_SD_Corr_m", self.bdt_Jet_trk02_SD_Corr_m)
        self.reader.AddVariable("Jet_trk04_SD_Corr_m", self.bdt_Jet_trk04_SD_Corr_m)
        self.reader.AddVariable("Jet_trk08_SD_Corr_m", self.bdt_Jet_trk08_SD_Corr_m)
        path = "/eos/experiment/fcc/hh/analyses/W_top_vs_QCD_tagger/heppy_outputs/fcc_v02/TMVA_trainings/"
        #path = "/afs/cern.ch/user/d/djamin/fcc_work/BDT_trains/20180223_tagger/"
        self.reader.BookMVA("BDT",str(path)+"BDT_BDT_thad_vs_QCD.weights.xml")
        self.tree.var('Jet1_thad_vs_QCD_tagger', float)
        self.tree.var('Jet2_thad_vs_QCD_tagger', float)

        #self.tree.var('label', int)
        #self.tree2 = Tree( 'all_events', '')
        #self.tree2.var('label', int)

    def corrMET(self, jet1, pdg1 , jet2, pdg2, met):
        dphi1 = abs(jet1.p4().DeltaPhi(met.p4()))
        dphi2 = abs(jet2.p4().DeltaPhi(met.p4()))

        metp4 = ROOT.TLorentzVector()
        px = met.p4().Px()
        py = met.p4().Py()
            
        if (dphi1 < dphi2):
            pz = jet1.p4().Pz()/2.
            e = math.sqrt(px**2 + py**2 + pz**2)
            metp4.SetPxPyPzE(px, py, pz, e) 
            jetcorr1   = Particle(pdg1, 0, jet1.p4() + metp4, 1)
            jetcorr2   = Particle(pdg2, 0, jet2.p4(), 1)
        else:
            pz = jet2.p4().Pz()/2.
            e = math.sqrt(px**2 + py**2 + pz**2)
            metp4.SetPxPyPzE(px, py, pz, e) 
            jetcorr1  = Particle(pdg1, 0, jet1.p4(), 1)
            jetcorr2  = Particle(pdg2, 0, jet2.p4() + metp4, 1)
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
        jets_trk02 = getattr(event, self.cfg_ana.jets_trk02_1000)
        jets_pf02 = getattr(event, self.cfg_ana.jets_pf02_1500)
        jets_pf04 = getattr(event, self.cfg_ana.jets_pf04_1000)
        jets_pf04_pdg = event.jets_pf04_1000_pdg
        jets_pf08 = getattr(event, self.cfg_ana.jets_pf08_1500)
        #gen_particles = event.all_particles

        jets_pf04_1500 = getattr(event, self.cfg_ana.jets_pf04_1500)
        jets_trk04 = getattr(event, self.cfg_ana.jets_trk04_1000)
        jets_trk08 = getattr(event, self.cfg_ana.jets_trk08_1000)
        
        electrons = getattr(event, self.cfg_ana.electrons)
        muons = getattr(event, self.cfg_ana.muons)

        #self.tree2.reset()
        ##
        #label = -1
        #part1 = -10000
        #part2 = -10000
        #index = 0
        #part_index = -1
        #count = 0
        #for j in gen_particles :
        #  # 1st part
        #  if (j.status()==22 or j.status()==23) and count==0:
        #    part1 = j.pdgid()
        #    count += 1
        #    part_index = index
        #  # 2nd part
        #  if (j.status()==22 or j.status()==23) and count==1 and j.q()+gen_particles[part_index].q()==0:
        #    part2 = j.pdgid()
        #    count += 1
        #  index += 1
        #if abs(part1)==6 and abs(part2)==6 : label = 6
        #if abs(part1)==5 and abs(part2)==5 : label = 5
        #if abs(part1)==4 and abs(part2)==4 : label = 4
        #if abs(part1)==3 and abs(part2)==3 : label = 0
        #if abs(part1)==2 and abs(part2)==2 : label = 0
        #if abs(part1)==1 and abs(part2)==1 : label = 0
        ## missed cases
        #if label == -1 :
        #  count = 0
        #  for j in gen_particles :
        #    if count<10 and abs(j.pdgid())==6 :
        #      label = 6
        #    count += 1
        #if label==-1 : print "issue label==-1"
        ##
        #self.tree2.fill('label' , label )
        #self.tree2.tree.Fill()

        Jet1_trk02_dR_lep = 999
        Jet2_trk02_dR_lep  = 999
        if ( len(jets_trk02)>=2 and  len(jets_pf02)>=2):

            #self.tree.fill('label' , label )

            j1 = ROOT.TLorentzVector(); j2 = ROOT.TLorentzVector()
            j1.SetPtEtaPhiE(jets_trk02[0].pt(), jets_trk02[0].eta(), jets_trk02[0].phi(), jets_trk02[0].e())
            j2.SetPtEtaPhiE(jets_trk02[1].pt(), jets_trk02[1].eta(), jets_trk02[1].phi(), jets_trk02[1].e())
            if ( len(electrons)!=0 and len(muons)==0 ):
                e = ROOT.TLorentzVector()
                e.SetPtEtaPhiE(electrons[0].pt(), electrons[0].eta(), electrons[0].phi(), electrons[0].e())
                Jet1_dR = j1.DeltaR(e)
                Jet2_dR = j2.DeltaR(e)
            if ( len(electrons)==0 and len(muons)!=0 ):
                m = ROOT.TLorentzVector()
                m.SetPtEtaPhiE(muons[0].pt(), muons[0].eta(), muons[0].phi(), muons[0].e())
                Jet1_dR = j1.DeltaR(m)
                Jet2_dR = j2.DeltaR(m)
            if ( len(electrons)!=0 and len(muons)!=0 ):
                isElectron = False; isMuon = False
                if ( electrons[0].pt() > muons[0].pt() ): isElectron = True
                else: isMuon = True
                l = ROOT.TLorentzVector()
                if isElectron: l.SetPtEtaPhiE(electrons[0].pt(), electrons[0].eta(), electrons[0].phi(), electrons[0].e())
                if isMuon: l.SetPtEtaPhiE(muons[0].pt(), muons[0].eta(), muons[0].phi(), muons[0].e())
                Jet1_trk02_dR_lep  = j1.DeltaR(l)
                Jet2_trk02_dR_lep  = j2.DeltaR(l)
            
            self.tree.fill('Jet1_trk02_dR_lep' , Jet1_trk02_dR_lep )
            self.tree.fill('Jet2_trk02_dR_lep' , Jet2_trk02_dR_lep )
#had_hadsemilep_lep_decays

            self.tree.fill('weight' , event.weight )
            self.tree.fill('missingET', event.met.pt())
            self.tree.fill('numberOfElectrons', len(electrons))
            self.tree.fill('numberOfMuons', len(muons))

            self.tree.fill('rapiditySeparation_trk02', abs(jets_trk02[0].eta() - jets_trk02[1].eta()))
            self.tree.fill('transverseMomentumAsymmetry_trk02', (jets_trk02[0].pt() - jets_trk02[1].pt())/(jets_trk02[0].pt() + jets_trk02[1].pt()))

            self.tree.fill('Jet1_trk02_tau1' , jets_trk02[0].tau1 )
            self.tree.fill('Jet1_trk02_tau2' , jets_trk02[0].tau2 )
            self.tree.fill('Jet1_trk02_tau3' , jets_trk02[0].tau3 )
            self.tree.fill('Jet2_trk02_tau1' , jets_trk02[1].tau1 )
            self.tree.fill('Jet2_trk02_tau2' , jets_trk02[1].tau2 )
            self.tree.fill('Jet2_trk02_tau3' , jets_trk02[1].tau3 )

            Jet1_trk02_tau31 = -999.0
            Jet1_trk02_tau21 = -999.0
            Jet1_trk02_tau32 = -999.0
            Jet2_trk02_tau31 = -999.0
            Jet2_trk02_tau21 = -999.0
            Jet2_trk02_tau32 = -999.0

            if (jets_trk02[0].tau1 != 0.0):
                Jet1_trk02_tau31 = jets_trk02[0].tau3/jets_trk02[0].tau1
                Jet1_trk02_tau21 = jets_trk02[0].tau2/jets_trk02[0].tau1 
            if (jets_trk02[0].tau2 != 0.0):
                Jet1_trk02_tau32 = jets_trk02[0].tau3/jets_trk02[0].tau2

            if (jets_trk02[1].tau1 != 0.0):
                Jet2_trk02_tau31 = jets_trk02[1].tau3/jets_trk02[1].tau1
                Jet2_trk02_tau21 = jets_trk02[1].tau2/jets_trk02[1].tau1
            if (jets_trk02[1].tau2 != 0.0):
                Jet2_trk02_tau32 = jets_trk02[1].tau3/jets_trk02[1].tau2

            self.tree.fill('Jet1_trk02_tau31', Jet1_trk02_tau31)
            self.tree.fill('Jet1_trk02_tau21', Jet1_trk02_tau21)
            self.tree.fill('Jet1_trk02_tau32', Jet1_trk02_tau32)
            self.tree.fill('Jet2_trk02_tau31', Jet2_trk02_tau31)
            self.tree.fill('Jet2_trk02_tau21', Jet2_trk02_tau21)
            self.tree.fill('Jet2_trk02_tau32', Jet2_trk02_tau32)

	    # here is btag, need matching in DR
            Jet1_trk02_dR_pf04 = 999
            Jet2_trk02_dR_pf04 = 999
	    for j in jets_pf04:
                pf04= ROOT.TLorentzVector()
                pf04.SetPtEtaPhiE(j.pt(), j.eta(), j.phi(), j.e())
                if j.tags['bf'] > 0:
                    if pf04.DeltaR(j1)<Jet1_trk02_dR_pf04:
                        Jet1_trk02_dR_pf04=pf04.DeltaR(j1)
                    if pf04.DeltaR(j2)<Jet2_trk02_dR_pf04:
                        Jet2_trk02_dR_pf04=pf04.DeltaR(j2)
            #print 'dr j1  ',Jet1_trk02_dR_pf04
            #print 'dr j2  ',Jet2_trk02_dR_pf04
            
            pdg1 = 0
            pdg2 = 0
            if Jet1_trk02_dR_pf04 < 0.3:
                pdg1 = 5
            if Jet2_trk02_dR_pf04 < 0.3:
                pdg2 = 5

            # TRF / truth b-tagging -> need at least 2 jets_pf04
            use_DELPHES=False
            weight_1tagex=0.
            weight_2tagex=0.
            jet=[]
            ipdg=0
            for i in range(len(jets_pf04)):
              if use_DELPHES==True:
                ipdg = jets_pf04[i].tags['flav']
                if ipdg!=4 and ipdg!=5 : ipdg=0
              else:
                ipdg = jets_pf04_pdg[i].flavour
              jet.append([jets_pf04[i],ipdg])
            if (len(jet)>0): weight_1tagex=getNbTagEx(1,jet,2)
            if (len(jet)>1): weight_2tagex=getNbTagEx(2,jet,2)
            weight_1tagin=weight_1tagex+weight_2tagex
            self.tree.fill('weight_1tagex', weight_1tagex)
            self.tree.fill('weight_2tagex', weight_2tagex)
            self.tree.fill('weight_1tagin', weight_1tagin)

            #MATCHING PF02 and trk02 for CORRECTION
            Jet1_trk02_dR_pf02 = 999
            Jet2_trk02_dR_pf02 = 999
            Jet1_pf02 = None
            Jet2_pf02 = None
            for j in jets_pf02:
                pf02= ROOT.TLorentzVector()
                pf02.SetPtEtaPhiE(j.pt(), j.eta(), j.phi(), j.e())
                if pf02.DeltaR(j1)<Jet1_trk02_dR_pf02:
                    Jet1_trk02_dR_pf02=pf02.DeltaR(j1)
                    Jet1_pf02=j
                if pf02.DeltaR(j2)<Jet2_trk02_dR_pf02:
                    Jet2_trk02_dR_pf02=pf02.DeltaR(j2)
                    Jet2_pf02=j
            #print 'jet1 dr ',Jet1_trk02_dR_pf02,'  pf02   ',Jet1_pf02,'  trk02  ',jets_trk02[0]
            #print 'jet2 dr ',Jet2_trk02_dR_pf02,'  pf02   ',Jet2_pf02,'  trk02  ',jets_trk02[1]

	    corr1 = Jet1_pf02.p4().Pt()/j1.Pt()
	    corr2 = Jet2_pf02.p4().Pt()/j2.Pt()

            #print 'corr 1  ',corr1,'   corr2  ',corr2
            #NORMAL TRK02 SD corrected jet
	    p4sd1 = ROOT.TLorentzVector(); p4sd2 = ROOT.TLorentzVector()
	    p4sd1.SetPtEtaPhiM(jets_trk02[0].subjetsSoftDrop[0].p4().Pt()*corr1, 
	    			jets_trk02[0].eta(), 
	        		jets_trk02[0].phi(), 
	        		jets_trk02[0].subjetsSoftDrop[0].p4().M()*corr1)
	    
	    p4sd2.SetPtEtaPhiM(jets_trk02[1].subjetsSoftDrop[0].p4().Pt()*corr2, 
	    			jets_trk02[1].eta(), 
	        		jets_trk02[1].phi(), 
	        		jets_trk02[1].subjetsSoftDrop[0].p4().M()*corr2)
	    
            sdjet1_corr = Particle(pdg1, 0, p4sd1, 1)
            sdjet2_corr = Particle(pdg2, 0, p4sd2, 1)
            fillParticle(self.tree, 'Jet1_trk02_SD_Corr', sdjet1_corr)
            fillParticle(self.tree, 'Jet2_trk02_SD_Corr', sdjet2_corr)

            #NORMAL TRK02 SD jet
	    #sdjet1 = Particle(pdg1, 0, jets_trk02[0].subjetsSoftDrop[0].p4(), 1)
            #sdjet2 = Particle(pdg2, 0, jets_trk02[1].subjetsSoftDrop[0].p4(), 1)
            #fillParticle(self.tree, 'Jet1_trk02_SD', sdjet1)
            #fillParticle(self.tree, 'Jet2_trk02_SD', sdjet2)

            #CORRECTED TRK02 jet
	    p4jet1_corr = ROOT.TLorentzVector(); p4jet2_corr = ROOT.TLorentzVector()
            p4jet1_corr.SetPtEtaPhiM(jets_trk02[0].pt()*corr1, jets_trk02[0].eta(), jets_trk02[0].phi(), jets_trk02[0].m()*corr1)
	    p4jet2_corr.SetPtEtaPhiM(jets_trk02[1].pt()*corr2, jets_trk02[1].eta(), jets_trk02[1].phi(), jets_trk02[1].m()*corr2)

            jet1_corr = Particle(pdg1, 0, p4jet1_corr, 1)
            jet2_corr = Particle(pdg2, 0, p4jet2_corr, 1)
            #fillParticle(self.tree, 'Jet1_trk02_Corr', jet1_corr)
            #fillParticle(self.tree, 'Jet2_trk02_Corr', jet2_corr)

 
            # associate MET to one jet or another based on softdrop
            sdjetmet1, sdjetmet2 = self.corrMET(jets_trk02[0].subjetsSoftDrop[0], pdg1, jets_trk02[1].subjetsSoftDrop[0], pdg2, event.met)
            fillParticle(self.tree, 'Jet1_trk02_SD_MetCorr', sdjetmet1)
            fillParticle(self.tree, 'Jet2_trk02_SD_MetCorr', sdjetmet2)

            sdjetmet1, sdjetmet2 = self.corrMET(sdjet1_corr, pdg1, sdjet2_corr, pdg2, event.met)
            fillParticle(self.tree, 'Jet1_trk02_SD_Corr_MetCorr', sdjetmet1)
            fillParticle(self.tree, 'Jet2_trk02_SD_Corr_MetCorr', sdjetmet2)

            ######################
            # trkjet04 mass info #
            ######################
            #MATCHING PF04 and trk04 for CORRECTION
            Jet1_trk04_dR_pf04 = 999
            Jet2_trk04_dR_pf04 = 999
            Jet1_pf04 = None
            Jet2_pf04 = None
            for j in jets_pf04_1500:
                pf04= ROOT.TLorentzVector()
                pf04.SetPtEtaPhiE(j.pt(), j.eta(), j.phi(), j.e())
                if pf04.DeltaR(j1)<Jet1_trk04_dR_pf04:
                    Jet1_trk04_dR_pf04=pf04.DeltaR(j1)
                    Jet1_pf04=j
                if pf04.DeltaR(j2)<Jet2_trk04_dR_pf04:
                    Jet2_trk04_dR_pf04=pf04.DeltaR(j2)
                    Jet2_pf04=j
            corr1_04 = Jet1_pf04.p4().Pt()/j1.Pt()
            corr2_04 = Jet2_pf04.p4().Pt()/j2.Pt()

            #NORMAL TRK04 SD corrected jet
            p4sd1_04 = ROOT.TLorentzVector(); p4sd2_04 = ROOT.TLorentzVector()
            Jet1_trk04_SD_Corr_m = -1000.   ; Jet2_trk04_SD_Corr_m = -1000.

            if len(jets_trk04)>=1 :
                p4sd1_04.SetPtEtaPhiM(jets_trk04[0].subjetsSoftDrop[0].p4().Pt()*corr1_04,
                                      jets_trk04[0].eta(),
                                      jets_trk04[0].phi(),
                                      jets_trk04[0].subjetsSoftDrop[0].p4().M()*corr1_04)
                pdg1 = 0
                sdjet1_corr_04 = Particle(pdg1, 0, p4sd1_04, 1)
                Jet1_trk04_SD_Corr_m = sdjet1_corr_04.p4().M()

            if len(jets_trk04)>=2 :
                p4sd2_04.SetPtEtaPhiM(jets_trk04[1].subjetsSoftDrop[0].p4().Pt()*corr2_04,
                                      jets_trk04[1].eta(),
                                      jets_trk04[1].phi(),
                                      jets_trk04[1].subjetsSoftDrop[0].p4().M()*corr2_04)
                pdg2 = 0
                sdjet2_corr_04 = Particle(pdg2, 0, p4sd2_04, 1)
                Jet2_trk04_SD_Corr_m = sdjet2_corr_04.p4().M()

            self.tree.fill('Jet1_trk04_SD_Corr_m', Jet1_trk04_SD_Corr_m)
            self.tree.fill('Jet2_trk04_SD_Corr_m', Jet2_trk04_SD_Corr_m)

            ######################
            # trkjet08 mass info #
            ######################
            #MATCHING PF08 and trk08 for CORRECTION
            Jet1_trk08_dR_pf08 = 999
            Jet2_trk08_dR_pf08 = 999
            Jet1_pf08 = None
            Jet2_pf08 = None
            for j in jets_pf08:
                pf08= ROOT.TLorentzVector()
                pf08.SetPtEtaPhiE(j.pt(), j.eta(), j.phi(), j.e())
                if pf08.DeltaR(j1)<Jet1_trk08_dR_pf08:
                    Jet1_trk08_dR_pf08=pf08.DeltaR(j1)
                    Jet1_pf08=j
                if pf08.DeltaR(j2)<Jet2_trk08_dR_pf08:
                    Jet2_trk08_dR_pf08=pf08.DeltaR(j2)
                    Jet2_pf08=j
            corr1_08 = Jet1_pf08.p4().Pt()/j1.Pt()
            corr2_08 = Jet2_pf08.p4().Pt()/j2.Pt()

            #NORMAL TRK08 SD corrected jet
            p4sd1_08 = ROOT.TLorentzVector(); p4sd2_08 = ROOT.TLorentzVector()
            Jet1_trk08_SD_Corr_m = -1000.   ; Jet2_trk08_SD_Corr_m = -1000.

            if len(jets_trk08)>=1 :
                p4sd1_08.SetPtEtaPhiM(jets_trk08[0].subjetsSoftDrop[0].p4().Pt()*corr1_08,
                                      jets_trk08[0].eta(),
                                      jets_trk08[0].phi(),
                                      jets_trk08[0].subjetsSoftDrop[0].p4().M()*corr1_08)
                pdg1 = 0
                sdjet1_corr_08 = Particle(pdg1, 0, p4sd1_08, 1)
                Jet1_trk08_SD_Corr_m = sdjet1_corr_08.p4().M()

            if len(jets_trk08)>=2 :
                p4sd2_08.SetPtEtaPhiM(jets_trk08[1].subjetsSoftDrop[0].p4().Pt()*corr2_08,
                                      jets_trk08[1].eta(),
                                      jets_trk08[1].phi(),
                                      jets_trk08[1].subjetsSoftDrop[0].p4().M()*corr2_08)
                pdg2 = 0
                sdjet2_corr_08 = Particle(pdg2, 0, p4sd2_08, 1)
                Jet2_trk08_SD_Corr_m = sdjet2_corr_08.p4().M()

            self.tree.fill('Jet1_trk08_SD_Corr_m', Jet1_trk08_SD_Corr_m)
            self.tree.fill('Jet2_trk08_SD_Corr_m', Jet2_trk08_SD_Corr_m)

            if (len(jets_trk02)>1): 
                self.tree.fill( 'Mj1j2_trk02',self.fillMass(jets_trk02[0],jets_trk02[1]))
                self.tree.fill( 'Mj1j2_trk02_Corr',self.fillMass(jet1_corr,jet2_corr))
                jetmet1, jetmet2 = self.corrMET(jets_trk02[0], pdg1, jets_trk02[1], pdg2, event.met)
                self.tree.fill( 'Mj1j2_trk02_MetCorr',self.fillMass(jetmet1,jetmet2))
                #fillParticle(self.tree, 'Jet1_trk02_MetCorr', jetmet1)
                #fillParticle(self.tree, 'Jet2_trk02_MetCorr', jetmet2)

                jetmet1, jetmet2 = self.corrMET(jet1_corr, pdg1, jet2_corr, pdg2, event.met)
                self.tree.fill( 'Mj1j2_trk02_Corr_MetCorr',self.fillMass(jetmet1,jetmet2))
                fillParticle(self.tree, 'Jet1_trk02_Corr_MetCorr', jetmet1)
                fillParticle(self.tree, 'Jet2_trk02_Corr_MetCorr', jetmet2)

            if (len(jets_pf02)>1):  
                self.tree.fill( 'Mj1j2_pf02', self.fillMass(jets_pf02[0],jets_pf02[1]))
                jetmet1, jetmet2 = self.corrMET(jets_pf02[0], pdg1, jets_pf02[1], pdg2, event.met)
                self.tree.fill( 'Mj1j2_pf02_MetCorr', self.fillMass(jetmet1,jetmet2))

            if (len(jets_pf04)>1):  
                self.tree.fill( 'Mj1j2_pf04', self.fillMass(jets_pf04[0],jets_pf04[1]))
                jetmet1, jetmet2 = self.corrMET(jets_pf04[0], pdg1, jets_pf04[1], pdg2, event.met)
                self.tree.fill( 'Mj1j2_pf04_MetCorr', self.fillMass(jetmet1,jetmet2))

            if (len(jets_pf08)>1):  
                self.tree.fill( 'Mj1j2_pf08', self.fillMass(jets_pf08[0],jets_pf08[1]))
                jetmet1, jetmet2 = self.corrMET(jets_pf08[0], pdg1, jets_pf08[1], pdg2, event.met)
                self.tree.fill( 'Mj1j2_pf08_MetCorr', self.fillMass(jetmet1,jetmet2))





            if ( len(electrons) >=1 ): fillParticle(self.tree, 'Electron1', electrons[0])
            if ( len(electrons) >=2 ): fillParticle(self.tree, 'Electron2', electrons[1])

            if ( len(muons) >=1 ): fillParticle(self.tree, 'Muon1', muons[0])
            if ( len(muons) >=2 ): fillParticle(self.tree, 'Muon2', muons[1])

            ###################################
            #TMVA Stuff Starts!
            ###################################

            self.bdt_Jet_trk02_tau1[0] = jets_trk02[0].tau1
            self.bdt_Jet_trk02_tau2[0] = jets_trk02[0].tau2
            self.bdt_Jet_trk02_tau3[0] = jets_trk02[0].tau3
            self.bdt_Jet_trk02_tau21[0] = Jet1_trk02_tau21
            self.bdt_Jet_trk02_tau31[0] = Jet1_trk02_tau31
            self.bdt_Jet_trk02_tau32[0] = Jet1_trk02_tau32
            self.bdt_Jet_trk02_SD_Corr_m[0]  = sdjet1_corr.p4().M()
            if len(jets_trk04)>=1 : self.bdt_Jet_trk04_SD_Corr_m[0] = sdjet1_corr_04.p4().M()
            else                  : self.bdt_Jet_trk04_SD_Corr_m[0] = -1000.
            if len(jets_trk08)>=1 : self.bdt_Jet_trk08_SD_Corr_m[0] = sdjet1_corr_08.p4().M()
            else                  : self.bdt_Jet_trk08_SD_Corr_m[0] = -1000.
            mva_value = self.reader.EvaluateMVA("BDT")
            self.tree.fill( 'Jet1_thad_vs_QCD_tagger', mva_value)
            #
            self.bdt_Jet_trk02_tau1[0] = jets_trk02[1].tau1
            self.bdt_Jet_trk02_tau2[0] = jets_trk02[1].tau2
            self.bdt_Jet_trk02_tau3[0] = jets_trk02[1].tau3
            self.bdt_Jet_trk02_tau21[0] = Jet2_trk02_tau21
            self.bdt_Jet_trk02_tau31[0] = Jet2_trk02_tau31
            self.bdt_Jet_trk02_tau32[0] = Jet2_trk02_tau32
            self.bdt_Jet_trk02_SD_Corr_m[0]  = sdjet2_corr.p4().M()
            if len(jets_trk04)>=2 : self.bdt_Jet_trk04_SD_Corr_m[0] = sdjet2_corr_04.p4().M()
            else                  : self.bdt_Jet_trk04_SD_Corr_m[0] = -1000.
            if len(jets_trk08)>=2 : self.bdt_Jet_trk08_SD_Corr_m[0] = sdjet2_corr_08.p4().M()
            else                  : self.bdt_Jet_trk08_SD_Corr_m[0] = -1000.
            mva_value = self.reader.EvaluateMVA("BDT")
            self.tree.fill( 'Jet2_thad_vs_QCD_tagger', mva_value)

            self.tree.tree.Fill()

    def write(self, setup):
        self.rootfile.Write()
        self.rootfile.Close()

