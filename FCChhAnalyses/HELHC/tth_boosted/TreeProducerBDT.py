from heppy.framework.analyzer import Analyzer
from heppy.statistics.tree import Tree
from heppy.analyzers.ntuple import *
from heppy.particles.tlv.resonance import Resonance2 as Resonance
from heppy.utils.deltar import matchObjectCollection, deltaR

from ROOT import TFile, TLorentzVector
import itertools

class TreeProducerBDT(Analyzer):

    def beginLoop(self, setup):
        super(TreeProducerBDT, self).beginLoop(setup)
        
        self.rootfileS = TFile('/'.join([self.dirName,
                                        'treeS.root']),
                              'recreate')
        self.treeS = Tree( 'events', '')
	self.treeS.var('weight', float)
        
        bookParticle(self.treeS, 'jet')
        bookParticle(self.treeS, 'softDropped_jet')
        
        self.treeS.var('jet_tau1', float)       
        self.treeS.var('jet_tau2', float)
        self.treeS.var('jet_tau3', float)
        self.treeS.var('jet_tau32', float)
        self.treeS.var('jet_tau31', float)
        self.treeS.var('jet_tau21', float)

        self.treeS.var('jet_flow15', float)
        self.treeS.var('jet_flow25', float)
        self.treeS.var('jet_flow35', float)
        self.treeS.var('jet_flow45', float)
        self.treeS.var('jet_flow55', float)

        self.treeS.var('jet_nbs', float)

        self.rootfileB = TFile('/'.join([self.dirName,
                                        'treeB.root']),
                              'recreate')
        self.treeB = Tree( 'events', '')

        bookParticle(self.treeB, 'jet')
        bookParticle(self.treeB, 'softDropped_jet')
        
        self.treeB.var('jet_tau1', float)       
        self.treeB.var('jet_tau2', float)
        self.treeB.var('jet_tau3', float)
        self.treeB.var('jet_tau32', float)
        self.treeB.var('jet_tau31', float)
        self.treeB.var('jet_tau21', float)

        self.treeB.var('jet_flow15', float)
        self.treeB.var('jet_flow25', float)
        self.treeB.var('jet_flow35', float)
        self.treeB.var('jet_flow45', float)
        self.treeB.var('jet_flow55', float)

        self.treeB.var('jet_nbs', float)

    def process(self, event):
        self.treeS.reset()
        self.treeB.reset()
        gen_bs = getattr(event, self.cfg_ana.gen_bs)
        gen_higgses = getattr(event, self.cfg_ana.gen_higgses)
        gen_higgses.sort(key=lambda x: x.pt(), reverse = True)
        gen_tops = getattr(event, self.cfg_ana.gen_tops)
        gen_tops.sort(key=lambda x: x.pt(), reverse = True)
        jets = getattr(event, self.cfg_ana.fatjets)
        leptons = getattr(event, self.cfg_ana.selected_leptons)
        bjets = event.selected_bs

        if len(gen_higgses) > 1:
            hh_gen = Resonance(gen_higgses[0], gen_higgses[1], 25)

        ljets = []

        #_________________________________________________________________
        # count number of bjets inside jet
        for jet in jets:
            is_light = True
            setattr(jet, 'nbs', 0)
            for b in bjets:
                drjb = deltaR(b, jet)
                if drjb < 1.5: 
                    jet.nbs += 1
        
        #_________________________________________________________________
        # compute eflow variables
        
        R = 1.5
        
        for jet in jets:
            
            setattr(jet, 'flow', [0]*5)
            constituent_vector = TLorentzVector()
            #print jet.pt, jet.flow
            for n in range(1,5+1):
                 #print n 
                 for constituent in jet.jetConstituents[1:]:
                     #print constituent.pt()
                     dR = jet.p4().DeltaR(constituent.p4())
                     if ((dR >= (n-1)/5.*R) and (dR < n/5.*R)):
                         #print 'in ring', dR
                         jet.flow[n-1] += abs(constituent.pt())/abs(jet.pt())
        
        #print '--------------- new event --------------------------------'
        
        if len(leptons) > 0 and len(jets) > 1:

            #print len(jets), len(leptons)
            
            #print deltaR(jets[0], leptons[0]), deltaR(jets[1], leptons[0])
            
            selected_higgs_jets = []
            selected_top_jets = []

            # to decide wheather top or higgs jet will be done with MVA
            # for now just cheat by checking MC truth
            
            for jet in jets:
                drmin_h = 999.
                drmin_t = 999.

                for higgs in gen_higgses:
                    drjh = deltaR(higgs, jet)
                    if drjh < drmin_h: 
                        drmin_h = drjh

                for top in gen_tops:
                    drjt = deltaR(top, jet)
                    if drjt < drmin_t: 
                        drmin_t = drjt

                if  drmin_h < drmin_t and drmin_h < 1.0:   
                    selected_higgs_jets.append(jet)

                elif  drmin_t < drmin_h and drmin_t < 1.0:   
                    selected_top_jets.append(jet)


            if len(selected_higgs_jets) > 0 and len(selected_top_jets) > 0 :
                for tree in [self.treeS, self.treeB]:

                    if tree == self.treeS:
		        jet =  selected_higgs_jets[0]
		    else:
                        jet   =  selected_top_jets[0]

                    fillParticle(tree, 'jet', jet)
                    fillParticle(tree, 'softDropped_jet', jet.subjetsSoftDrop[0])

                    tree.fill('jet_tau1' , jet.tau1 )
                    tree.fill('jet_tau2' , jet.tau2 )
                    tree.fill('jet_tau3' , jet.tau3 )

                    jet_tau31 = -9.0
                    jet_tau21 = -9.0
                    jet_tau32 = -9.0

                    if (jet.tau1 != 0.0):
                	jet_tau31 = jet.tau3/jet.tau1
                	jet_tau21 = jet.tau2/jet.tau1 
                    if (jet.tau2 != 0.0):
                	jet_tau32 = jet.tau3/jet.tau2

                    tree.fill('jet_tau31' , jet_tau31 )
                    tree.fill('jet_tau32' , jet_tau32 )
                    tree.fill('jet_tau21' , jet_tau21 )

                    #print 'filling: ',jet.flow[0], jet.flow[1], jet.flow[2], jet.flow[3], jet.flow[4]

                    tree.fill('jet_flow15', jet.flow[0])
                    tree.fill('jet_flow25', jet.flow[1])
                    tree.fill('jet_flow35', jet.flow[2])
                    tree.fill('jet_flow45', jet.flow[3])
                    tree.fill('jet_flow55', jet.flow[4])

                    tree.fill('jet_nbs', jet.nbs)

                    tree.tree.Fill()
        

        
    def write(self, setup):
        self.rootfileS.Write()
        self.rootfileS.Close()

        self.rootfileB.Write()
        self.rootfileB.Close()

