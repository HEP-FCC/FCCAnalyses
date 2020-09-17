from heppy.framework.analyzer import Analyzer
from heppy.statistics.tree import Tree
from heppy.analyzers.ntuple import *
from heppy.particles.tlv.resonance import Resonance2 as Resonance
from ROOT import TFile, TVector2, TVector3, TLorentzVector
import itertools

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

        # leptons and jets ordered in pt
        bookParticle(self.tree, 'lpt1')
        bookParticle(self.tree, 'lpt2')
        bookParticle(self.tree, 'jpt1')
        bookParticle(self.tree, 'jpt2')

        # leptons and jets ordered in abs(eta)
        bookParticle(self.tree, 'leta1')
        bookParticle(self.tree, 'leta2')
        bookParticle(self.tree, 'jeta1')
        bookParticle(self.tree, 'jeta2')

        self.tree.var('is_sf', float)
        self.tree.var('is_of', float)

        self.tree.var('mt', float)
        self.tree.var('mr', float)

        self.tree.var('mll', float)
        self.tree.var('mjj', float)

        self.tree.var('ptll', float)
        self.tree.var('ptjj', float)

        self.tree.var('detajj', float)
        self.tree.var('detall', float)

        self.tree.var('dphill', float)
        self.tree.var('dphijj', float)

        self.tree.var('dphillmet', float)


        bookMet(self.tree, 'met')

    def process(self, event):
        self.tree.reset()
        
        # just the ll pair added into a particle for convenience
        higgses = event.higgses
	
        leptons = event.selected_leptons
        leptons.sort(key=lambda x: x.pt(), reverse = True)

        jets = event.jets_nolepton
        jets.sort(key=lambda x: x.pt(), reverse = True)

        
        met = event.met

        '''
        for jet in jets:
           print jet
        '''

        sign = lambda x: x and (1, -1)[x < 0]
        same_sign_pair = []
        # this gives orders pairs (so twice as many as we need)
        for i in itertools.permutations(leptons, 2):
            #print 'new lep pair', i[0], i[1]
            if sign(i[0].pdgid()) == sign(i[1].pdgid()):
                same_sign_pair.append(i)

        if len(same_sign_pair) > 0 and len(jets) > 1:
            
            self.tree.fill('weight' , 1. )
            self.tree.fill('njets' ,  len(jets))
            self.tree.fill('nleptons' , len(leptons))

            l1 = leptons[0]
            l2 = leptons[1]
            j1 = jets[0]
            j2 = jets[1]

            fillParticle(self.tree, 'lpt1', l1)
            fillParticle(self.tree, 'lpt2', l2)

            fillParticle(self.tree, 'jpt1', j1)
            fillParticle(self.tree, 'jpt2', j2)

            leptons.sort(key=lambda x: abs(x.eta()))
            jets.sort(key=lambda x: abs(x.eta()))

            l1 = leptons[0]
            l2 = leptons[1]
            j1 = jets[0]
            j2 = jets[1]

            fillParticle(self.tree, 'leta1', l1)
            fillParticle(self.tree, 'leta2', l2)

            fillParticle(self.tree, 'jeta1', j1)
            fillParticle(self.tree, 'jeta2', j2)

            if abs(l1.pdgid()) == abs(l2.pdgid()):
                self.tree.fill('is_sf' , 1.0 )
                self.tree.fill('is_of' , 0.0 )
            else:
                self.tree.fill('is_sf' , 0.0 )
                self.tree.fill('is_of' , 1.0 )


            higgs = higgses[0]
            mll = higgs.m()

            dphi_ll = TVector2.Phi_mpi_pi(l1.phi() - l2.phi())
            dphi_jj = TVector2.Phi_mpi_pi(j1.phi() - j2.phi())
            dphi_llmet = TVector2.Phi_mpi_pi(higgs.phi() - event.met.phi())

            mt = math.sqrt(2*higgs.pt()*event.met.pt()*(1 - math.cos(dphi_llmet)))


            mll = higgs.m()
            ptll = higgs.pt()
	    met = event.met.pt()
            hpx  = higgs.pt()*math.cos(higgs.phi())
            hpy  = higgs.pt()*math.sin(higgs.phi())
            metx = event.met.pt()*math.cos(event.met.phi())
            mety = event.met.pt()*math.sin(event.met.phi())
	    met_d_ptll = metx*hpx + mety*hpy
            mr = math.sqrt((mll**2 - met_d_ptll + math.sqrt( (mll**2 + ptll**2)*(mll**2 + met**2) )))

            self.tree.fill('mt' , mt )
            self.tree.fill('mr' , mr )

            mjj = math.sqrt( (j1.e()+j2.e())**2 - (j1.p4().Px()+j2.p4().Px())**2  - (j1.p4().Py()+j2.p4().Py())**2  - (j1.p4().Pz()+j2.p4().Pz())**2 )
            ptjj = math.sqrt( (j1.p4().Px()+j2.p4().Px())**2  + (j1.p4().Py()+j2.p4().Py())**2 )


            self.tree.fill('mll' , mll )
            self.tree.fill('mjj' , mjj )

            self.tree.fill('ptll' , higgs.pt())
            self.tree.fill('ptjj' , ptjj )


            deta_ll = abs(l1.eta() - l2.eta())
            deta_jj = abs(j1.eta() - j2.eta())

            self.tree.fill('detall' , deta_ll)
            self.tree.fill('detajj' , deta_jj)

            #mll2 = math.sqrt( (l1.e()+l2.e())**2 - (l1.p4().Px()+l2.p4().Px())**2  - (l1.p4().Py()+l2.p4().Py())**2  - (l1.p4().Pz()+l2.p4().Pz())**2 )

            self.tree.fill('dphill' , abs(dphi_ll) )
            self.tree.fill('dphijj' , abs(dphi_jj) )
            self.tree.fill('dphillmet' , abs(dphi_llmet) )

            fillMet(self.tree, 'met', event.met)

            self.tree.tree.Fill()
        
    def write(self, setup):
        self.rootfile.Write()
        self.rootfile.Close()

