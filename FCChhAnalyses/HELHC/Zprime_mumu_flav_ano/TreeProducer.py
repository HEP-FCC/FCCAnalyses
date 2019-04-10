from heppy.framework.analyzer import Analyzer
from heppy.statistics.tree import Tree
from heppy.analyzers.ntuple import *
from numpy import sign
from ROOT import TFile

class TreeProducer(Analyzer):

    def beginLoop(self, setup):
        super(TreeProducer, self).beginLoop(setup)
        self.rootfile = TFile('/'.join([self.dirName,
                                        'tree.root']),
                              'recreate')
        self.tree = Tree( 'events', '')
        self.tree.var('weight', float)

        bookParticle(self.tree, 'zprime_ele')
        bookParticle(self.tree, 'zprime_muon')

        bookParticle(self.tree, 'jet1')
        bookParticle(self.tree, 'jet2')
        bookParticle(self.tree, 'jet3')
        bookLepton(self.tree, 'lep1', pflow=False)
        bookLepton(self.tree, 'lep2', pflow=False)
        bookLepton(self.tree, 'lep3', pflow=False)

        bookMet(self.tree, 'met')


    def process(self, event):
        self.tree.reset()
        zprimes_ele = getattr(event, self.cfg_ana.zprime_ele)
        zprimes_muon = getattr(event, self.cfg_ana.zprime_muon)
        if len(zprimes_ele)+len(zprimes_muon)==0: return

        jets = getattr(event, self.cfg_ana.jets)
        for ijet, jet in enumerate(jets):
            if ijet==3:
                break
            fillParticle(self.tree, 'jet{ijet}'.format(ijet=ijet+1), jet)

        self.tree.fill('weight' , sign(event.weight) )

        met = getattr(event, self.cfg_ana.met)
        fillMet(self.tree, 'met', met)


        zprimes_ele.sort(key=lambda x: x.m(), reverse=True)
        zprimes_muon.sort(key=lambda x: x.m(), reverse=True)


        if len(zprimes_ele)>0 and len(zprimes_muon)==0:
            fillParticle(self.tree, 'zprime_ele', zprimes_ele[0])
            fillLepton(self.tree, 'lep1', zprimes_ele[0].legs[0])
            fillLepton(self.tree, 'lep2', zprimes_ele[0].legs[1])
        elif len(zprimes_muon)>0 and len(zprimes_ele)==0 :
            fillParticle(self.tree, 'zprime_muon', zprimes_muon[0])
            fillLepton(self.tree, 'lep1', zprimes_muon[0].legs[0])
            fillLepton(self.tree, 'lep2', zprimes_muon[0].legs[1])
        else:
            if zprimes_ele[0].m()>zprimes_muon[0].m():
                fillParticle(self.tree, 'zprime_ele', zprimes_ele[0])
                fillLepton(self.tree, 'lep1', zprimes_ele[0].legs[0])
                fillLepton(self.tree, 'lep2', zprimes_ele[0].legs[1])
            else:
                fillParticle(self.tree, 'zprime_muon', zprimes_muon[0])
                fillLepton(self.tree, 'lep1', zprimes_muon[0].legs[0])
                fillLepton(self.tree, 'lep2', zprimes_muon[0].legs[1])

        self.tree.tree.Fill()

    def write(self, setup):
        self.rootfile.Write()
        self.rootfile.Close()
        
