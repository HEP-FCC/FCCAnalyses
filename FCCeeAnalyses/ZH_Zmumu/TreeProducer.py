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
        self.tree.var('ncjets', float)
        self.tree.var('ntaujets', float)
        self.tree.var('njets', float)

        self.tree.var('nmu_recoil', float)
        self.tree.var('nele', float)
        self.tree.var('nph', float)

        bookParticle(self.tree, 'recoil')
        bookParticle(self.tree, 'zed')
        bookParticle(self.tree, 'mu1')
        bookParticle(self.tree, 'mu2')
        bookMet(self.tree, 'met')

    def process(self, event):
        self.tree.reset()
        zeds = getattr(event, self.cfg_ana.zeds)

        if len(zeds) == 1:  
            self.tree.fill('weight' , event.weight )
            
            # Reco Higgs
            zed = zeds[0]
            fillParticle(self.tree, 'zed', zed)
            fillMet(self.tree, 'met', event.met)

            fillLepton(self.tree, 'mu1', zeds[0].legs[0])
            fillLepton(self.tree, 'mu2', zeds[0].legs[1])

            self.tree.fill('nbjets' , len(event.selected_bs) )
            self.tree.fill('ncjets' , len(event.selected_cs) )
            self.tree.fill('ntaujets' , len(event.selected_taus) )
            self.tree.fill('nljets' , len(event.selected_lights) )
            self.tree.fill('njets' , len(event.selected_lights) + len(event.selected_bs)+ len(event.selected_cs))

            self.tree.fill('nmu_recoil' , len(event.dressed_muons)-2)
            self.tree.fill('nele' , len(event.dressed_electrons))
            self.tree.fill('nph' , len(event.dressed_photons))

            recoil = getattr(event, self.cfg_ana.recoil)
            fillParticle(self.tree, 'recoil', recoil)


            self.tree.tree.Fill()
        
    def write(self, setup):
        self.rootfile.Write()
        self.rootfile.Close()

