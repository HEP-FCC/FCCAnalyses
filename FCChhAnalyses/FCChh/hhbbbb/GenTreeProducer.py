from heppy.framework.analyzer import Analyzer
from heppy.statistics.tree import Tree
from heppy.analyzers.ntuple import *
from heppy.particles.tlv.resonance import Resonance2 as Resonance
from heppy.utils.deltar import matchObjectCollection, deltaR

from ROOT import TFile

class GenTreeProducer(Analyzer):

    def beginLoop(self, setup):
        super(GenTreeProducer, self).beginLoop(setup)
        self.rootfile = TFile('/'.join([self.dirName,
                                        'tree.root']),
                              'recreate')
        self.tree = Tree( 'events', '')
        self.tree.var('weight', float)
        self.tree.var('nh', float)
        self.tree.var('drhh', float)

        bookParticle(self.tree, 'h1')
        bookParticle(self.tree, 'h2')
        bookParticle(self.tree, 'hh')

    def process(self, event):
        self.tree.reset()
        gen_higgses = getattr(event, self.cfg_ana.gen_higgses)

        self.tree.fill('weight' , event.weight )
        self.tree.fill('nh' , len(gen_higgses) )
       
        gen_higgses.sort(key=lambda x: x.pt(), reverse = True)
 
        if len(gen_higgses) > 1:

            hh = Resonance(gen_higgses[0], gen_higgses[1], 25)
            if hh.pt() > 500. :

               fillParticle(self.tree, 'h1', gen_higgses[0])
               fillParticle(self.tree, 'h2', gen_higgses[1])
            
               fillParticle(self.tree, 'hh', hh)

               drhh = deltaR(gen_higgses[0], gen_higgses[1])
               self.tree.fill('drhh' , drhh)
            
               self.tree.tree.Fill()
        
    def write(self, setup):
        self.rootfile.Write()
        self.rootfile.Close()

