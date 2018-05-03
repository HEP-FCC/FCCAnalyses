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
        bookParticle(self.tree, 'zed')
        bookParticle(self.tree, 'l1')
        bookParticle(self.tree, 'l2')
        bookParticle(self.tree, 'a')
        bookMet(self.tree, 'met')


    def process(self, event):
        self.tree.reset()
        zeds = getattr(event, self.cfg_ana.zeds)
	zeds.sort(key=lambda x: abs(x.m()-91.))
        photons = getattr(event, self.cfg_ana.photons)
	photons.sort(key=lambda x: x.pt(), reverse = True)
        
	leptons = []
	if len(zeds) > 0 and len(photons) > 0:
	    higgs = Resonance(zeds[0], photons[0], 25)

            self.tree.fill('weight' , event.weight )
            #print event.weight
            # Reco Higgs
            fillParticle(self.tree, 'higgs', higgs)
            fillParticle(self.tree, 'zed', zeds[0])
            fillMet(self.tree, 'met', event.met)

            leptons.append(zeds[0].legs[0])
            leptons.append(zeds[0].legs[1])

            leptons.sort(key=lambda x: x.pt(), reverse=True)

            fillLepton(self.tree, 'l1', leptons[0])
            fillLepton(self.tree, 'l2', leptons[1])
            fillLepton(self.tree, 'a', photons[0])

            self.tree.tree.Fill()
        
    def write(self, setup):
        self.rootfile.Write()
        self.rootfile.Close()

