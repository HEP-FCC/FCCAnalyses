from heppy.framework.analyzer import Analyzer
from heppy.statistics.tree import Tree
from heppy.analyzers.ntuple import *
from heppy.particles.tlv.resonance import Resonance2 as Resonance
from heppy.utils.deltar import matchObjectCollection, deltaR
from heppy.particles.tlv.particle import Particle

from ROOT import TFile, TLorentzVector
import ROOT
import array

#ROOT.gROOT.ProcessLine('.L /afs/cern.ch/work/s/selvaggi/private/FCCSW/heppy/FCChhAnalyses/FCChh/hhbbtahtah/mt2.h+')
#ROOT.gROOT.ProcessLine('.L /afs/cern.ch/work/s/selvaggi/private/FCCSW/heppy/FCChhAnalyses/FCChh/hhbbtahtah/chi2.cxx+')

from ctypes import cdll
import ctypes as ct
#lib = cdll.LoadLibrary('/afs/cern.ch/work/s/selvaggi/private/FCCSW/heppy/FCChhAnalyses/FCChh/hhbbtahtah/libfoo.so')
lib = cdll.LoadLibrary('/afs/cern.ch/work/s/selvaggi/private/FCCSW/heppy/FCChhAnalyses/FCChh/hhbbtahtah/libmt2.so')

'''class Foo(object):
    def __init__(self):
        self.obj = lib.Foo_new()

    def bar(self):
        lib.Foo_bar(self.obj)
'''

class asymm_mt2_lester_bisect(object):
    def __init__(self):

        lib.asymm_mt2_lester_bisect_new.restype = ct.c_void_p
        lib.asymm_mt2_lester_bisect_get_mT2.argtypes = [ct.c_void_p, ct.c_double, ct.c_double, ct.c_double, ct.c_double, ct.c_double, ct.c_double, ct.c_double, ct.c_double, ct.c_double, ct.c_double, ct.c_bool]
        lib.asymm_mt2_lester_bisect_get_mT2.restype = ct.c_double
        self.obj = lib.asymm_mt2_lester_bisect_new()
    
    def get_mT2(self, mVis1, pxVis1, pyVis1, mVis2, pxVis2, pyVis2, pxMiss, pyMiss, mInvis1, mInvis2, desiredPrecisionOnMT2, useDeciSectionsInitially):
        return lib.asymm_mt2_lester_bisect_get_mT2(self.obj, mVis1, pxVis1, pyVis1, mVis2, pxVis2, pyVis2, pxMiss, pyMiss, mInvis1, mInvis2, desiredPrecisionOnMT2, useDeciSectionsInitially) 



