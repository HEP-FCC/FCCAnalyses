from heppy.framework.analyzer import Analyzer
from heppy.statistics.tree import Tree
from heppy.analyzers.ntuple import *
from heppy.particles.tlv.resonance import Resonance2 as Resonance
from heppy.utils.deltar import matchObjectCollection, deltaR
from heppy.FCChhAnalyses.analyzers.TRFbtag import *

from ROOT import TFile, TLorentzVector, TMVA
import itertools
import array

class TreeProducer(Analyzer):

    def beginLoop(self, setup):
        super(TreeProducer, self).beginLoop(setup)
        self.rootfile = TFile('/'.join([self.dirName,
                                        'tree.root']),
                              'recreate')
        self.tree = Tree( 'events', '')
        self.tree.var('weight', float)
        self.tree.var('nbjets', float)

        self.tree.var('weight_0tagex', float)
        self.tree.var('weight_1tagex', float)
        self.tree.var('weight_2tagex', float)
        self.tree.var('weight_3tagex', float)
        self.tree.var('weight_4tagex', float)

        bookParticle(self.tree, 'l')
        bookMet(self.tree, 'met')
        
        # fatjet stuff
        for flavour in ['higgs', 'top']:

            bookParticle(self.tree, '{}jet'.format(flavour))
            bookParticle(self.tree, 'softDropped_{}jet'.format(flavour))

            self.tree.var('{}jet_tau1'.format(flavour), float)       
            self.tree.var('{}jet_tau2'.format(flavour), float)
            self.tree.var('{}jet_tau3'.format(flavour), float)
            self.tree.var('{}jet_tau32'.format(flavour), float)
            self.tree.var('{}jet_tau31'.format(flavour), float)
            self.tree.var('{}jet_tau21'.format(flavour), float)

            self.tree.var('{}jet_flow15'.format(flavour), float)
            self.tree.var('{}jet_flow25'.format(flavour), float)
            self.tree.var('{}jet_flow35'.format(flavour), float)
            self.tree.var('{}jet_flow45'.format(flavour), float)
            self.tree.var('{}jet_flow55'.format(flavour), float)

            self.tree.var('{}jet_njs'.format(flavour), float)
            self.tree.var('{}jet_nbs'.format(flavour), float)
            self.tree.var('{}jet_ncs'.format(flavour), float)
            self.tree.var('{}jet_nls'.format(flavour), float)
            self.tree.var('{}jet_mjs'.format(flavour), float)
            self.tree.var('{}jet_mbs'.format(flavour), float)
            ##self.tree.var('{}jet_bdt_th'.format(flavour), float)

        ## for MVA
        #self.reader            = TMVA.Reader()
        #
        #self.bdt_tau1              = array.array('f',[0])
        #self.bdt_tau2              = array.array('f',[0])
        #self.bdt_tau3              = array.array('f',[0])
        #self.bdt_tau21             = array.array('f',[0])
        #self.bdt_tau31             = array.array('f',[0])
        #self.bdt_tau32             = array.array('f',[0])
        #self.bdt_flow15            = array.array('f',[0])
        #self.bdt_flow25            = array.array('f',[0])
        #self.bdt_flow35            = array.array('f',[0])
        #self.bdt_flow45            = array.array('f',[0])
        #self.bdt_flow55            = array.array('f',[0])
        #self.bdt_jet_m             = array.array('f',[0])
        #self.bdt_softDropped_jet_m = array.array('f',[0])
        #self.bdt_jet_nbs           = array.array('f',[0])

        #self.reader.AddVariable('jet_m',             self.bdt_jet_m )
        #self.reader.AddVariable('softDropped_jet_m', self.bdt_softDropped_jet_m)
        #self.reader.AddVariable('jet_tau1',          self.bdt_tau1          )
        #self.reader.AddVariable('jet_tau2',          self.bdt_tau2          )
        #self.reader.AddVariable('jet_tau3',          self.bdt_tau3          )
        #self.reader.AddVariable('jet_tau32',         self.bdt_tau32         )
        #self.reader.AddVariable('jet_tau31',         self.bdt_tau31         )
        #self.reader.AddVariable('jet_tau21',         self.bdt_tau21         )
        #self.reader.AddVariable('jet_flow15',        self.bdt_flow15        )
        #self.reader.AddVariable('jet_flow25',        self.bdt_flow25        )
        #self.reader.AddVariable('jet_flow35',        self.bdt_flow35        )
        #self.reader.AddVariable('jet_flow45',        self.bdt_flow45        )
        #self.reader.AddVariable('jet_flow55',        self.bdt_flow55        )
        #self.reader.AddVariable('jet_nbs',           self.bdt_jet_nbs       )
        #
        ##path = "/afs/cern.ch/work/s/selvaggi/private/FCCSW/heppy/FCChhAnalyses/tth_boosted/"
        #path = "/eos/experiment/fcc/hh/analyses/Higgs/ttH/BDT/"
        #self.reader.BookMVA("BDT",str(path)+"BDT_BDT_Higgs_vs_Top.weights.xml")
    
    def process(self, event):
        self.tree.reset()
        gen_bs = getattr(event, self.cfg_ana.gen_bs)
        gen_higgses = getattr(event, self.cfg_ana.gen_higgses)
        gen_higgses.sort(key=lambda x: x.pt(), reverse = True)
        gen_tops = getattr(event, self.cfg_ana.gen_tops)
        gen_tops.sort(key=lambda x: x.pt(), reverse = True)
        fatjets = getattr(event, self.cfg_ana.fatjets)
        leptons = getattr(event, self.cfg_ana.selected_leptons)
        bjets = event.selected_bs
        for_jets = event.jets_nolepton
        jets = event.jets_30

        #_________________________________________________________________
        # compute eflow, tau_ij and bdt variables

        R = 1.5

        use_DELPHES=False
        jet_forTRF=[]
        jetin_forTRF=[]

        # fill jet collection to compute TRF -> use all jets
        for j in for_jets:
            ipdg=0
            if use_DELPHES==True:
              ipdg = j.tags['flav']
              if ipdg!=4 and ipdg!=5 : ipdg=0
            else:
              ipdg = j.flavour
            jet_forTRF.append([j,ipdg])

        for jet in fatjets:
            
            setattr(jet, 'njs', 0)
            setattr(jet, 'nbs', 0)
            setattr(jet, 'ncs', 0)
            setattr(jet, 'nls', 0)
            setattr(jet, 'flow', [0]*5)
            setattr(jet, 'p4_js', TLorentzVector())
            setattr(jet, 'p4_bs', TLorentzVector())

            setattr(jet, 'tau32', -9.)
            setattr(jet, 'tau31', -9.)
            setattr(jet, 'tau21', -9.)
            
            #setattr(jet, 'bdt_th', -99.)
            
            if (jet.tau1 != 0.0):
                jet.tau31 = jet.tau3/jet.tau1
                jet.tau21 = jet.tau2/jet.tau1
            if (jet.tau2 != 0.0):
                jet.tau32 = jet.tau3/jet.tau2

            # counting the number of jets inside (R = 1.5 - 0.4 = 1.1) fatjet
            for j in for_jets:

                # fill different jets matched with fatjet
                drjjet = deltaR(j, jet)
                if drjjet < 1.1: 
                  jet.njs += 1
                  jet.p4_js += j.p4()
 
                  # get pdgID to compute TRF
                  ipdg=0
                  if use_DELPHES==True:
                    ipdg = j.tags['flav']
                    if ipdg!=4 and ipdg!=5 : ipdg=0
                  else:
                    ipdg = j.flavour

                  if ipdg==5 :
                      jet.nbs += 1
                      jet.p4_bs += j.p4()
                  elif ipdg==4 :
                      jet.ncs += 1
                  else :
                      jet.nls += 1

            # do eflow with constituents here
            constituent_vector = TLorentzVector()
            
            #print jet.pt, jet.flow
            for n in range(1,5+1):
                 #print n 
                 for constituent in jet.jetConstituents[1:]:
                     #print constituent.pt()
                     dR = jet.p4().DeltaR(constituent.p4())
                     if ((dR >= (n-1)/5.*R) and (dR < n/5.*R)):
                         #print 'in ring', dR
                         jet.flow[n-1] += abs(constituent.pt())/abs(jet.pt())
            
            #print jet.flow

            ## do what is needed to evaluate bdt here
            #self.bdt_tau1              [0] = jet.tau1
            #self.bdt_tau2              [0] = jet.tau2
            #self.bdt_tau3              [0] = jet.tau3
            #self.bdt_tau31             [0] = jet.tau31
            #self.bdt_tau21             [0] = jet.tau21
            #self.bdt_tau32             [0] = jet.tau32
            #self.bdt_flow15            [0] = jet.flow[0]
            #self.bdt_flow25            [0] = jet.flow[1]
            #self.bdt_flow35            [0] = jet.flow[2]
            #self.bdt_flow45            [0] = jet.flow[3]
            #self.bdt_flow55            [0] = jet.flow[4]
            #self.bdt_jet_m             [0] = jet.p4().M()
            #self.bdt_softDropped_jet_m [0] = jet.subjetsSoftDrop[0].p4().M()
            #self.bdt_jet_nbs           [0] = float(jet.nbs)
            #
            #jet.bdt_th = self.reader.EvaluateMVA("BDT")
            
        # highest bdt score is more higgs like
        #fatjets.sort(key=lambda x: x.bdt_th, reverse = True)

        
        # 1/ highest number of jets in fatjet is more top like 
        fatjets.sort(key=lambda x: x.njs, reverse = True)
        # 2/ lowest mass is more higgs like 
        if len(fatjets)>1 and fatjets[0].njs==fatjets[1].njs:
          fatjets.sort(key=lambda x: x.subjetsSoftDrop[0].p4().M(), reverse = True)

        if len(leptons) > 0 and len(fatjets) > 1:
            
            self.tree.fill('weight' , event.weight )
            fillLepton(self.tree, 'l',leptons[0] )
            fillMet(self.tree, 'met', event.met)
            self.tree.fill('nbjets', len(bjets))

            # compute and fill TRF
            self.tree.fill('weight_0tagex', getNbTagEx(0,jet_forTRF,-1))
            self.tree.fill('weight_1tagex', getNbTagEx(1,jet_forTRF,-1))
            self.tree.fill('weight_2tagex', getNbTagEx(2,jet_forTRF,-1))
            self.tree.fill('weight_3tagex', getNbTagEx(3,jet_forTRF,-1))
            self.tree.fill('weight_4tagex', getNbTagEx(4,jet_forTRF,-1))

            '''higgsjet = fatjets[1]
            if higgsjet.nbs > 1:
                print higgsjet.p4_bs.M(), higgsjet.subjetsSoftDrop[0].p4().M()'''
            
            for flavour in ['higgs', 'top']:
                
                if flavour == 'higgs':
                    jet = fatjets[1]
                else:
                    jet = fatjets[0]

                fillParticle(self.tree, '{}jet'.format(flavour), jet)
                fillParticle(self.tree, 'softDropped_{}jet'.format(flavour), jet.subjetsSoftDrop[0])

                self.tree.fill('{}jet_tau1'.format(flavour) , jet.tau1 )
                self.tree.fill('{}jet_tau2'.format(flavour) , jet.tau2 )
                self.tree.fill('{}jet_tau3'.format(flavour) , jet.tau3 )
                self.tree.fill('{}jet_tau31'.format(flavour) , jet.tau31 )
                self.tree.fill('{}jet_tau32'.format(flavour) , jet.tau32 )
                self.tree.fill('{}jet_tau21'.format(flavour) , jet.tau21 )

                #print 'filling: ',jet.flow[0], jet.flow[1], jet.flow[2], jet.flow[3], jet.flow[4]

                self.tree.fill('{}jet_flow15'.format(flavour), jet.flow[0])
                self.tree.fill('{}jet_flow25'.format(flavour), jet.flow[1])
                self.tree.fill('{}jet_flow35'.format(flavour), jet.flow[2])
                self.tree.fill('{}jet_flow45'.format(flavour), jet.flow[3])
                self.tree.fill('{}jet_flow55'.format(flavour), jet.flow[4])

                self.tree.fill('{}jet_njs'.format(flavour), jet.njs)
                self.tree.fill('{}jet_nbs'.format(flavour), jet.nbs)
                self.tree.fill('{}jet_ncs'.format(flavour), jet.ncs)
                self.tree.fill('{}jet_nls'.format(flavour), jet.nls)
                self.tree.fill('{}jet_mjs'.format(flavour), jet.p4_js.M())
                self.tree.fill('{}jet_mbs'.format(flavour), jet.p4_bs.M())
                ##self.tree.fill('{}jet_bdt_th'.format(flavour), jet.bdt_th)

            #Hjet = fatjets[1]
            #tjet = fatjets[0]
            #isHiggsOK = False
            # 1/ 18/31 wrong
            #if Hjet.nbs > tjet.nbs : isHiggsOK=True
            #elif Hjet.nbs == tjet.nbs and Hjet.subjetsSoftDrop[0].p4().M() < tjet.subjetsSoftDrop[0].p4().M() : isHiggsOK=True
            # 2/ 18/31 wrong
            #if Hjet.nbs > 1 : # 3/ 14/15 wrong
            #  if Hjet.bdt_th > tjet.bdt_th : isHiggsOK=True
            #  if isHiggsOK==True : print "good match Higgs"
            #  else :               print "wrong match Higgs"
            self.tree.tree.Fill()
        

        
    def write(self, setup):
        self.rootfile.Write()
        self.rootfile.Close()

