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
        
        self.tree.var('njets', float)
        self.tree.var('nleptons', float)

        bookParticle(self.tree, 'l1')
        bookParticle(self.tree, 'l2')
        bookParticle(self.tree, 'l3')
        bookParticle(self.tree, 'l4')
        
        bookParticle(self.tree, 'j1')
        bookParticle(self.tree, 'j2')
        bookParticle(self.tree, 'j3')
        bookParticle(self.tree, 'j4')

        bookParticle(self.tree, 'gj1')
        bookParticle(self.tree, 'gj2')
        bookParticle(self.tree, 'gl1')
        bookParticle(self.tree, 'gl2')
        bookParticle(self.tree, 'gv1')
        bookParticle(self.tree, 'gv2')
        
        bookMet(self.tree, 'met')

    '''
    def filterHard(self, event):
        
        genparts = event.gen_particles
        
        print '--------------------------------------'
        for gen in genparts:
            if gen.status > 20 and gen.status < 30:
                print gen'''

        



    def process(self, event):
        self.tree.reset()
        
        genparts = event.gen_particles
        
        #print '--------------------------------------'
        
        genjets = []
        genneus = []
        genleps = []
        genws   = []

        for gen in genparts:
            if gen.status() > 20 and gen.status() < 30:
                if abs(gen.pdgid())<5 and gen.pt() > 0.:
                    genjets.append(gen)
                if abs(gen.pdgid()) == 11 or abs(gen.pdgid()) == 13 or abs(gen.pdgid()) == 15:
                    genleps.append(gen)
                if abs(gen.pdgid()) == 12 or abs(gen.pdgid()) == 14 or abs(gen.pdgid()) == 16:
                    genneus.append(gen)
                if abs(gen.pdgid()) == 24:
                    genws.append(gen)
                    
        if len(genleps) < 2:
            
            genleps = []
	    for gen in genparts:
                if gen.status() == 1 and gen.pt() > 5.:
                    if abs(gen.pdgid()) == 11 or abs(gen.pdgid()) == 13 or abs(gen.pdgid()) == 15:
                        genleps.append(gen)

        if len(genneus) < 2:
            genneus = []
            for gen in genparts:
                if gen.status() == 1 and gen.pt() > 5:
                    if abs(gen.pdgid()) == 12 or abs(gen.pdgid()) == 14 or abs(gen.pdgid()) == 16:
                        genneus.append(gen)
	
	'''if len(genleps) < 2:
            for gen in genparts:
	        if gen.status() > 20 and gen.status() < 30 :
                   print gen'''
        
	

        genjets.sort(key=lambda x: x.pt(), reverse = True)
        genneus.sort(key=lambda x: x.pt(), reverse = True)
        genleps.sort(key=lambda x: x.pt(), reverse = True)
	
        if len(genjets) > 0:
            fillParticle(self.tree, 'gj1', genjets[0])
            if len(genjets) > 1:
                fillParticle(self.tree, 'gj2', genjets[1])

        if len(genneus) > 0:
            fillParticle(self.tree, 'gv1', genneus[0])
            if len(genneus) > 1:
                fillParticle(self.tree, 'gv2', genneus[1])
	
        if len(genleps) > 0:
            fillParticle(self.tree, 'gl1', genleps[0])
            if len(genleps) > 1:
                fillParticle(self.tree, 'gl2', genleps[1])
	
	
        '''for gen in genparts:
            if gen.status() == 1 and (abs(gen.pdgid()) == 11 or abs(gen.pdgid()) == 13 or abs(gen.pdgid()) == 15 or abs(gen.pdgid()) == 12 or abs(gen.pdgid()) == 14 or abs(gen.pdgid()) == 16):
               print gen
 	
        print len(genjets), len(genneus), len(genleps)'''

        '''print ''
	
        for gen in genparts:
            if gen.status() == 1 and (abs(gen.pdgid()) == 11 or abs(gen.pdgid()) == 13 or abs(gen.pdgid()) == 15 or abs(gen.pdgid()) == 12 or abs(gen.pdgid()) == 14 or abs(gen.pdgid()) == 16):
               print gen
        

        print len(genjets), len(genneus), len(genleps)
        print ''
	
        for gen in genparts:
            print gen
        '''
        
        leptons = event.selected_leptons
        leptons.sort(key=lambda x: x.pt(), reverse = True)

        jets = event.jets_nolepton
        jets.sort(key=lambda x: x.pt(), reverse = True)
        
        met = event.met
        
        self.tree.fill('weight' , event.weight )
        self.tree.fill('njets' , len(jets))
        self.tree.fill('nleptons' , len(leptons))
        fillMet(self.tree, 'met', met)

        if len(leptons) > 0:
            fillParticle(self.tree, 'l1', leptons[0])
            if len(leptons) > 1:
                fillParticle(self.tree, 'l2', leptons[1])
                if len(leptons) > 2:
                    fillParticle(self.tree, 'l3', leptons[2])
                    if len(leptons) > 3:
                        fillParticle(self.tree, 'l4', leptons[3])

        if len(jets) > 0:
            fillParticle(self.tree, 'j1', jets[0])
            if len(jets) > 1:
                fillParticle(self.tree, 'j2', jets[1])
                if len(jets) > 2:
                    fillParticle(self.tree, 'j3', jets[2])
                    if len(jets) > 3:
                        fillParticle(self.tree, 'j4', jets[3])


        self.tree.tree.Fill()
        
    def write(self, setup):
        self.rootfile.Write()
        self.rootfile.Close()

