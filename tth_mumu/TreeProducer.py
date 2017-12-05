from heppy.framework.analyzer import Analyzer
from heppy.statistics.tree import Tree
from heppy.analyzers.ntuple import *
from heppy.particles.tlv.resonance import Resonance2 as Resonance

from ROOT import TFile

class TreeProducer(Analyzer):

    def beginLoop(self, setup):
        super(TreeProducer, self).beginLoop(setup)
        self.rootfile = TFile('/'.join([self.dirName,
                                        'tree.root']),
                              'recreate')
        self.tree = Tree( 'events', '')
        self.tree.var('weight', float)
        self.tree.var('nljets', float)
        self.tree.var('nbjets', float)
        self.tree.var('njets', float)
        self.tree.var('DiMuonInvMass', float)

        bookParticle(self.tree, 'higgs')
        bookParticle(self.tree, 'mu1')
        bookParticle(self.tree, 'mu2')
        bookMet(self.tree, 'met')

    def process(self, event):
        self.tree.reset()
        higgses = getattr(event, self.cfg_ana.higgses)

        if len(higgses) == 1:  
            self.tree.fill('weight' , event.weight )
            
            # Reco Higgs
            higgs = higgses[0]
            fillParticle(self.tree, 'higgs', higgs)
            fillMet(self.tree, 'met', event.met)

            fillLepton(self.tree, 'mu1', higgses[0].legs[0])
            fillLepton(self.tree, 'mu2', higgses[0].legs[1])

            self.tree.fill("DiMuonInvMass", higgses[0]._tlv.M())
            self.tree.fill('nbjets' , len(event.selected_bs) )
            self.tree.fill('nljets' , len(event.selected_lights) )
            self.tree.fill('njets' , len(event.selected_lights) + len(event.selected_bs))


            self.tree.tree.Fill()
        
    def write(self, setup):
        self.rootfile.Write()
        self.rootfile.Close()

