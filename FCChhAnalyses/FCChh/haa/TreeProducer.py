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
        #self.tree.var('met', float)
        self.tree.var('nljets', float)
        self.tree.var('nbjets', float)
        self.tree.var('njets', float)

        bookParticle(self.tree, 'higgs')
        bookParticle(self.tree, 'a1')
        bookParticle(self.tree, 'a2')
        bookMet(self.tree, 'met')

    def process(self, event):
        self.tree.reset()
        higgses = getattr(event, self.cfg_ana.higgses)
        higgses.sort(key=lambda x: x.legs[0].pt()+x.legs[1].pt(), reverse=True)
        leptons = []

        if len(higgses) > 0:  
            self.tree.fill('weight' , event.weight )
            
            # Reco Higgs
            higgs = higgses[0]
            fillParticle(self.tree, 'higgs', higgs)
            fillMet(self.tree, 'met', event.met)

            fillLepton(self.tree, 'a1', higgses[0].legs[0])
            fillLepton(self.tree, 'a2', higgses[0].legs[1])

            self.tree.fill('nbjets' , len(event.selected_bs) )
            self.tree.fill('nljets' , len(event.selected_lights) )
            self.tree.fill('njets' , len(event.selected_lights) + len(event.selected_bs))

            self.tree.tree.Fill()
        
    def write(self, setup):
        self.rootfile.Write()
        self.rootfile.Close()

