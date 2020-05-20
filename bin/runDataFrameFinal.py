import ROOT
import json
import sys

class runDataFrameFinal():

    #__________________________________________________________
    def __init__(self, baseDir, procDict, processes, cuts, variables, treename="events"):
        self.baseDir   = baseDir
        self.processes = processes
        self.variables = variables
        self.cuts      = cuts
        self.treename  = treename

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
                print 'file do not contains events, selection was too tight, will skip: ',f
                return False
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
            return False
        except ValueError:
            print "Could read the file"
            return False
        except:
            print "Unexpected error:", sys.exc_info()[0]
            print 'file ===%s=== must be deleted'%f
            return False
        return True
    #__________________________________________________________
    def run(self,ncpu=5):
        print "EnableImplicitMT: {}".format(ncpu)
        ROOT.ROOT.EnableImplicitMT(ncpu)
        print "Load cxx analyzers ... ",
        ROOT.gSystem.Load("libdatamodel")
        ROOT.gSystem.Load("libFCCAnalyses")
        ROOT.gErrorIgnoreLevel = ROOT.kFatal
        nevents_real=0
        import time
        start_time = time.time()

        processEvents={}
        for pr in self.processes:
            fin    = self.baseDir+pr+'.root' #input file
            tfin = ROOT.TFile.Open(fin)
            tfin.cd()
            events = tfin.eventsProcessed.GetVal()
            processEvents[pr]=events
            tfin.Close()

        for cut in self.cuts:
            print 'running over cut : ',self.cuts[cut]
            for pr in self.processes:
                print '   running over process : ',pr
                fin    = self.baseDir+pr+'.root' #input file
                fout   = self.baseDir+pr+'_'+cut+'.root' #output file for tree
                fhisto = self.baseDir+pr+'_'+cut+'_histo.root' #output file for histograms

                RDF = ROOT.ROOT.RDataFrame
                df  = RDF(self.treename,fin )
                df_cut = df.Filter(self.cuts[cut])
                snapshot_tdf = df_cut.Snapshot(self.treename, fout)

                validfile = self.testfile(fout)
                if not validfile: continue

                nevents_real+=df_cut.Count().GetValue()

                tf    = ROOT.TFile.Open(fhisto,'RECREATE')
                for v in self.variables:
                    model = ROOT.RDF.TH1DModel(v, ";{};".format(self.variables[v]["title"]), self.variables[v]["bin"], self.variables[v]["xmin"],  self.variables[v]["xmax"])
                    h     = snapshot_tdf.Histo1D(model,self.variables[v]["name"])
                    h.Scale(1.*self.procDict[pr]["crossSection"]*self.procDict[pr]["kfactor"]*self.procDict[pr]["matchingEfficiency"]/processEvents[pr])
                    h.Write()
                tf.Close()

        elapsed_time = time.time() - start_time
        print  '==============================SUMMARY=============================='
        print  'Elapsed time (H:M:S)     :  ',time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
        print  'Events Processed/Second  :  ',int(nevents_real/elapsed_time)
        print  'Total Events Processed   :  ',nevents_real
        print  '==================================================================='
