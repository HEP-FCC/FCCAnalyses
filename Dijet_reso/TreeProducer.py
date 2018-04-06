from __future__ import division
from heppy.framework.analyzer import Analyzer
from heppy.statistics.tree import Tree
from heppy.analyzers.ntuple import *
from heppy.particles.tlv.resonance import Resonance2 as Resonance
from heppy.particles.tlv.particle import Particle

import math
import ROOT
from ROOT import *
import collections
from array import array

class TreeProducer(Analyzer):

    def beginLoop(self, setup):
        super(TreeProducer, self).beginLoop(setup)
        self.rootfile = TFile('/'.join([self.dirName,
                                        'tree.root']),
                              'recreate')
        self.tree = Tree( 'events', '')
        
        self.tree.var('weight', float)
        self.tree.var('missingET', float)

        self.tree.var('rapiditySeparation_calo04', float)
        self.tree.var('pseudorapiditySeparation_calo04', float)
        self.tree.var('transverseMomentumAsymmetry_calo04', float)

        self.tree.var('rapiditySeparation_pf04', float)
        self.tree.var('pseudorapiditySeparation_pf04', float)
        self.tree.var('transverseMomentumAsymmetry_pf04', float)

        bookParticle(self.tree, 'Jet1_pf04')
        bookParticle(self.tree, 'Jet2_pf04')

        bookParticle(self.tree, 'Jet1_calo04')
        bookParticle(self.tree, 'Jet2_calo04')

        self.tree.var('Mj1j2_pf04', float)
        self.tree.var('Mj1j2_calo04', float)


    def fillMass(self, jet1, jet2):
        mj1j2 = ROOT.TLorentzVector()
        j1 = ROOT.TLorentzVector(); j2 = ROOT.TLorentzVector()
        j1.SetPtEtaPhiE(jet1.pt(), jet1.eta(), jet1.phi(), jet1.e())
        j2.SetPtEtaPhiE(jet2.pt(), jet2.eta(), jet2.phi(), jet2.e())
        mj1j2 = j1+j2
        return mj1j2.M()


    def process(self, event):
        self.tree.reset()
        jets_pf04   = getattr(event, self.cfg_ana.jets_pf04_2000)
        jets_calo04 = getattr(event, self.cfg_ana.jets_calo04_2000)

        
        if ( len(jets_pf04)>=2 and  len(jets_calo04)>=2):

            self.tree.fill('weight' , event.weight )
            self.tree.fill('missingET', event.met.pt())
    
            j1 = ROOT.TLorentzVector(); j2 = ROOT.TLorentzVector()
            j1.SetPtEtaPhiE(jets_calo04[0].pt(), jets_calo04[0].eta(), jets_calo04[0].phi(), jets_calo04[0].e())
            j2.SetPtEtaPhiE(jets_calo04[1].pt(), jets_calo04[1].eta(), jets_calo04[1].phi(), jets_calo04[1].e())

            self.tree.fill('rapiditySeparation_calo04', abs(j1.Rapidity()-j2.Rapidity())/2.)
            self.tree.fill('pseudorapiditySeparation_calo04', abs(jets_calo04[0].eta() - jets_calo04[1].eta()))
            self.tree.fill('transverseMomentumAsymmetry_calo04', (jets_calo04[0].pt() - jets_calo04[1].pt())/(jets_calo04[0].pt() + jets_calo04[1].pt()))
 
            j1.SetPtEtaPhiE(jets_pf04[0].pt(), jets_pf04[0].eta(), jets_pf04[0].phi(), jets_pf04[0].e())
            j2.SetPtEtaPhiE(jets_pf04[1].pt(), jets_pf04[1].eta(), jets_pf04[1].phi(), jets_pf04[1].e())
            self.tree.fill('rapiditySeparation_pf04', abs(j1.Rapidity()-j2.Rapidity())/2.)
            self.tree.fill('pseudorapiditySeparation_pf04', abs(jets_pf04[0].eta() - jets_pf04[1].eta()))
            self.tree.fill('transverseMomentumAsymmetry_pf04', (jets_pf04[0].pt() - jets_pf04[1].pt())/(jets_pf04[0].pt() + jets_pf04[1].pt()))

            fillParticle(self.tree, 'Jet1_pf04', jets_pf04[0])
            fillParticle(self.tree, 'Jet2_pf04', jets_pf04[1])

            fillParticle(self.tree, 'Jet1_calo04', jets_calo04[0])
            fillParticle(self.tree, 'Jet2_calo04', jets_calo04[1])

            self.tree.fill( 'Mj1j2_pf04', self.fillMass(jets_pf04[0],jets_pf04[1]))
            self.tree.fill( 'Mj1j2_calo04', self.fillMass(jets_calo04[0],jets_calo04[1]))

            self.tree.tree.Fill()

    def write(self, setup):
        self.rootfile.Write()
        self.rootfile.Close()
