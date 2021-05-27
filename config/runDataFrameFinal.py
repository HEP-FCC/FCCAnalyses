#!/usr/bin/env python
import ROOT
import json
import sys
import os

class runDataFrameFinal():

    #__________________________________________________________
    def __init__(self, baseDir, procDict, processes, cuts, variables, treename="events", defines={}):
        self.baseDir   = baseDir
        self.processes = processes
        self.variables = variables
        self.cuts      = cuts
        self.treename  = treename
        self.defines   = defines
        self.procDict  = None
        
        if 'https://fcc-physics-events.web.cern.ch' in procDict:
            print ('getting info from the web')
            import urllib.request
            req = urllib.request.urlopen(procDict).read()
            self.procDict = json.loads(req.decode('utf-8'))
        elif '.json' in procDict:
            with open(procDict, 'r') as f:
                self.procDict=json.load(f)
        else:
            self.procDict=procDict
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
                print ('file does not contains events, selection was too tight, will skip: ',f)
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
    def run(self,ncpu=5,doTree=False):
        print ("EnableImplicitMT: {}".format(ncpu))
        ROOT.ROOT.EnableImplicitMT(ncpu)
        print ("Load cxx analyzers ... ")
        ROOT.gSystem.Load("libdatamodel")
        ROOT.gSystem.Load("libFCCAnalyses")
        ROOT.gErrorIgnoreLevel = ROOT.kFatal
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
            if 'Bc2TauNuTAUHADNU' in pr:
                processEvents[pr]=self.procDict[pr]["numberOfEvents"]
            tfin.Close()

        for pr in self.processes:
            print ('   running over process : ',pr)
            fin    = self.baseDir+pr+'.root' #input file

            RDF = ROOT.ROOT.RDataFrame
            df  = RDF(self.treename,fin )
            if len(self.defines)>0:
                print ('Running extra Define')
                for define in self.defines:
                    df=df.Define(define, self.defines[define])

            fout_list = []
            histos_list = []
            tdf_list = []

            # Define all histos, snapshots, etc...
            print ('Defining snapshots and histograms')
            for cut in self.cuts:
                fout   = self.baseDir+pr+'_'+cut+'.root' #output file for tree
                fout_list.append(fout)
                
                df_cut = df.Filter(self.cuts[cut])

                histos = []
                for v in self.variables:
                    model = ROOT.RDF.TH1DModel(v, ";{};".format(self.variables[v]["title"]), self.variables[v]["bin"], self.variables[v]["xmin"],  self.variables[v]["xmax"])
                    
                    histos.append(df_cut.Histo1D(model,self.variables[v]["name"]))
                    #h     = snapshot_tdf.Histo1D(model,self.variables[v]["name"])
                histos_list.append(histos)

                if doTree:
                    opts = ROOT.RDF.RSnapshotOptions()
                    opts.fLazy = True
                    snapshot_tdf = df_cut.Snapshot(self.treename, fout, "", opts)
                    # Needed to avoid python garbage collector messing around with the snapshot
                    tdf_list.append(snapshot_tdf)

            # Now perform the loop and evaluate everything at once.
            print ('Evaluating...')
            nevents_real+=df.Count().GetValue()
            print ('Done...')

            # And save everything
            print ('Saving outputs')
            for i, cut in enumerate(self.cuts):
                fhisto = self.baseDir+pr+'_'+cut+'_histo.root' #output file for histograms
                tf    = ROOT.TFile.Open(fhisto,'RECREATE')
                for h in histos_list[i]:
                    try :
                        h.Scale(1.*self.procDict[pr]["crossSection"]*self.procDict[pr]["kfactor"]*self.procDict[pr]["matchingEfficiency"]/processEvents[pr])
                    except KeyError:
                        print ('no value found for something')
                        h.Scale(1./h.Integral(0,-1))
                    h.Write()
                tf.Close()

                if doTree:
                    # test that the snapshot worked well
                    validfile = self.testfile(fout_list[i])
                    if not validfile: continue


        elapsed_time = time.time() - start_time
        print  ('==============================SUMMARY==============================')
        print  ('Elapsed time (H:M:S)     :  ',time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
        print  ('Events Processed/Second  :  ',int(nevents_real/elapsed_time))
        print  ('Total Events Processed   :  ',nevents_real)
        print  ('===================================================================')
