import ROOT
import json
import sys
import os
import uproot4 as uproot
import awkward1 as ak
import numpy as np
#import matplotlib.pyplot as plt
#from fcc_python_tools.locations import loc
import kinematics
from particle import literals as lp
#from fcc_python_tools import plotting
#import tensorflow as tf
#import zfit
import random
#import uproot4
#import 

class runCombinatorics():

    #__________________________________________________________
    def __init__(self, baseDir, procDict, processes, cuts, variables, treename="events", defines={}):
        self.baseDir   = baseDir
        self.processes = processes
        self.variables = variables
        self.cuts      = cuts
        self.treename  = treename
        self.defines   = defines
        self.procDict  = None
        with open(procDict, 'r') as f:
            self.procDict=json.load(f)

        if self.procDict==None:
            print ('no procDict found ==={}=== exit'.format(self.procDict))
            sys.exit(3)
    #__________________________________________________________
    def testfile(self,f):
        tf=ROOT.TFile.Open(f)
        tt=None
        try :
            tt=tf.Get(self.treename)
            if tt==None:
                print ('file do not contains events, selection was too tight, will skip: ',f)
                return False
        except IOError as e:
            print ("I/O error({0}): {1}".format(e.errno, e.strerror))
            return False
        except ValueError:
            print ("Could read the file")
            return False
        except:
            print ("Unexpected error:", sys.exc_info()[0])
            print ('file ===%s=== must be deleted'%f)
            return False
        return True
    #__________________________________________________________
    def run(self, decay, ncpu=5):

        nevents_real=0
        import time
        start_time = time.time()

        processEvents={}
        for pr in self.processes:
            fin    = self.baseDir+pr+'.root' #input file
            if not os.path.isfile(fin):
                print ('file ',fin,'  does not exist. exit')
                exit(3)
            tfin = ROOT.TFile.Open(fin)
            tfin.cd()
            found=False
            for key in tfin.GetListOfKeys():
                if 'eventsProcessed' == key.GetName():
                    events = tfin.eventsProcessed.GetVal()
                    processEvents[pr]=events
                    found=True
            if not found:
                processEvents[pr]=1
            tfin.Close()

        for pr in self.processes:
            print ('   running over process : ',pr)
            fin    = self.baseDir+pr+'.root' #input file
            fout   = self.baseDir+pr+'.root' #output file for tree
            fhisto = self.baseDir+pr+'_histo.root' #output file for histograms


            file = uproot.open(fin)
            tree = file['events']

            #Number of events to keep and analyse
            n_events = 1000

            #Container for the reco particles
            p_c = 'RP'

            events = tree.arrays(library="ak", how="zip",filter_name=f"{p_c}*")[:n_events]
            print ('events loaded ', events)
            p = events[p_c]
            
            
            print ('fin ',fin)
            p_c = 'RP'
            #Number of events to keep and analyse
            n_events = 10000
            file = uproot.open(fin)
            tree = file[self.treename]
            print ('here-1.2')
            events = tree.arrays(library="ak", how="zip", filter_name=f"{p_c}*")[:n_events]
            print ('here0')

 

            #Container for the reco particles
            p = events[p_c][:n_events]
            print ('here1')

            p["p"] = kinematics_flat.calc_p(p)
            p_cut = p["p"] > 1.
            p = p[p_cut]
            print ('here2')

            pi_cut = abs(p["mass"] - lp.pi_plus.mass/1000.) < 1e-4
            pi = p[pi_cut]
            print ('here3')

            k_cut = abs(p["mass"] - lp.K_plus.mass/1000.) < 1e-4
            k = p[k_cut]
            print ('here4')

            D = ak.cartesian({"k": k, "pi": pi})
            D_cut = np.sign(D["k","charge"]) != np.sign(D["pi","charge"])
            D = D[D_cut]
            print ('here5')

            PDG_K_m = lp.K_plus.mass/1000.
            PDG_pi_m = lp.pi_plus.mass/1000.
            D["mass"] = kinematics_flat.mass([D["k"], D["pi"]], [PDG_K_m, PDG_pi_m])
            print ('here6')

            PDG_D_m = lp.D_0.mass/1000.
            D_window = 0.05
            D_cut = abs(D["mass"] - PDG_D_m) < D_window
            D = D[D_cut]
            print ('here7')

            B = ak.cartesian({"D_k": D["k"], "D_pi": D["pi"], "pi": pi})
            B_cut = np.sign(B["D_k","charge"]) == np.sign(B["pi","charge"])
            B = B[B_cut]
            B["mass"] = kinematics_flat.mass([B["D_k"], B["D_pi"], B["pi"]], [PDG_K_m, PDG_pi_m, PDG_pi_m])
            print ('here8')


            data_np = ak.to_numpy(ak.flatten(B["mass"]))
            print (data_np)


            validfile = self.testfile(fout)
            if not validfile: continue

            nevents_real+=df_cut.Count().GetValue()

            tf    = ROOT.TFile.Open(fhisto,'RECREATE')
            for v in self.variables:
                model = ROOT.RDF.TH1DModel(v, ";{};".format(self.variables[v]["title"]), self.variables[v]["bin"], self.variables[v]["xmin"],  self.variables[v]["xmax"])
                h     = snapshot_tdf.Histo1D(model,self.variables[v]["name"])
                try :
                    h.Scale(1.*self.procDict[pr]["crossSection"]*self.procDict[pr]["kfactor"]*self.procDict[pr]["matchingEfficiency"]/processEvents[pr])
                except KeyError:
                    h.Scale(1./h.Integral(0,-1))
                h.Write()
            tf.Close()

        elapsed_time = time.time() - start_time
        print  ('==============================SUMMARY==============================')
        print  ('Elapsed time (H:M:S)     :  ',time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
        print  ('Events Processed/Second  :  ',int(nevents_real/elapsed_time))
        print  ('Total Events Processed   :  ',nevents_real)
        print  ('===================================================================')
