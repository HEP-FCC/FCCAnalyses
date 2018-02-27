from heppy.framework.analyzer import Analyzer
from heppy.statistics.tree import Tree
from heppy.analyzers.ntuple import *
from heppy.particles.tlv.resonance import Resonance2 as Resonance
from heppy.utils.deltar import matchObjectCollection, deltaR

from ROOT import TFile, TLorentzVector
import itertools

class TreeProducer(Analyzer):

    def beginLoop(self, setup):
        super(TreeProducer, self).beginLoop(setup)
        self.rootfile = TFile('/'.join([self.dirName,
                                        'tree.root']),
                              'recreate')
        self.tree = Tree( 'events', '')
        self.tree.var('weight', float)
        
        bookParticle(self.tree, 'higgsjet')
        bookParticle(self.tree, 'softDropped_higgsjet')
        
        self.tree.var('higgsjet_tau1', float)       
        self.tree.var('higgsjet_tau2', float)
        self.tree.var('higgsjet_tau3', float)
        self.tree.var('higgsjet_tau32', float)
        self.tree.var('higgsjet_tau31', float)
        self.tree.var('higgsjet_tau21', float)

        self.tree.var('higgsjet_flow15', float)
        self.tree.var('higgsjet_flow25', float)
        self.tree.var('higgsjet_flow35', float)
        self.tree.var('higgsjet_flow45', float)
        self.tree.var('higgsjet_flow55', float)

        self.tree.var('higgsjet_nbs', float)

        bookParticle(self.tree, 'topjet')
        bookParticle(self.tree, 'softDropped_topjet')

        self.tree.var('topjet_tau1', float)       
        self.tree.var('topjet_tau2', float)
        self.tree.var('topjet_tau3', float)
        self.tree.var('topjet_tau32', float)
        self.tree.var('topjet_tau31', float)
        self.tree.var('topjet_tau21', float)

        self.tree.var('topjet_flow15', float)
        self.tree.var('topjet_flow25', float)
        self.tree.var('topjet_flow35', float)
        self.tree.var('topjet_flow45', float)
        self.tree.var('topjet_flow55', float)

        self.tree.var('topjet_nbs', float)

    def process(self, event):
        self.tree.reset()
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

        #bjets = []
        ljets = []
        # do b-tagging on the fly ...
        
        #print '---------------------------------------------------'
        #print len(bjets)
        
        
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
        
            #print jet.flow
        
        
        
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

                higgsjet =  selected_higgs_jets[0]
                topjet   =  selected_top_jets[0]
                
                fillParticle(self.tree, 'higgsjet', higgsjet)
                fillParticle(self.tree, 'softDropped_higgsjet', higgsjet.subjetsSoftDrop[0])
                
                self.tree.fill('higgsjet_tau1' , higgsjet.tau1 )
                self.tree.fill('higgsjet_tau2' , higgsjet.tau2 )
                self.tree.fill('higgsjet_tau3' , higgsjet.tau3 )
                
                higgsjet_tau31 = -9.0
                higgsjet_tau21 = -9.0
                higgsjet_tau32 = -9.0
     
                if (higgsjet.tau1 != 0.0):
                    higgsjet_tau31 = higgsjet.tau3/higgsjet.tau1
                    higgsjet_tau21 = higgsjet.tau2/higgsjet.tau1 
                if (higgsjet.tau2 != 0.0):
                    higgsjet_tau32 = higgsjet.tau3/higgsjet.tau2

                self.tree.fill('higgsjet_tau31' , higgsjet_tau31 )
                self.tree.fill('higgsjet_tau32' , higgsjet_tau32 )
                self.tree.fill('higgsjet_tau21' , higgsjet_tau21 )

                #print 'filling: ',higgsjet.flow[0], higgsjet.flow[1], higgsjet.flow[2], higgsjet.flow[3], higgsjet.flow[4]

                self.tree.fill('higgsjet_flow15', higgsjet.flow[0])
                self.tree.fill('higgsjet_flow25', higgsjet.flow[1])
                self.tree.fill('higgsjet_flow35', higgsjet.flow[2])
                self.tree.fill('higgsjet_flow45', higgsjet.flow[3])
                self.tree.fill('higgsjet_flow55', higgsjet.flow[4])

                self.tree.fill('higgsjet_nbs', higgsjet.nbs)

                fillParticle(self.tree, 'topjet', topjet)
                fillParticle(self.tree, 'softDropped_topjet', topjet.subjetsSoftDrop[0])

                self.tree.fill('topjet_tau1' , topjet.tau1 )
                self.tree.fill('topjet_tau2' , topjet.tau2 )
                self.tree.fill('topjet_tau3' , topjet.tau3 )

                topjet_tau31 = -9.0
                topjet_tau21 = -9.0
                topjet_tau32 = -9.0
     
                if (topjet.tau1 != 0.0):
                    topjet_tau31 = topjet.tau3/topjet.tau1
                    topjet_tau21 = topjet.tau2/topjet.tau1 
                if (topjet.tau2 != 0.0):
                    topjet_tau32 = topjet.tau3/topjet.tau2

                self.tree.fill('topjet_tau31' , topjet_tau31 )
                self.tree.fill('topjet_tau32' , topjet_tau32 )
                self.tree.fill('topjet_tau21' , topjet_tau21 )

                self.tree.fill('topjet_flow15', topjet.flow[0])
                self.tree.fill('topjet_flow25', topjet.flow[1])
                self.tree.fill('topjet_flow35', topjet.flow[2])
                self.tree.fill('topjet_flow45', topjet.flow[3])
                self.tree.fill('topjet_flow55', topjet.flow[4])

                self.tree.fill('topjet_nbs', topjet.nbs)

                self.tree.tree.Fill()
        

        
    def write(self, setup):
        self.rootfile.Write()
        self.rootfile.Close()

