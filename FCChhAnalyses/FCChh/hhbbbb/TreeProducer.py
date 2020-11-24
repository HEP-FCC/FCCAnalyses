from heppy.framework.analyzer import Analyzer
from heppy.statistics.tree import Tree
from heppy.analyzers.ntuple import *
from heppy.particles.tlv.resonance import Resonance2 as Resonance
from heppy.utils.deltar import matchObjectCollection, deltaR

from ROOT import TFile, TLorentzVector
import ROOT
import array

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

        bookParticle(self.tree, 'h1')
        bookParticle(self.tree, 'h2')
        bookParticle(self.tree, 'hh')

        bookParticle(self.tree, 'b1')
        bookParticle(self.tree, 'b2')
        bookParticle(self.tree, 'b3')
        bookParticle(self.tree, 'b4')

        bookMet(self.tree, 'met')

        self.reader = ROOT.TMVA.Reader()

        self.bdt_b1_pt    = array.array('f',[0])
        self.bdt_b1_eta   = array.array('f',[0])
        self.bdt_b1_phi   = array.array('f',[0])

        self.bdt_b2_pt    = array.array('f',[0])
        self.bdt_b2_eta   = array.array('f',[0])
        self.bdt_b2_phi   = array.array('f',[0])

        self.bdt_b3_pt    = array.array('f',[0])
        self.bdt_b3_eta   = array.array('f',[0])
        self.bdt_b3_phi   = array.array('f',[0])

        self.bdt_b4_pt    = array.array('f',[0])
        self.bdt_b4_eta   = array.array('f',[0])
        self.bdt_b4_phi   = array.array('f',[0])

        self.bdt_h1_pt    = array.array('f',[0])
        self.bdt_h1_eta   = array.array('f',[0])
        self.bdt_h1_phi   = array.array('f',[0])
        self.bdt_h1_m     = array.array('f',[0])

        self.bdt_h2_pt    = array.array('f',[0])
        self.bdt_h2_eta   = array.array('f',[0])
        self.bdt_h2_phi   = array.array('f',[0])
        self.bdt_h2_m     = array.array('f',[0])

        self.bdt_hh_pt    = array.array('f',[0])
        self.bdt_hh_eta   = array.array('f',[0])
        self.bdt_hh_phi   = array.array('f',[0])
        self.bdt_hh_m     = array.array('f',[0])

        self.reader.AddVariable('b1_pt',  self.bdt_b1_pt )
        self.reader.AddVariable('b1_eta',  self.bdt_b1_eta)
        self.reader.AddVariable('b1_phi',  self.bdt_b1_phi)

        self.reader.AddVariable('b2_pt',  self.bdt_b2_pt )
        self.reader.AddVariable('b2_eta',  self.bdt_b2_eta)
        self.reader.AddVariable('b2_phi',  self.bdt_b2_phi)

        self.reader.AddVariable('b3_pt',  self.bdt_b3_pt )
        self.reader.AddVariable('b3_eta',  self.bdt_b3_eta)
        self.reader.AddVariable('b3_phi',  self.bdt_b3_phi)

        self.reader.AddVariable('b4_pt',  self.bdt_b4_pt )
        self.reader.AddVariable('b4_eta',  self.bdt_b4_eta)
        self.reader.AddVariable('b4_phi',  self.bdt_b4_phi)

        self.reader.AddVariable('h1_pt',  self.bdt_h1_pt )
        self.reader.AddVariable('h1_eta',  self.bdt_h1_eta)
        self.reader.AddVariable('h1_phi',  self.bdt_h1_phi)
        self.reader.AddVariable('h1_m',  self.bdt_h1_m)

        self.reader.AddVariable('h2_pt',  self.bdt_h2_pt )
        self.reader.AddVariable('h2_eta',  self.bdt_h2_eta)
        self.reader.AddVariable('h2_phi',  self.bdt_h2_phi)
        self.reader.AddVariable('h2_m',  self.bdt_h2_m)

        self.reader.AddVariable('hh_pt',  self.bdt_hh_pt )
        self.reader.AddVariable('hh_eta',  self.bdt_hh_eta)
        self.reader.AddVariable('hh_phi',  self.bdt_hh_phi)
        self.reader.AddVariable('hh_m',  self.bdt_hh_m)

        path = "/eos/user/s/selvaggi/Analysis/TMVA/hhbbbb_v3/lambda100_5f/weights/BDT_BDT_lambda100_5f.weights.xml"
        
	self.reader.BookMVA("BDT",path)
        self.tree.var('tmva_bdt', float)


    def process(self, event):
        self.tree.reset()

        ## these pairs contain overlap
        hbbs  = getattr(event, self.cfg_ana.hbbs)
        bs    = getattr(event, self.cfg_ana.bs)
        hbbs.sort(key=lambda x: abs(x.m()-125.))

        if len(bs) > 3:

            def bestHiggsPair(hbbs):

                higgs_pairs = []

                for p in hbbs:
                    p1=p.leg1()
                    p2=p.leg2()

                    for m in hbbs:
                        m1=m.leg1()
                        m2=m.leg2()

                        if m1 == p1 or m1 == p2 or m2 == p1 or m2 == p2:
                            continue

                        fillpair = True
                        for hp in higgs_pairs:

                           if m in hp and p in hp:
                               fillpair = False

                        if fillpair:
                            higgs_pairs.append((p,m))

                higgs_pairs.sort(key=lambda x: abs(x[0].m()-x[1].m()))
                return higgs_pairs[0]

            higgs_pair = bestHiggsPair(hbbs)
                        
            self.tree.fill('weight' , event.weight )
            # jet multiplicities
            self.tree.fill('nbjets' , len(event.selected_bs) )
            self.tree.fill('nljets' , len(event.selected_lights) )
            self.tree.fill('njets' , len(event.selected_lights) + len(event.selected_bs))
            self.tree.fill('nlep' , len(event.selected_leptons))
            
            # missing Et
            fillMet(self.tree, 'met', event.met)
            
            #bs.sort(key=lambda x: x.pt(), reverse=True)
            
            hh = Resonance( higgs_pair[0], higgs_pair[1], 25)

            higgses = [ higgs_pair[0], higgs_pair[1] ]
            higgses.sort(key=lambda x: x.pt(), reverse=True)

            self.bdt_b1_pt    [0]= bs[0].p4().Pt()
            self.bdt_b1_eta   [0]= bs[0].p4().Eta()
            self.bdt_b1_phi   [0]= bs[0].p4().Phi()

            self.bdt_b2_pt    [0]= bs[1].p4().Pt()
            self.bdt_b2_eta   [0]= bs[1].p4().Eta()
            self.bdt_b2_phi   [0]= bs[1].p4().Phi()

            self.bdt_b3_pt    [0]= bs[2].p4().Pt()
            self.bdt_b3_eta   [0]= bs[2].p4().Eta()
            self.bdt_b3_phi   [0]= bs[2].p4().Phi()

            self.bdt_b4_pt    [0]= bs[3].p4().Pt()
            self.bdt_b4_eta   [0]= bs[3].p4().Eta()
            self.bdt_b4_phi   [0]= bs[3].p4().Phi()

            self.bdt_h1_pt    [0]= higgses[0].p4().Pt()
            self.bdt_h1_eta   [0]= higgses[0].p4().Eta()
            self.bdt_h1_phi   [0]= higgses[0].p4().Phi()
            self.bdt_h1_m     [0]= higgses[0].p4().M()

            self.bdt_h2_pt    [0]= higgses[1].p4().Pt()
            self.bdt_h2_eta   [0]= higgses[1].p4().Eta()
            self.bdt_h2_phi   [0]= higgses[1].p4().Phi()
            self.bdt_h2_m     [0]= higgses[1].p4().M()

            self.bdt_hh_pt    [0]= hh.p4().Pt()
            self.bdt_hh_eta   [0]= hh.p4().Eta()
            self.bdt_hh_phi   [0]= hh.p4().Phi()
            self.bdt_hh_m     [0]= hh.p4().M()

            mva_value = self.reader.EvaluateMVA("BDT")
            print mva_value

            fillParticle(self.tree, 'hh', hh)
            fillParticle(self.tree, 'h1', higgses[0])
            fillParticle(self.tree, 'h2', higgses[1])
            fillParticle(self.tree, 'b1', bs[0])
            fillParticle(self.tree, 'b2', bs[1])
            fillParticle(self.tree, 'b3', bs[2])
            fillParticle(self.tree, 'b4', bs[3])

            self.tree.fill( 'tmva_bdt', mva_value)
            self.tree.tree.Fill()
        
        
    def write(self, setup):
        self.rootfile.Write()
        self.rootfile.Close()

