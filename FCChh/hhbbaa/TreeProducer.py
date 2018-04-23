from heppy.framework.analyzer import Analyzer
from heppy.statistics.tree import Tree
from heppy.analyzers.ntuple import *
from heppy.particles.tlv.resonance import Resonance2 as Resonance
from heppy.utils.deltar import matchObjectCollection, deltaR

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
        self.tree.var('nlep', float)
        self.tree.var('drbb', float)
        self.tree.var('draa', float)

        bookParticle(self.tree, 'haa')
        bookParticle(self.tree, 'hbb')
        bookLepton(self.tree, 'a1')
        bookLepton(self.tree, 'a2')
        bookLepton(self.tree, 'b1')
        bookLepton(self.tree, 'b2')        
        bookParticle(self.tree, 'hh')

        bookMet(self.tree, 'met')

    def process(self, event):
        self.tree.reset()
        haas = getattr(event, self.cfg_ana.haas)
        hbbs  = getattr(event, self.cfg_ana.hbbs)

        haas.sort(key=lambda x: abs(x.m()-125.))
        hbbs.sort(key=lambda x: abs(x.m()-125.))
              
	      
        if len(haas) > 0 and len(hbbs) > 0:
            
	    self.tree.fill('weight' , event.weight )
            # jet multiplicities
            self.tree.fill('nbjets' , len(event.selected_bs) )
            self.tree.fill('nljets' , len(event.selected_lights) )
            self.tree.fill('njets' , len(event.selected_lights) + len(event.selected_bs))
            self.tree.fill('nlep' , len(event.selected_leptons))
            
            # missing Et
            fillMet(self.tree, 'met', event.met)
            
            # Reco higgses
            photons = []
            photons.append(haas[0].leg1())
            photons.append(haas[0].leg2())
            photons.sort(key=lambda x: x.pt(), reverse=True)
            
            bs = []
            bs.append(hbbs[0].leg1())
            bs.append(hbbs[0].leg2())
            bs.sort(key=lambda x: x.pt(), reverse=True)
            
            hh = Resonance( haas[0], hbbs[0], 25)

            fillParticle(self.tree, 'hh', hh)
            fillParticle(self.tree, 'haa', haas[0])
            fillParticle(self.tree, 'hbb', hbbs[0])
            fillParticle(self.tree, 'a1', photons[0])
            fillParticle(self.tree, 'a2', photons[1])
            fillParticle(self.tree, 'b1', bs[0])
            fillParticle(self.tree, 'b2', bs[1])

            self.tree.tree.Fill()
        
	'''phos = getattr(event, self.cfg_ana.photons)
        bs   = getattr(event, self.cfg_ana.bs)
	
        phos.sort(key=lambda x: x.pt(), reverse=True)
        bs.sort(key=lambda x: x.pt(), reverse=True)'''


        #print len(phos), len(bs)	
	'''if len(phos) > 1 and len(bs) > 1 :

            drbb = deltaR(bs[0], bs[1])
            draa = deltaR(phos[0], phos[1])
	    haa = Resonance( phos[0], phos[1], 25)
	    hbb = Resonance( bs[0], bs[1], 25)
            hh = Resonance( haa, hbb, 25)

            if haa.m() > 100 and haa.m() < 150 and hbb.m() > 60 and hbb.m() < 200: 


		self.tree.fill('weight' , event.weight )
        	# jet multiplicities
        	self.tree.fill('nbjets' , len(event.selected_bs) )
        	self.tree.fill('nljets' , len(event.selected_lights) )
        	self.tree.fill('njets' , len(event.selected_lights) + len(event.selected_bs))
        	self.tree.fill('nlep' , len(event.selected_leptons))


        	self.tree.fill('draa' , draa)
        	self.tree.fill('drbb' , drbb)


        	# missing Et
        	fillMet(self.tree, 'met', event.met)


        	fillParticle(self.tree, 'hh', hh)
        	fillParticle(self.tree, 'haa', haa)
        	fillParticle(self.tree, 'hbb', hbb)
        	fillParticle(self.tree, 'a1', phos[0])
        	fillParticle(self.tree, 'a2', phos[1])
        	fillParticle(self.tree, 'b1', bs[0])
        	fillParticle(self.tree, 'b2', bs[1])

        	self.tree.tree.Fill()'''
	
    def write(self, setup):
        self.rootfile.Write()
        self.rootfile.Close()