class TreeProducer(Analyzer):

    def beginLoop(self, setup):
        super(TreeProducer, self).beginLoop(setup)
        self.rootfile = TFile('/'.join([self.dirName,
                                        'tree.root']),
                              'recreate')
        self.tree = Tree( 'events', '')
        self.tree.var('weight', float)

        bookParticle(self.tree, 'ta1')
        self.tree.var('ta1_mt', float)
        bookParticle(self.tree, 'ta2')
        self.tree.var('ta2_mt', float)
        bookParticle(self.tree, 'b1')
        bookParticle(self.tree, 'b2')        
        bookParticle(self.tree, 'j1')
        bookParticle(self.tree, 'j2')        
        bookParticle(self.tree, 'htata')
        bookParticle(self.tree, 'htata_metcorr')
        bookParticle(self.tree, 'hbb')
        bookParticle(self.tree, 'hh')
        bookParticle(self.tree, 'hh_metcorr')

        self.tree.var('mT2', float)
        self.tree.var('sT', float)

        self.tree.var('ntajets', float)
        self.tree.var('nbjets', float)
        self.tree.var('nljets', float)
        self.tree.var('njets', float)
        self.tree.var('nlep', float)
        self.tree.var('drbb', float)
        self.tree.var('drtata', float)

        bookMet(self.tree, 'met')

        self.reader = ROOT.TMVA.Reader()

        self.bdt_ta1_pt    = array.array('f',[0])
        self.bdt_ta1_eta    = array.array('f',[0])
        self.bdt_ta1_phi    = array.array('f',[0])
        self.bdt_ta2_pt    = array.array('f',[0])
        self.bdt_ta2_eta    = array.array('f',[0])
        self.bdt_ta2_phi    = array.array('f',[0])
        self.bdt_b1_pt    = array.array('f',[0])
        self.bdt_b1_eta    = array.array('f',[0])
        self.bdt_b1_phi    = array.array('f',[0])
        self.bdt_b2_pt    = array.array('f',[0])
        self.bdt_b2_eta    = array.array('f',[0])
        self.bdt_b2_phi    = array.array('f',[0])
        self.bdt_met_pt    = array.array('f',[0])
        self.bdt_met_phi    = array.array('f',[0])
        self.bdt_met_px    = array.array('f',[0])
        self.bdt_met_py    = array.array('f',[0])
        self.bdt_htata_pt    = array.array('f',[0])
        self.bdt_htata_eta    = array.array('f',[0])
        self.bdt_htata_phi    = array.array('f',[0])
        self.bdt_htata_m    = array.array('f',[0])
        self.bdt_hbb_pt    = array.array('f',[0])
        self.bdt_hbb_eta    = array.array('f',[0])
        self.bdt_hbb_phi    = array.array('f',[0])
        self.bdt_hbb_m    = array.array('f',[0])
        self.bdt_hh_pt    = array.array('f',[0])
        self.bdt_hh_eta    = array.array('f',[0])
        self.bdt_hh_phi    = array.array('f',[0])
        self.bdt_hh_m    = array.array('f',[0])
        self.bdt_ta1_mt    = array.array('f',[0])
        self.bdt_ta2_mt    = array.array('f',[0])        
        self.bdt_mT2    = array.array('f',[0])
        self.bdt_sT    = array.array('f',[0])
        self.bdt_njets    = array.array('f',[0])
        self.bdt_nbjets    = array.array('f',[0])
        self.bdt_ntajets    = array.array('f',[0])
        #self.bdt_nlep    = array.array('f',[0])
        
        self.reader.AddVariable('ta1_pt'     , self.bdt_ta1_pt)
        self.reader.AddVariable('ta1_eta'    , self.bdt_ta1_eta)
        self.reader.AddVariable('ta1_phi'    , self.bdt_ta1_phi)
        self.reader.AddVariable('ta2_pt'     , self.bdt_ta2_pt)
        self.reader.AddVariable('ta2_eta'    , self.bdt_ta2_eta)
        self.reader.AddVariable('ta2_phi'    , self.bdt_ta2_phi)
        self.reader.AddVariable('b1_pt'      , self.bdt_b1_pt)
        self.reader.AddVariable('b1_eta'     , self.bdt_b1_eta)
        self.reader.AddVariable('b1_phi'     , self.bdt_b1_phi)
        self.reader.AddVariable('b2_pt'      , self.bdt_b2_pt)
        self.reader.AddVariable('b2_eta'     , self.bdt_b2_eta)
        self.reader.AddVariable('b2_phi'     , self.bdt_b2_phi)
        self.reader.AddVariable('met_pt'     , self.bdt_met_pt)
        self.reader.AddVariable('met_phi'    , self.bdt_met_phi)
        self.reader.AddVariable('met_px'     , self.bdt_met_px)
        self.reader.AddVariable('met_py'     , self.bdt_met_py)
        self.reader.AddVariable('htata_pt'   , self.bdt_htata_pt)
        self.reader.AddVariable('htata_eta'  , self.bdt_htata_eta)
        self.reader.AddVariable('htata_phi'  , self.bdt_htata_phi)
        self.reader.AddVariable('htata_m'    , self.bdt_htata_m)
        self.reader.AddVariable('hbb_pt'     , self.bdt_hbb_pt)
        self.reader.AddVariable('hbb_eta'    , self.bdt_hbb_eta)
        self.reader.AddVariable('hbb_phi'    , self.bdt_hbb_phi)
        self.reader.AddVariable('hbb_m'      , self.bdt_hbb_m)
        self.reader.AddVariable('hh_pt'      , self.bdt_hh_pt)
        self.reader.AddVariable('hh_eta'     , self.bdt_hh_eta)
        self.reader.AddVariable('hh_phi'     , self.bdt_hh_phi)
        self.reader.AddVariable('hh_m'       , self.bdt_hh_m)
        self.reader.AddVariable('ta1_mt'     , self.bdt_ta1_mt)
        self.reader.AddVariable('ta2_mt'     , self.bdt_ta2_mt)
        self.reader.AddVariable('mT2'        , self.bdt_mT2)
        self.reader.AddVariable('sT'         , self.bdt_sT)
        self.reader.AddVariable('njets'      , self.bdt_njets)
        self.reader.AddVariable('nbjets'     , self.bdt_nbjets)
        self.reader.AddVariable('ntajets'    , self.bdt_ntajets)
        #self.reader.AddVariable('nlep'       , self.bdt_nlep)

        #path = "/afs/cern.ch/work/s/selvaggi/private/Analysis/FCC/analysis/TMVAfacility/HH_vs_Top_lowstat/weights/"
        path = "/eos/user/s/selvaggi/Analysis/TMVA/hhbbtahtah_v3/lambda100_5f/weights/"
        self.reader.BookMVA("BDT",path+"/BDT_BDT_lambda100_5f.weights.xml")
        self.tree.var('tmva_bdt', float)


    def process(self, event):
        self.tree.reset()
        htatas = getattr(event, self.cfg_ana.htatas)
        hbbs  = getattr(event, self.cfg_ana.hbbs)
        met = event.met

        htatas.sort(key=lambda x: abs(x.m()-125.))
        hbbs.sort(key=lambda x: abs(x.m()-125.))

        bs = event.selected_bs
        taus = event.selected_taus
        lights = event.selected_lights
        leptons = event.selected_leptons
        
        #print '-------------------'

        #print len(htatas), len(hbbs)
        #print len(taus), len(bs)

        #for tau in taus:
        #    print tau.charge

        #print ROOT.return2()
        #f = Foo()
        #f.bar() #and you will see "Hello" on the screen

        '''
        mVisA = 10.; # mass of visible object on side A.  Must be >=0.
        pxA = 20.; # x momentum of visible object on side A.
        pyA = 30.; # y momentum of visible object on side A.

        mVisB = 10.; # mass of visible object on side B.  Must be >=0.
        pxB = -20.; # x momentum of visible object on side B.
        pyB = -30.; # y momentum of visible object on side B.

        pxMiss = -5.; # x component of missing transverse momentum.
        pyMiss = -5.; # y component of missing transverse momentum.

        chiA = 4.; # hypothesised mass of invisible on side A.  Must be >=0.
        chiB = 7.; # hypothesised mass of invisible on side B.  Must be >=0.

        desiredPrecisionOnMt2 = 0.; # Must be >=0.  If 0 alg aims for machine precision.  if >0, MT2 computed to supplied absolute precision.
        useDeciSectionsInitially=True

        asymm_mt2 = asymm_mt2_lester_bisect()
        print '-----------------------------------------'
        MT2 =  asymm_mt2.get_mT2(
           mVisA, pxA, pyA,
           mVisB, pxB, pyB,
           pxMiss, pyMiss,
           chiA, chiB,
           desiredPrecisionOnMt2,
           useDeciSectionsInitially)
        
        print 'MT2', MT2
        '''

        # fully hadronic selection
        if len(taus) > 1 and len(bs) > 1 and len(leptons) == 0:

            self.tree.fill('weight' , event.weight )
            #print  event.weight
            fillParticle(self.tree, 'ta1', taus[0])
            fillParticle(self.tree, 'ta2', taus[1])
            fillParticle(self.tree, 'b1', bs[0])
            fillParticle(self.tree, 'b2', bs[1])

            '''
            def mTsq(bT, cT, mB, mC):
                eB = math.sqrt(mB*mB+ bT*bT)
                eC = math.sqrt(mC*mC+ cT*cT)
                return mB*mB+mC*mC+2*(eB*eC - bT*cT)

            def smT2(bt1, bt2):
                return max(math.sqrt(bt1),math.sqrt(bt2))

            mTsq1 = mTsq(taus[0].p4().Vect().XYvector(), bs[0].p4().Vect().XYvector(), taus[0].p4().M(), bs[0].p4().M())
            mTsq2 = mTsq(taus[1].p4().Vect().XYvector(), bs[1].p4().Vect().XYvector(), taus[1].p4().M(), bs[1].p4().M())

            smTsq = smT2(mTsq1, mTsq2)
            #print mTsq1, mTsq2, smTsq
            '''

            mVisA = bs[0].p4().M(); # mass of visible object on side A.  Must be >=0.
            pxA   = bs[0].p4().Px(); # x momentum of visible object on side A.
            pyA   = bs[0].p4().Py(); # y momentum of visible object on side A.

            mVisB = bs[1].p4().M(); # mass of visible object on side A.  Must be >=0.
            pxB   = bs[1].p4().Px(); # x momentum of visible object on side A.
            pyB   = bs[1].p4().Py(); # y momentum of visible object on side A.

            pxMiss = taus[0].p4().Px() + taus[1].p4().Px() + met.p4().Px() # x component of missing transverse momentum.
            pyMiss = taus[0].p4().Py() + taus[1].p4().Py() + met.p4().Py() # x component of missing transverse momentum.

            chiA = taus[0].p4().M(); # hypothesised mass of invisible on side A.  Must be >=0.
            chiB = taus[1].p4().M(); # hypothesised mass of invisible on side B.  Must be >=0. 
 
            desiredPrecisionOnMt2 = 0.; # Must be >=0.  If 0 alg aims for machine precision.  if >0, MT2 computed to supplied absolute precision.
            useDeciSectionsInitially=True

            asymm_mt2 = asymm_mt2_lester_bisect()

            MT2 =  asymm_mt2.get_mT2(
               mVisA, pxA, pyA,
               mVisB, pxB, pyB,
               pxMiss, pyMiss,
               chiA, chiB,
               desiredPrecisionOnMt2,
               useDeciSectionsInitially)

            #print 'MT2', MT2

            self.tree.fill('mT2' , MT2 )

            if len(lights)>0:
                fillParticle(self.tree, 'j1', lights[0])
                if len(lights)>1:
                    fillParticle(self.tree, 'j2', lights[1])

            def computeMT(taup4, metp4):
                scalar_prod = taup4.Px()*metp4.Px() +  taup4.Py()*metp4.Py() 
                return math.sqrt(2*(taup4.Pt()*metp4.Pt() - scalar_prod))

            mt1 = computeMT(taus[0].p4(), met.p4())
            mt2 = computeMT(taus[1].p4(), met.p4())

            self.tree.fill('ta1_mt' , mt1 )
            self.tree.fill('ta2_mt' , mt2 )

            st = taus[0].p4().Pt() + taus[1].p4().Pt() + bs[0].p4().Pt() + bs[0].p4().Pt() +  met.p4().Pt()
            self.tree.fill('sT' , st )

            fillMet(self.tree, 'met', met)
            fillParticle(self.tree, 'htata', htatas[0])
            fillParticle(self.tree, 'hbb', hbbs[0])

            htata_metcorr_p4 = taus[0].p4() + taus[1].p4() + met.p4()
            htata_metcorr  = Particle(25, 0, htata_metcorr_p4, 1)
            
            fillParticle(self.tree, 'htata_metcorr', htata_metcorr)

            hh = Resonance( htatas[0], hbbs[0], 25)
            hh_metcorr = Resonance( htata_metcorr, hbbs[0], 25)

            fillParticle(self.tree, 'hh', hh)
            fillParticle(self.tree, 'hh_metcorr', hh_metcorr)

            self.tree.fill('nbjets' , len(event.selected_bs) )
            self.tree.fill('nljets' , len(event.selected_lights) )
            self.tree.fill('njets' , len(event.selected_lights) + len(event.selected_bs) + len(event.selected_taus) )
            self.tree.fill('nlep' , len(event.selected_leptons) )
            self.tree.fill('ntajets' , len(event.selected_taus) )

            drbb = deltaR(bs[0], bs[1])
            drtata = deltaR(taus[0], taus[1])

            self.tree.fill('drtata' , drtata)
            self.tree.fill('drbb' , drbb)

            # here fill all variables for BDT
            self.bdt_ta1_pt   [0] =  taus[0].p4().Pt()
            self.bdt_ta1_eta   [0] =  taus[0].p4().Eta()
            self.bdt_ta1_phi   [0] =  taus[0].p4().Phi()
            self.bdt_ta2_pt   [0] =  taus[1].p4().Pt()
            self.bdt_ta2_eta   [0] =  taus[1].p4().Eta()  
            self.bdt_ta2_phi   [0] =  taus[1].p4().Phi()  
            self.bdt_b1_pt    [0] =  bs[0].p4().Pt()
            self.bdt_b1_eta    [0] =  bs[0].p4().Eta()
            self.bdt_b1_phi    [0] =  bs[0].p4().Phi()  
            self.bdt_b2_pt    [0] =  bs[1].p4().Pt()
            self.bdt_b2_eta    [0] =  bs[1].p4().Eta()
            self.bdt_b2_phi    [0] =  bs[1].p4().Phi() 
            self.bdt_met_pt   [0] =  met.p4().Pt()
            self.bdt_met_phi   [0] =  met.p4().Phi()
            self.bdt_met_px   [0] =  met.p4().Px()
            self.bdt_met_py   [0] =  met.p4().Py()
            self.bdt_htata_pt [0] =  htatas[0].p4().Pt()
            self.bdt_htata_eta [0] =  htatas[0].p4().Eta()
            self.bdt_htata_phi [0] =  htatas[0].p4().Phi() 
            self.bdt_htata_m  [0] =  htatas[0].p4().M()
            self.bdt_hbb_pt   [0] =  hbbs[0].p4().Pt()
            self.bdt_hbb_eta   [0] =  hbbs[0].p4().Eta()
            self.bdt_hbb_phi   [0] =  hbbs[0].p4().Phi() 
            self.bdt_hbb_m    [0] =  hbbs[0].p4().M()
            self.bdt_hh_pt    [0] =  hh.p4().Pt()
            self.bdt_hh_eta    [0] =  hh.p4().Eta()
            self.bdt_hh_phi    [0] =  hh.p4().Phi() 
            self.bdt_hh_m     [0] =  hh.p4().M()
            self.bdt_ta1_mt   [0] =  mt1
            self.bdt_ta2_mt   [0] =  mt2
            self.bdt_mT2      [0] =  MT2                                                                                                                                                                         
            self.bdt_sT       [0] =  st                                                                                                                                                                          
            self.bdt_njets    [0] =  len(event.selected_lights) + len(event.selected_bs) + len(event.selected_taus)                                                                                              
            self.bdt_nbjets   [0] =  len(event.selected_bs)                                                                                                                                                      
            self.bdt_ntajets  [0] =  len(event.selected_taus)                                                                                                                                                    
            #self.bdt_nlep     [0] =  len(event.selected_leptons)                                                                                                                                                 

            #print MT2, ",", s ,",", len(event.selected_lights) + len(event.selected_bs) + len(event.selected_taus), ",", len(event.selected_bs) ,",", len(event.selected_taus) ,",", len(event.selected_leptons)t

            mva_value = self.reader.EvaluateMVA("BDT")
            #print mva_value
            self.tree.fill( 'tmva_bdt', mva_value)
            self.tree.tree.Fill()

        
    def write(self, setup):
        self.rootfile.Write()
        self.rootfile.Close()

