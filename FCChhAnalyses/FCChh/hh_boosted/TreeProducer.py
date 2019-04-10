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
        
        self.tree.var('nljets', float)
        self.tree.var('njets', float)
        self.tree.var('nbjets', float)

        #self.tree.var('hh_m', float)
        self.tree.var('drhh', float)
        self.tree.var('dPtRel', float)

        self.tree.var('bJet1_tau21', float)
        self.tree.var('bJet2_tau21', float)
        self.tree.var('bJet3_tau21', float)

        self.tree.var('lJet1_tau21', float)
        self.tree.var('lJet2_tau21', float)


        bookParticle(self.tree, 'bJet1')
        bookParticle(self.tree, 'bJet2')
        bookParticle(self.tree, 'bJet3')
        bookParticle(self.tree, 'softDropped_bJet1')
        bookParticle(self.tree, 'softDropped_bJet2')
        bookParticle(self.tree, 'softDropped_bJet3')
        
        bookParticle(self.tree, 'hh')
        bookParticle(self.tree, 'hh_gen')

        bookParticle(self.tree, 'lJet1')
        bookParticle(self.tree, 'lJet2')
        bookParticle(self.tree, 'softDropped_lJet1')
        bookParticle(self.tree, 'softDropped_lJet2')


    def process(self, event):
        self.tree.reset()
        gen_bs = getattr(event, self.cfg_ana.gen_bs)
        gen_higgses = getattr(event, self.cfg_ana.gen_higgses)
        gen_higgses.sort(key=lambda x: x.pt(), reverse = True)
        jets = getattr(event, self.cfg_ana.fatjets)

        if len(gen_higgses) > 1:
            hh_gen = Resonance(gen_higgses[0], gen_higgses[1], 25)

        bjets = []
        ljets = []
        # do b-tagging on the fly ...
        for jet in jets:
            is_light = True
            for b in gen_bs:
                drjb = deltaR(b, jet)
                if drjb < 0.8: 
                    is_light = False
            if is_light:
                ljets.append(jet)
            else:
                bjets.append(jet)

        bjets.sort(key=lambda x: x.pt(), reverse = True)
        ljets.sort(key=lambda x: x.pt(), reverse = True)

        #if (len(ljets)>0 and len(bjets)>1):
        if len(bjets)>1:
            
            hh = Resonance(bjets[0], bjets[1], 25)
            if hh.pt() > 250. :

                #self.tree.fill('weight' , event.weight  )
                weight = (0.70**4) * event.weight 
		self.tree.fill('weight' , weight )
                
		self.tree.fill('nljets' , len(ljets) )
                self.tree.fill('njets' , len(jets) )
                self.tree.fill('nbjets' , len(bjets) )

                fillParticle(self.tree, 'bJet1', bjets[0])
                fillParticle(self.tree, 'bJet2', bjets[1])

                fillParticle(self.tree, 'softDropped_bJet1', bjets[0].subjetsSoftDrop[0])
                fillParticle(self.tree, 'softDropped_bJet2', bjets[1].subjetsSoftDrop[0])

                fillParticle(self.tree, 'hh', hh)
                self.tree.fill('drhh', deltaR(bjets[0], bjets[1]))

                self.tree.fill('dPtRel', abs(bjets[0].pt() - bjets[1].pt())/hh.pt())

                if (bjets[0].tau1 != 0.0):
                    self.tree.fill('bJet1_tau21' , bjets[0].tau2/bjets[0].tau1 )
                else:
                    self.tree.fill('bJet1_tau21' , -99 )
                if (bjets[1].tau1 != 0.0):
                    self.tree.fill('bJet2_tau21' , bjets[1].tau2/bjets[1].tau1 )
                else:
                    self.tree.fill('bJet2_tau21' , -99 )


                if len(ljets) > 0:

                    fillParticle(self.tree, 'lJet1', ljets[0])
                    fillParticle(self.tree, 'softDropped_lJet1', ljets[0].subjetsSoftDrop[0])

                    if (ljets[0].tau1 != 0.0):
                        self.tree.fill('lJet1_tau21' , ljets[0].tau2/ljets[0].tau1 )
                    else:
                        self.tree.fill('lJet1_tau21' , -99 )

                if len(bjets) > 2:

                   fillParticle(self.tree, 'bJet3', bjets[2])
                   fillParticle(self.tree, 'softDropped_bJet3', bjets[2].subjetsSoftDrop[0])

                   if (bjets[2].tau1 != 0.0):
                       self.tree.fill('bJet3_tau21' , bjets[2].tau2/bjets[2].tau1 )
                   else:
                       self.tree.fill('bJet3_tau21' , -99 )

                if len(ljets) > 1:

                   fillParticle(self.tree, 'lJet2', ljets[1])
                   fillParticle(self.tree, 'softDropped_lJet1', ljets[1].subjetsSoftDrop[0])

                   if (ljets[1].tau1 != 0.0):
                       self.tree.fill('lJet2_tau21' , ljets[1].tau2/ljets[1].tau1 )
                   else:
                       self.tree.fill('lJet2_tau21' , -99 )


                if len(gen_higgses) > 1:
                    hh_gen = Resonance(gen_higgses[0], gen_higgses[1], 25)
                    fillParticle(self.tree, 'hh_gen', hh_gen)


                self.tree.tree.Fill()
        
    def write(self, setup):
        self.rootfile.Write()
        self.rootfile.Close()

