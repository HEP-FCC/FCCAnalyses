from heppy.framework.analyzer import Analyzer
from heppy.statistics.tree import Tree
from heppy.analyzers.ntuple import *
from numpy import sign
from ROOT import TFile, TLorentzVector
class TreeProducer(Analyzer):

    def beginLoop(self, setup):
        super(TreeProducer, self).beginLoop(setup)
        self.rootfile = TFile('/'.join([self.dirName,
                                        'tree.root']),
                              'recreate')
        self.tree = Tree( 'events', '')
        self.tree.var('weight', float)
        self.tree.var('zprime_y', float)

        bookParticle(self.tree, 'zprime_ele')
        bookParticle(self.tree, 'zprime_muon')

        bookParticle(self.tree, 'jet1')
        bookParticle(self.tree, 'jet2')
        bookParticle(self.tree, 'jet3')
        bookLepton(self.tree, 'lep1', pflow=False)
        bookLepton(self.tree, 'lep2', pflow=False)
        bookLepton(self.tree, 'lep3', pflow=False)

        bookLepton(self.tree, 'lep1_gen_1', pflow=False)
        bookLepton(self.tree, 'lep2_gen_1', pflow=False)

        bookLepton(self.tree, 'lep1_gen_23', pflow=False)
        bookLepton(self.tree, 'lep2_gen_23', pflow=False)

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

        Zp = TLorentzVector()

        if len(zprimes_ele)>0 and len(zprimes_muon)==0:
            fillParticle(self.tree, 'zprime_ele', zprimes_ele[0])
            fillLepton(self.tree, 'lep1', zprimes_ele[0].legs[0])
            fillLepton(self.tree, 'lep2', zprimes_ele[0].legs[1])
            Zp.SetPtEtaPhiM(zprimes_ele[0].pt(),zprimes_ele[0].eta(),zprimes_ele[0].phi(),zprimes_ele[0].m())
            self.tree.fill('zprime_y' ,  Zp.Rapidity())

        elif len(zprimes_muon)>0 and len(zprimes_ele)==0 :
            fillParticle(self.tree, 'zprime_muon', zprimes_muon[0])
            fillLepton(self.tree, 'lep1', zprimes_muon[0].legs[0])
            fillLepton(self.tree, 'lep2', zprimes_muon[0].legs[1])
            Zp.SetPtEtaPhiM(zprimes_muon[0].pt(),zprimes_muon[0].eta(),zprimes_muon[0].phi(),zprimes_muon[0].m())
            self.tree.fill('zprime_y' ,  Zp.Rapidity())

        else:
            if zprimes_ele[0].m()>zprimes_muon[0].m():
                fillParticle(self.tree, 'zprime_ele', zprimes_ele[0])
                fillLepton(self.tree, 'lep1', zprimes_ele[0].legs[0])
                fillLepton(self.tree, 'lep2', zprimes_ele[0].legs[1])
                Zp.SetPtEtaPhiM(zprimes_ele[0].pt(),zprimes_ele[0].eta(),zprimes_ele[0].phi(),zprimes_ele[0].m())
                self.tree.fill('zprime_y' ,  Zp.Rapidity())

            else:
                fillParticle(self.tree, 'zprime_muon', zprimes_muon[0])
                fillLepton(self.tree, 'lep1', zprimes_muon[0].legs[0])
                fillLepton(self.tree, 'lep2', zprimes_muon[0].legs[1])
                Zp.SetPtEtaPhiM(zprimes_muon[0].pt(),zprimes_muon[0].eta(),zprimes_muon[0].phi(),zprimes_muon[0].m())
                self.tree.fill('zprime_y' ,  Zp.Rapidity())

        for g in event.gen_particles:
            if g.pt()<50.:continue
            if g.pdgid()==11 or g.pdgid()==13 and g.status()==1:
                fillLepton(self.tree, 'lep1_gen_1', g)
            if g.pdgid()==-11 or g.pdgid()==-13 and g.status()==1:
                fillLepton(self.tree, 'lep2_gen_1', g)
            if g.pdgid()==11 or g.pdgid()==13 and g.status()==23:
                fillLepton(self.tree, 'lep1_gen_23', g)
            if g.pdgid()==-11 or g.pdgid()==-13 and g.status()==23:
                fillLepton(self.tree, 'lep2_gen_23', g)



        self.tree.tree.Fill()

    def write(self, setup):
        self.rootfile.Write()
        self.rootfile.Close()
        
