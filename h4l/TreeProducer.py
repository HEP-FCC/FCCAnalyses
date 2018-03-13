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

        bookParticle(self.tree, 'higgs')
        bookParticle(self.tree, 'zed1')
        bookParticle(self.tree, 'zed2')
        bookParticle(self.tree, 'l1')
        bookParticle(self.tree, 'l2')
        bookParticle(self.tree, 'l3')
        bookParticle(self.tree, 'l4')
        bookParticle(self.tree, 'e1')
        bookParticle(self.tree, 'e2')
        bookParticle(self.tree, 'mu1')
        bookParticle(self.tree, 'mu2')
        bookMet(self.tree, 'met')

        self.tree.var('nljets', float)
        self.tree.var('nbjets', float)
        self.tree.var('njets', float)



    def process(self, event):
        self.tree.reset()
        zeds = getattr(event, self.cfg_ana.zeds)
        zeds.sort(key=lambda x: abs(x.m()-91.))
        higgses = getattr(event, self.cfg_ana.higgses)
        leptons = []


        if len(higgses) > 0:  
            self.tree.fill('weight' , event.weight )

            # Reco Higgs
            higgs = higgses[0]
            fillParticle(self.tree, 'higgs', higgs)
            fillParticle(self.tree, 'zed1', zeds[0])
            fillParticle(self.tree, 'zed2', zeds[1])
            fillMet(self.tree, 'met', event.met)

            leptons.append(zeds[0].legs[0])
            leptons.append(zeds[0].legs[1])
            leptons.append(zeds[1].legs[0])
            leptons.append(zeds[1].legs[1])

            leptons.sort(key=lambda x: x.pt(), reverse=True)

            fillLepton(self.tree, 'l1', leptons[0])
            fillLepton(self.tree, 'l2', leptons[1])
            fillLepton(self.tree, 'l3', leptons[2])
            fillLepton(self.tree, 'l4', leptons[3])

            electrons = []
            muons = []
            
            for l in leptons:
                if abs(l.pdgid()) == 11:
                    electrons.append(l)
                if abs(l.pdgid()) == 13:
                    muons.append(l)

            if len(electrons) > 1:
                fillLepton(self.tree, 'e1', electrons[0])
                fillLepton(self.tree, 'e2', electrons[1])
            if len(muons) > 1:
                fillLepton(self.tree, 'mu1', muons[0])
                fillLepton(self.tree, 'mu2', muons[1])

            self.tree.fill('nbjets' , len(event.selected_bs) )
            self.tree.fill('nljets' , len(event.selected_lights) )
            self.tree.fill('njets' , len(event.selected_lights) + len(event.selected_bs))

            self.tree.tree.Fill()
        
    def write(self, setup):
        self.rootfile.Write()
        self.rootfile.Close()

