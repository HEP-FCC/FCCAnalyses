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

        ######################
        # event categorization
        # -> 0 fully hadronic decay
        # -> 1 fully hadronic decay (semi-leptonic decays)
        # -> 2 leptonic decay
        self.tree.var('fullhad_fullhadsemilep_lep_decays', float)

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

        jets_pf04_1500 = getattr(event, self.cfg_ana.jets_pf04_1500)
        jets_trk04 = getattr(event, self.cfg_ana.jets_trk04_1000)
        jets_trk08 = getattr(event, self.cfg_ana.jets_trk08_1000)

        electrons = getattr(event, self.cfg_ana.electrons)
        muons = getattr(event, self.cfg_ana.muons)

        if ( len(jets_trk02)>=2 and  len(jets_pf02)>=2):

            	j1 = ROOT.TLorentzVector(); j2 = ROOT.TLorentzVector()
            	j1.SetPtEtaPhiE(jets_trk02[0].pt(), jets_trk02[0].eta(), jets_trk02[0].phi(), jets_trk02[0].e())
            	j2.SetPtEtaPhiE(jets_trk02[1].pt(), jets_trk02[1].eta(), jets_trk02[1].phi(), jets_trk02[1].e())
            	n_had=0
            	n_hadsemilep=0
            	n_lep=0
            	if ( len(electrons)==0 and len(muons)==0 ): n_had+=1
            	for i in range(len(electrons)):
            	    e = ROOT.TLorentzVector()
            	    e.SetPtEtaPhiE(electrons[i].pt(), electrons[i].eta(), electrons[i].phi(), electrons[i].e())
            	    if j1.DeltaR(e)<=0.2 or j2.DeltaR(e)<=0.2 : n_hadsemilep+=1
            	    if j1.DeltaR(e)>0.2 and j2.DeltaR(e)>0.2  : n_lep+=1
            	for i in range(len(muons)):
            	    m = ROOT.TLorentzVector()
            	    m.SetPtEtaPhiE(muons[i].pt(), muons[i].eta(), muons[i].phi(), muons[i].e())
            	    if j1.DeltaR(m)<=0.2 or j2.DeltaR(m)<=0.2 : n_hadsemilep+=1
            	    if j1.DeltaR(m)>0.2 and j2.DeltaR(m)>0.2  : n_lep+=1
            	fullhad_fullhadsemilep_lep_decays=-1
            	if   n_had>0  and n_hadsemilep==0 and n_lep==0 : fullhad_fullhadsemilep_lep_decays=0.
            	elif n_had==0 and n_hadsemilep>0  and n_lep==0 : fullhad_fullhadsemilep_lep_decays=1.
            	elif n_had==0 and n_hadsemilep>=0 and n_lep>0  : fullhad_fullhadsemilep_lep_decays=2.
            	#print "n_had="+str(n_had)+" , n_hadsemilep="+str(n_hadsemilep)+" , n_lep="+str(n_lep)+" -> had_hadsemilep_lep_decays="+str(fullhad_fullhadsemilep_lep_decays)
            	self.tree.fill('fullhad_fullhadsemilep_lep_decays' , fullhad_fullhadsemilep_lep_decays )

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
		
				
                R = 0.05

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

                self.tree.tree.Fill()


    def write(self, setup):
        self.rootfile.Write()
        self.rootfile.Close()

