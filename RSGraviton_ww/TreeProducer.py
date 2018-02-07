from __future__ import division
from heppy.framework.analyzer import Analyzer
from heppy.statistics.tree import Tree
from heppy.analyzers.ntuple import *
from heppy.particles.tlv.resonance import Resonance2 as Resonance
from heppy.particles.tlv.particle import Particle

from numpy import sign
import sys

import ROOT
from ROOT import *
import array
import os

#ROOT.gROOT.ProcessLine(".L /afs/cern.ch/work/s/selvaggi/private/FCCSW/heppy/FCChhAnalyses/RSGraviton_ww/BDT_QCD.class.C+")

class TreeProducer(Analyzer):

    def beginLoop(self, setup):
        super(TreeProducer, self).beginLoop(setup)
        self.rootfile = TFile('/'.join([self.dirName,
                                        'tree.root']),
                              'recreate')
        self.tree = Tree( 'events', '')


        self.tree.var('weight', float)
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


        self.tree.var('rapiditySeparation_trk02', float)
        self.tree.var('transverseMomentumAsymmetry_trk02', float)
        self.tree.var('topJetMassDifference', float)

        bookParticle(self.tree, 'Jet1_trk02_SD_Corr')
        bookParticle(self.tree, 'Jet2_trk02_SD_Corr')

        bookParticle(self.tree, 'Electron1')
        bookParticle(self.tree, 'Electron2')

        bookParticle(self.tree, 'Muon1')
        bookParticle(self.tree, 'Muon2')

        #self.tree.var('BDTvariable_qcd', float)

        self.tree.var('Mj1j2_trk02', float)
        self.tree.var('Mj1j2_trk02_Corr', float)
        self.tree.var('Mj1j2_pf02', float)
        self.tree.var('Mj1j2_pf04', float)
        self.tree.var('Mj1j2_pf08', float)

	self.tree.var('Jet1_Flow15',float)
	self.tree.var('Jet1_Flow25',float)
	self.tree.var('Jet1_Flow35',float)
	self.tree.var('Jet1_Flow45',float)
	self.tree.var('Jet1_Flow55',float)
	self.tree.var('Jet2_Flow15',float)
	self.tree.var('Jet2_Flow25',float)
	self.tree.var('Jet2_Flow35',float)
	self.tree.var('Jet2_Flow45',float)
	self.tree.var('Jet2_Flow55',float)
	

	self.tree.var('rapiditySeparation', float)
        self.tree.var('transverseMomentumAsymmetry', float)

        # for MVA
        self.reader = ROOT.TMVA.Reader()
        self.bdt_Jet1_trk02_tau32 = array.array('f',[0])
        self.bdt_Jet1_trk02_tau31 = array.array('f',[0])
        self.bdt_Jet1_trk02_tau21 = array.array('f',[0])
        self.bdt_Jet1_trk02_SD_Corr_m = array.array('f',[0])
        self.bdt_Jet1_trk02_SD_Corr_pt = array.array('f',[0])
        self.bdt_Jet1_Flow15 = array.array('f',[0])
        self.bdt_Jet1_Flow25 = array.array('f',[0])
        self.bdt_Jet1_Flow35 = array.array('f',[0])
        self.bdt_Jet1_Flow45 = array.array('f',[0])
        self.bdt_Jet1_Flow55 = array.array('f',[0])
        self.bdt_Jet2_trk02_tau32 = array.array('f',[0])
        self.bdt_Jet2_trk02_tau31 = array.array('f',[0])
        self.bdt_Jet2_trk02_tau21 = array.array('f',[0])
        self.bdt_Jet2_trk02_SD_Corr_m = array.array('f',[0])
        self.bdt_Jet2_trk02_SD_Corr_pt = array.array('f',[0])
        self.bdt_Jet2_Flow15 = array.array('f',[0])
        self.bdt_Jet2_Flow25 = array.array('f',[0])
        self.bdt_Jet2_Flow35 = array.array('f',[0])
        self.bdt_Jet2_Flow45 = array.array('f',[0])
        self.bdt_Jet2_Flow55 = array.array('f',[0])
        self.bdt_rapiditySeparation_trk02 = array.array('f',[0])
        self.bdt_transverseMomentumAsymmetry_trk02 = array.array('f',[0])
        self.reader.AddVariable("Jet1_trk02_tau32",         self.bdt_Jet1_trk02_tau32        )
        self.reader.AddVariable("Jet1_trk02_tau31",         self.bdt_Jet1_trk02_tau31        )
        self.reader.AddVariable("Jet1_trk02_tau21",         self.bdt_Jet1_trk02_tau21        )
        self.reader.AddVariable("Jet1_trk02_SD_Corr_m",     self.bdt_Jet1_trk02_SD_Corr_m    )
        self.reader.AddVariable("Jet1_trk02_SD_Corr_pt",    self.bdt_Jet1_trk02_SD_Corr_pt   )
        self.reader.AddVariable("Jet1_Flow15",              self.bdt_Jet1_Flow15             )
        self.reader.AddVariable("Jet1_Flow25",              self.bdt_Jet1_Flow25             )
        self.reader.AddVariable("Jet1_Flow35",              self.bdt_Jet1_Flow35             )
        self.reader.AddVariable("Jet1_Flow45",              self.bdt_Jet1_Flow45             )
        self.reader.AddVariable("Jet1_Flow55",              self.bdt_Jet1_Flow55             )
        self.reader.AddVariable("Jet2_trk02_tau32",         self.bdt_Jet2_trk02_tau32        )
        self.reader.AddVariable("Jet2_trk02_tau31",         self.bdt_Jet2_trk02_tau31        )
        self.reader.AddVariable("Jet2_trk02_tau21",         self.bdt_Jet2_trk02_tau21        )
        self.reader.AddVariable("Jet2_trk02_SD_Corr_m",     self.bdt_Jet2_trk02_SD_Corr_m    )
        self.reader.AddVariable("Jet2_trk02_SD_Corr_pt",    self.bdt_Jet2_trk02_SD_Corr_pt   )
        self.reader.AddVariable("Jet2_Flow15",              self.bdt_Jet2_Flow15             )
        self.reader.AddVariable("Jet2_Flow25",              self.bdt_Jet2_Flow25             )
        self.reader.AddVariable("Jet2_Flow35",              self.bdt_Jet2_Flow35             )
        self.reader.AddVariable("Jet2_Flow45",              self.bdt_Jet2_Flow45             )
        self.reader.AddVariable("Jet2_Flow55",              self.bdt_Jet2_Flow55             )
        self.reader.AddVariable("rapiditySeparation_trk02", self.bdt_rapiditySeparation_trk02)
        self.reader.AddVariable("transverseMomentumAsymmetry_trk02",self.bdt_transverseMomentumAsymmetry_trk02)
        path = "/afs/cern.ch/user/d/djamin/fcc_work/BDT_trains/20180207_MVAqcd/"
        self.reader.BookMVA("BDT",str(path)+"BDT_BDT_RSGraviton_ww_M_20TeV.weights.xml")
        self.tree.var('BDTvariable_qcd', float)

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
        jets_pf08 = getattr(event, self.cfg_ana.jets_pf08_1500)

        jets_trk08 = getattr(event, self.cfg_ana.jets_trk08_1000)

        electrons = getattr(event, self.cfg_ana.electrons)
        muons = getattr(event, self.cfg_ana.muons)

        if ( len(jets_trk02)>=2 and  len(jets_pf02)>=2):

		self.tree.fill('weight' , event.weight )
                self.tree.fill('rapiditySeparation_trk02', abs(jets_trk02[0].eta() - jets_trk02[1].eta()))
                self.tree.fill('transverseMomentumAsymmetry_trk02', (jets_trk02[0].pt() - jets_trk02[1].pt())/(jets_trk02[0].pt() + jets_trk02[1].pt()))

                self.tree.fill('Jet1_trk02_tau1' , jets_trk02[0].tau1 )
                self.tree.fill('Jet1_trk02_tau2' , jets_trk02[0].tau2 )
                self.tree.fill('Jet1_trk02_tau3' , jets_trk02[0].tau3 )
                self.tree.fill('Jet2_trk02_tau1' , jets_trk02[1].tau1 )
                self.tree.fill('Jet2_trk02_tau2' , jets_trk02[1].tau2 )
                self.tree.fill('Jet2_trk02_tau3' , jets_trk02[1].tau3 )

                self.tree.fill('numberOfElectrons', len(electrons))
                self.tree.fill('numberOfMuons', len(muons))

                if ( len(muons) >=1 ): fillParticle(self.tree, 'Muon1', muons[0])
                if ( len(muons) >=2 ): fillParticle(self.tree, 'Muon2', muons[1])

                Jet1_trk02_tau31 = -9.0
                Jet1_trk02_tau21 = -9.0
                Jet1_trk02_tau32 = -9.0
                Jet2_trk02_tau31 = -9.0
                Jet2_trk02_tau21 = -9.0
                Jet2_trk02_tau32 = -9.0
                
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

                
                j1 = ROOT.TLorentzVector(); j2 = ROOT.TLorentzVector()
                j1.SetPtEtaPhiE(jets_trk02[0].pt(), jets_trk02[0].eta(), jets_trk02[0].phi(), jets_trk02[0].e())
                j2.SetPtEtaPhiE(jets_trk02[1].pt(), jets_trk02[1].eta(), jets_trk02[1].phi(), jets_trk02[1].e())

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
                
                pdg1 = 0
                pdg2 = 0
                sdjet1_corr = Particle(pdg1, 0, p4sd1, 1)
                sdjet2_corr = Particle(pdg2, 0, p4sd2, 1)
                fillParticle(self.tree, 'Jet1_trk02_SD_Corr', sdjet1_corr)
                fillParticle(self.tree, 'Jet2_trk02_SD_Corr', sdjet2_corr)

            #CORRECTED TRK02 jet
                p4jet1_corr = ROOT.TLorentzVector(); p4jet2_corr = ROOT.TLorentzVector()
                p4jet1_corr.SetPtEtaPhiM(jets_trk02[0].pt()*corr1, jets_trk02[0].eta(), jets_trk02[0].phi(), jets_trk02[0].m()*corr1)
                p4jet2_corr.SetPtEtaPhiM(jets_trk02[1].pt()*corr2, jets_trk02[1].eta(), jets_trk02[1].phi(), jets_trk02[1].m()*corr2)

                jet1_corr = Particle(pdg1, 0, p4jet1_corr, 1)
                jet2_corr = Particle(pdg2, 0, p4jet2_corr, 1)

                if (len(jets_trk02)>1): 
                    self.tree.fill( 'Mj1j2_trk02',self.fillMass(jets_trk02[0],jets_trk02[1]))
                    self.tree.fill( 'Mj1j2_trk02_Corr',self.fillMass(jet1_corr,jet2_corr))

                if (len(jets_pf02)>1):  
                    self.tree.fill( 'Mj1j2_pf02', self.fillMass(jets_pf02[0],jets_pf02[1]))
                
                if (len(jets_pf04)>1):  
                    self.tree.fill( 'Mj1j2_pf04', self.fillMass(jets_pf04[0],jets_pf04[1]))

                if (len(jets_pf08)>1):  
                    self.tree.fill( 'Mj1j2_pf08', self.fillMass(jets_pf08[0],jets_pf08[1]))

		
		#Flow n,5
		#############################################################################
                #REQUIRES THE FOLLOWING IN heppy/analyzers/fcc/Reader.py AFTER LINE 151:
		
		#	particle_relations = defaultdict(list)
        	#       for tjet in store.get(self.cfg_ana.fatjets):
                #		for i in range(tjet.particles_size()):
                #     			particle_relations[Jet(tjet)].append(Particle(tjet.particles(i)))
            	#	for fatjet, particles in particle_relations.items():
                # 		fatjets[fatjet].jetConstituents = particles 

		#############################################################################
		
				
		#R = 0.8 # init
                R = 0.2

		flow_Jet1 = [0]*5
		flow_Jet2 = [0]*5
                if len( jets_pf08)<2:return
                jet1_ungroomed = ROOT.TLorentzVector(); jet2_ungroomed = ROOT.TLorentzVector()
		jet1_ungroomed.SetPtEtaPhiE(jets_pf08[0].pt(), jets_pf08[0].eta(), jets_pf08[0].phi(), jets_pf08[0].e())
		jet2_ungroomed.SetPtEtaPhiE(jets_pf08[1].pt(), jets_pf08[1].eta(), jets_pf08[1].phi(), jets_pf08[1].e())

		constituent_vector = ROOT.TLorentzVector()
		for n in range(1,5+1):
                    for constituent in jets_pf08[0].jetConstituents[1:]:
                        constituent_vector.SetPtEtaPhiE(constituent.pt(),constituent.eta(),constituent.phi(),constituent.e())
                        dR = jet1_ungroomed.DeltaR(constituent_vector)
                        if ((dR >= (n-1)/5*R) and (dR < n/5*R)):
                            flow_Jet1[n-1] += abs(constituent.pt())/abs(jets_pf08[0].pt())
                    for constituent in jets_pf08[1].jetConstituents[1:]:
                        constituent_vector.SetPtEtaPhiE(constituent.pt(),constituent.eta(),constituent.phi(),constituent.e())
                        dR = jet2_ungroomed.DeltaR(constituent_vector)
                        if ((dR >= (n-1)/5*R) and (dR < n/5*R)):
                            flow_Jet2[n-1] += abs(constituent.pt())/abs(jets_pf08[1].pt())

		self.tree.fill('Jet1_Flow15', flow_Jet1[0]); self.tree.fill('Jet2_Flow15', flow_Jet2[0])
		self.tree.fill('Jet1_Flow25', flow_Jet1[1]); self.tree.fill('Jet2_Flow25', flow_Jet2[1])
		self.tree.fill('Jet1_Flow35', flow_Jet1[2]); self.tree.fill('Jet2_Flow35', flow_Jet2[2])
		self.tree.fill('Jet1_Flow45', flow_Jet1[3]); self.tree.fill('Jet2_Flow45', flow_Jet2[3])
		self.tree.fill('Jet1_Flow55', flow_Jet1[4]); self.tree.fill('Jet2_Flow55', flow_Jet2[4])
		
		#varlist = [ 
		#		"Jet1_pt",
		#		"Jet1_tau21",
		#		"Jet1_tau32",
		#		"Jet1_Flow15",
		#		"Jet1_Flow25",
		#		"Jet1_Flow35",
		#		"Jet1_Flow45",
		#		"Jet1_Flow55",
		#		"softDroppedJet1_m",
		#]

		#inputs = ROOT.vector('string')()
		#for v in varlist:
		#	inputs.push_back(v)

		#mva = ROOT.ReadQCD(inputs)
		#values = ROOT.vector('double')()

		#values.push_back(jets[0].pt())
		#values.push_back(Jet1_tau21)
		#values.push_back(Jet1_tau32)
		#values.push_back(flow_Jet1[0]) 
		#values.push_back(flow_Jet1[1])
		#values.push_back(flow_Jet1[2])
		#values.push_back(flow_Jet1[3])
		#values.push_back(flow_Jet1[4])        
		#values.push_back(jets[0].subjetsSoftDrop[0].m())
         
   
		#mva_value=mva.GetMvaValue(values)
		#self.tree.fill('BDTvariable_qcd', mva_value)

                jet1_sdcorr = Particle(pdg1, 0, p4sd1, 1)
                jet2_sdcorr = Particle(pdg2, 0, p4sd2, 1)
                #
                self.bdt_Jet1_trk02_tau32[0] = Jet1_trk02_tau32
                self.bdt_Jet1_trk02_tau31[0] = Jet1_trk02_tau31
                self.bdt_Jet1_trk02_tau21[0] = Jet1_trk02_tau21
                self.bdt_Jet1_trk02_SD_Corr_m[0]  = jet1_sdcorr.p4().M()
                self.bdt_Jet1_trk02_SD_Corr_pt[0] = jet1_sdcorr.p4().Pt()
                self.bdt_Jet1_Flow15[0] = flow_Jet1[0]
                self.bdt_Jet1_Flow25[0] = flow_Jet1[1]
                self.bdt_Jet1_Flow35[0] = flow_Jet1[2]
                self.bdt_Jet1_Flow45[0] = flow_Jet1[3]
                self.bdt_Jet1_Flow55[0] = flow_Jet1[4]
                self.bdt_Jet2_trk02_tau32[0] = Jet2_trk02_tau32
                self.bdt_Jet2_trk02_tau31[0] = Jet2_trk02_tau31
                self.bdt_Jet2_trk02_tau21[0] = Jet2_trk02_tau21
                self.bdt_Jet2_trk02_SD_Corr_m[0]  = jet2_sdcorr.p4().M()
                self.bdt_Jet2_trk02_SD_Corr_pt[0] = jet2_sdcorr.p4().Pt()
                self.bdt_Jet2_Flow15[0] = flow_Jet2[0]
                self.bdt_Jet2_Flow25[0] = flow_Jet2[1]
                self.bdt_Jet2_Flow35[0] = flow_Jet2[2]
                self.bdt_Jet2_Flow45[0] = flow_Jet2[3]
                self.bdt_Jet2_Flow55[0] = flow_Jet2[4]
                self.bdt_rapiditySeparation_trk02[0] = abs(jets_trk02[0].eta() - jets_trk02[1].eta())
                self.bdt_transverseMomentumAsymmetry_trk02[0] = (jets_trk02[0].pt() - jets_trk02[1].pt())/(jets_trk02[0].pt() + jets_trk02[1].pt())
                #
                mva_value = self.reader.EvaluateMVA("BDT")
                self.tree.fill( 'BDTvariable_qcd', mva_value)


                self.tree.tree.Fill()


    def write(self, setup):
        self.rootfile.Write()
        self.rootfile.Close()

