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
        self.tree.var('ntaujets', float)
        self.tree.var('njets', float)
        self.tree.var('nele', float)
        self.tree.var('nmu', float)
        self.tree.var('mtw', float)

        bookParticle(self.tree, 'm3')
        bookParticle(self.tree, 'jet1')
        bookParticle(self.tree, 'jet2')
        bookParticle(self.tree, 'jet3')
        bookParticle(self.tree, 'jet4')
        
        bookMet(self.tree, 'met')

        bookLepton(self.tree, 'muon', pflow=False)
        bookLepton(self.tree, 'electron', pflow=False)

    def process(self, event):
        self.tree.reset()
    


        muons     = event.dressed_muons  
        electrons = event.dressed_electrons

        if len(muons)==0 and len(electrons)==0:
            return # NOT FILLING THE TREE IF NO

        if len(muons)==1 and len(electrons)==0:
            fillLepton(self.tree, 'muon', muons[0])
            fillIso(self.tree, 'muon_iso', muons[0].iso)

        elif len(electrons)==1 and len(muons)==0:
            fillLepton(self.tree, 'electron', electrons[0])
            fillIso(self.tree, 'electron_iso', electrons[0].iso)
                        
        else:
            return # NOT FILLING THE TREE IF MORE THAN 1 LEPTON


        jets = event.jets_nomuonnoelectron
        if len(jets)<3:
            return # NOT FILLING THE TREE IF LESS THAN 4 JETS
        for ijet, jet in enumerate(jets):
            if ijet==4:
                break
            fillParticle(self.tree, 'jet{ijet}'.format(ijet=ijet+1), jet)


        self.tree.fill('weight' , event.weight )
        fillMet(self.tree, 'met', event.met)

        #fillLepton(self.tree, 'mu1', zeds[0].legs[0])
        #fillLepton(self.tree, 'mu2', zeds[0].legs[1])

        self.tree.fill('nbjets' , len(event.selected_bs) )
        self.tree.fill('ntaujets' , len(event.selected_taus) )
        self.tree.fill('nljets' , len(event.selected_lights) )
        self.tree.fill('njets' , len(event.selected_lights) + len(event.selected_bs))
        self.tree.fill('nele' , len(event.dressed_electrons))
        self.tree.fill('nmu' , len(event.dressed_muons))

        m3 = getattr(event, self.cfg_ana.m3)
        if m3: fillParticle(self.tree, 'm3', m3)
        mtw = getattr(event, self.cfg_ana.mtw)
        if mtw: self.tree.fill( 'mtw', mtw)







        self.tree.tree.Fill()
        
    def write(self, setup):
        self.rootfile.Write()
        self.rootfile.Close()

