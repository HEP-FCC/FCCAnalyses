from heppy.framework.analyzer import Analyzer
from heppy.statistics.tree import Tree
from heppy.analyzers.ntuple import *
from heppy.particles.tlv.resonance import Resonance2 as Resonance

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
        
	self.tree.var('Jet1_tau1', float)	
	self.tree.var('Jet1_tau2', float)
        self.tree.var('Jet1_tau3', float)
        self.tree.var('Jet2_tau1', float)
        self.tree.var('Jet2_tau2', float)
        self.tree.var('Jet2_tau3', float)
	self.tree.var('Jet1_tau32', float)
        self.tree.var('Jet1_tau31', float)
        self.tree.var('Jet1_tau21', float)
        self.tree.var('Jet2_tau32', float)
        self.tree.var('Jet2_tau31', float)
        self.tree.var('Jet2_tau21', float)

        bookParticle(self.tree, 'Jet1')
        bookParticle(self.tree, 'Jet2')

	bookParticle(self.tree, 'softDroppedJet1')
	bookParticle(self.tree, 'softDroppedJet2')
        
	bookParticle(self.tree, 'trimmedJet1')
        bookParticle(self.tree, 'trimmedJet2')

	bookParticle(self.tree, 'prunedJet1')
        bookParticle(self.tree, 'prunedJet2')

	self.tree.var('zPrimeReconstructedMass', float)
	self.tree.var('zPrimeReconstructedMass_trimmed', float)
	self.tree.var('zPrimeReconstructedMass_softDropped', float)
	self.tree.var('zPrimeReconstructedMass_pruned', float)

	self.tree.var('rapiditySeparation', float)
	self.tree.var('transverseMomentumAsymmetry', float)

    def process(self, event):
        self.tree.reset()
        jets = getattr(event, self.cfg_ana.fatjets)

	if (len(jets) > 1):
	
	    self.tree.fill('weight' , event.weight )

	    self.tree.fill('rapiditySeparation', abs(jets[0].eta() - jets[1].eta()))
	    self.tree.fill('transverseMomentumAsymmetry', (jets[0].pt() - jets[1].pt())/(jets[0].pt() + jets[1].pt()))

	    self.tree.fill('Jet1_tau1' , jets[0].tau1 )
            self.tree.fill('Jet1_tau2' , jets[0].tau2 )
            self.tree.fill('Jet1_tau3' , jets[0].tau3 )
            self.tree.fill('Jet2_tau1' , jets[1].tau1 )
            self.tree.fill('Jet2_tau2' , jets[1].tau2 )
            self.tree.fill('Jet2_tau3' , jets[1].tau3 )

	    if (jets[0].tau1 != 0.0):
	        self.tree.fill('Jet1_tau31' , jets[0].tau3/jets[0].tau1 )
                self.tree.fill('Jet1_tau21' , jets[0].tau2/jets[0].tau1 )
            else:
		self.tree.fill('Jet1_tau31' , -99)
                self.tree.fill('Jet1_tau21' , -99)

            if (jets[0].tau2 != 0.0):
		self.tree.fill('Jet1_tau32', jets[0].tau3/jets[0].tau2)
	    else:
		self.tree.fill('Jet1_tau32', -99)

	    if (jets[1].tau1 != 0.0):
                self.tree.fill('Jet2_tau31' , jets[1].tau3/jets[1].tau1 )
                self.tree.fill('Jet2_tau21' , jets[1].tau2/jets[1].tau1 )
            else:
                self.tree.fill('Jet2_tau31' , -99)
                self.tree.fill('Jet2_tau21' , -99)

	    if (jets[1].tau2 != 0.0):
                self.tree.fill('Jet2_tau32', jets[1].tau3/jets[1].tau2)
            else:
                self.tree.fill('Jet2_tau32', -99)

            fillParticle(self.tree, 'Jet1', jets[0])
	    fillParticle(self.tree, 'Jet2', jets[1])

	    fillParticle(self.tree, 'softDroppedJet1', jets[0].subjetsSoftDrop[0])
	    fillParticle(self.tree, 'softDroppedJet2', jets[1].subjetsSoftDrop[0])
           
            fillParticle(self.tree, 'trimmedJet1', jets[0].subjetsTrimming[0])
            fillParticle(self.tree, 'trimmedJet2', jets[1].subjetsTrimming[0])
            
            fillParticle(self.tree, 'prunedJet1', jets[0].subjetsPruning[0])
            fillParticle(self.tree, 'prunedJet2', jets[1].subjetsPruning[0])

	    t1_ungroomed = ROOT.TLorentzVector(); t2_ungroomed = ROOT.TLorentzVector()
            t1_ungroomed.SetPtEtaPhiE(jets[0].pt(), jets[0].eta(), jets[0].phi(), jets[0].e())
            t2_ungroomed.SetPtEtaPhiE(jets[1].pt(), jets[1].eta(), jets[1].phi(), jets[1].e())
            self.tree.fill('zPrimeReconstructedMass', (t1_ungroomed+t2_ungroomed).M())            

            t1_trimmed = ROOT.TLorentzVector(); t2_trimmed = ROOT.TLorentzVector()
            t1_trimmed.SetPtEtaPhiE(jets[0].subjetsTrimming[0].pt(), 
                                    jets[0].subjetsTrimming[0].eta(), 
                                    jets[0].subjetsTrimming[0].phi(), 
                                    jets[0].subjetsTrimming[0].e())
            t2_trimmed.SetPtEtaPhiE(jets[1].subjetsTrimming[0].pt(),
                                    jets[1].subjetsTrimming[0].eta(),
                                    jets[1].subjetsTrimming[0].phi(),
                                    jets[1].subjetsTrimming[0].e())
            self.tree.fill('zPrimeReconstructedMass_trimmed', (t1_trimmed+t2_trimmed).M())

            t1_pruned = ROOT.TLorentzVector(); t2_pruned = ROOT.TLorentzVector()
            t1_pruned.SetPtEtaPhiE(jets[0].subjetsPruning[0].pt(),
                                   jets[0].subjetsPruning[0].eta(),
                                   jets[0].subjetsPruning[0].phi(),
                                   jets[0].subjetsPruning[0].e())
            t2_pruned.SetPtEtaPhiE(jets[1].subjetsPruning[0].pt(),
                                   jets[1].subjetsPruning[0].eta(),
                                   jets[1].subjetsPruning[0].phi(),
                                   jets[1].subjetsPruning[0].e())
            self.tree.fill('zPrimeReconstructedMass_pruned', (t1_pruned+t2_pruned).M())

            t1_softDropped = ROOT.TLorentzVector(); t2_softDropped = ROOT.TLorentzVector()
            t1_softDropped.SetPtEtaPhiE(jets[0].subjetsSoftDrop[0].pt(),
                                        jets[0].subjetsSoftDrop[0].eta(),
                                        jets[0].subjetsSoftDrop[0].phi(),
                                        jets[0].subjetsSoftDrop[0].e())
            t2_softDropped.SetPtEtaPhiE(jets[1].subjetsSoftDrop[0].pt(),
                                        jets[1].subjetsSoftDrop[0].eta(),
                                        jets[1].subjetsSoftDrop[0].phi(),
                                        jets[1].subjetsSoftDrop[0].e())
            self.tree.fill('zPrimeReconstructedMass_softDropped', (t1_softDropped+t2_softDropped).M())

	    self.tree.tree.Fill()

    def write(self, setup):
        self.rootfile.Write()
        self.rootfile.Close()

