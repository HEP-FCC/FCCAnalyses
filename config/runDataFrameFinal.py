#!/usr/bin/env python
import ROOT
import json
import sys
import os

class runDataFrameFinal():

    #__________________________________________________________
    def __init__(self, baseDir, procDict, processes, cuts, variables, intLumi=1., treename="events", defines={}):
        self.baseDir   = baseDir
        self.processes = processes
        self.variables = variables
        self.cuts      = cuts
        self.intLumi   = intLumi
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
    def run(self,ncpu=5,doTree=False,doScale=True,saveTabular=False):
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
        eventsTTree={}
        processList={}
        saveTab=[]
        efficiencyList=[]
        
        for pr in self.processes:
            processEvents[pr]=0
            eventsTTree[pr]=0

            fileListRoot = ROOT.vector('string')()    
            fin    = self.baseDir+pr+'.root' #input file
            if not os.path.isfile(fin):
                print ('file ',fin,'  does not exist. Try if it is a directory as it was processed with batch')
            else:
                print ('open file ',fin)
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
                tt=tfin.Get("events")
                eventsTTree[pr]+=tt.GetEntries()

                tfin.Close()
                fileListRoot.push_back(fin)

            if os.path.isdir(self.baseDir+pr):
                print ('is dir found')
                import glob
                flist=glob.glob(self.baseDir+pr+"/flat_chunk_*.root")
                for f in flist:
                    tfin = ROOT.TFile.Open(f)
                    print (f,'    ===    ',tfin, '  ',type(tfin))
                    tfin.cd()
                    
                    found=False
                    for key in tfin.GetListOfKeys():
                        if 'eventsProcessed' == key.GetName():
                            events = tfin.eventsProcessed.GetVal()
                            processEvents[pr]+=events
                            found=True
                    if not found:
                        processEvents[pr]=1
                        
                    tt=tfin.Get("events")
                    eventsTTree[pr]+=tt.GetEntries()
                    tfin.Close()
                    fileListRoot.push_back(f)
            processList[pr]=fileListRoot

        print('processed events ',processEvents)
        print('events in ttree  ',eventsTTree)



        length_cuts_names = max([len(cut) for cut in self.cuts])

        if saveTabular:
            f = open("outputTabular.txt","w")
            cutNames = [cut for cut in self.cuts]
            cutNames.insert(0,' ')
            saveTab.append(cutNames)
            efficiencyList.append(cutNames)

        for pr in self.processes:
            print ('\n   running over process : ',pr)
            RDF = ROOT.ROOT.RDataFrame
            df  = RDF(self.treename, processList[pr] )
            if len(self.defines)>0:
                print ('     Running extra Define')
                for define in self.defines:
                    df=df.Define(define, self.defines[define])

            fout_list = []
            histos_list = []
            tdf_list = []
            count_list = []
            cuts_list = []
            cuts_list.append(pr)
            eff_list=[]
            eff_list.append(pr)

            # Define all histos, snapshots, etc...
            print ('     Defining snapshots and histograms')
            for cut in self.cuts:
                fout   = self.baseDir+pr+'_'+cut+'.root' #output file for tree
                fout_list.append(fout)
                
                df_cut = df.Filter(self.cuts[cut])
                count_list.append(df_cut.Count())

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
            print ('     Evaluating...')
            all_events = df.Count().GetValue()
            print ('     Done')

            nevents_real += all_events

            if doScale:
                all_events = all_events*1.*self.procDict[pr]["crossSection"]*self.procDict[pr]["kfactor"]*self.procDict[pr]["matchingEfficiency"]*self.intLumi/eventsTTree[pr]
                print('  Printing scaled number of events!!! ')

            print ('     Cutflow')
            print ('       {cutname:{width}} : {nevents:.2e}'.format(cutname='All events', width=16+length_cuts_names, nevents=all_events))

            if saveTabular:
                uncertainty = ROOT.Math.sqrt(nevents_real)*self.procDict[pr]["crossSection"]*self.procDict[pr]["kfactor"]*self.procDict[pr]["matchingEfficiency"]*self.intLumi/eventsTTree[pr]
                # cuts_list.append('{nevents:.2e} $\\pm$ {uncertainty:.2e}'.format(nevents=all_events,uncertainty=uncertainty)) # scientific notation - recomended for backgrounds
                cuts_list.append('{nevents:.3f} $\\pm$ {uncertainty:.3f}'.format(nevents=all_events,uncertainty=uncertainty)) # float notation - recomended for signals with few events
                eff_list.append(100)

            for i, cut in enumerate(self.cuts):
                neventsThisCut = count_list[i].GetValue()
                neventsThisCut_raw = neventsThisCut
                if doScale:
                    neventsThisCut = neventsThisCut*1.*self.procDict[pr]["crossSection"]*self.procDict[pr]["kfactor"]*self.procDict[pr]["matchingEfficiency"]*self.intLumi/eventsTTree[pr]
                print ('       After selection {cutname:{width}} : {nevents:.2e}'.format(cutname=cut, width=length_cuts_names, nevents=neventsThisCut))

                # Saving the number of events, uncertainty and efficiency for the output-file
                if saveTabular and cut != 'selNone':
                    uncertainty = ROOT.Math.sqrt(neventsThisCut_raw)*self.procDict[pr]["crossSection"]*self.procDict[pr]["kfactor"]*self.procDict[pr]["matchingEfficiency"]*self.intLumi/eventsTTree[pr]
                    if neventsThisCut != 0:
                        # cuts_list.append('{nevents:.2e} $\\pm$ {uncertainty:.2e}'.format(nevents=neventsThisCut,uncertainty=uncertainty)) # scientific notation - recomended for backgrounds
                        cuts_list.append('{nevents:.3f} $\\pm$ {uncertainty:.3f}'.format(nevents=neventsThisCut,uncertainty=uncertainty)) # # float notation - recomended for signals with few events
                        prevNevents = cuts_list[-2].split()
                        eff_list.append('{eff:.2g}'.format(eff=100*neventsThisCut/float(prevNevents[0])))
                    # if number of events is zero, the previous uncertainty is saved instead:
                    elif '$\\pm$' in cuts_list[-1]:
                        cut = (cuts_list[-1]).split()
                        cuts_list.append('$\\leq$ {uncertainty}'.format(uncertainty=cut[2]))
                        eff_list.append('-')
                    else:
                        cuts_list.append(cuts_list[-1])
                        eff_list.append('-')


            # And save everything
            print ('     Saving outputs')
            for i, cut in enumerate(self.cuts):
                fhisto = self.baseDir+pr+'_'+cut+'_histo.root' #output file for histograms
                tf    = ROOT.TFile.Open(fhisto,'RECREATE')
                for h in histos_list[i]:
                    if doScale:
                        try :
                            h.Scale(1.*self.procDict[pr]["crossSection"]*self.procDict[pr]["kfactor"]*self.procDict[pr]["matchingEfficiency"]*self.intLumi/eventsTTree[pr])
                        except KeyError:
                            print ('no value found for something')
                            h.Scale(1./h.Integral(0,-1))
                    h.Write()
                tf.Close()

                if doTree:
                    # test that the snapshot worked well
                    validfile = self.testfile(fout_list[i])
                    if not validfile: continue

            if saveTabular and cut != 'selNone':
                saveTab.append(cuts_list)
                efficiencyList.append(eff_list)
        if saveTabular:
            # Printing the number of events in format of a LaTeX table
            print('\\begin{table}[H] \n    \\centering \n    \\resizebox{\\textwidth}{!}{ \n    \\begin{tabular}{|l||',end='',file=f)
            print('c|' * (len(cuts_list)-1),end='',file=f)
            print('} \hline',file=f)
            for i, row in enumerate(saveTab):
                print('        ', end='', file=f)
                print(*row, sep = ' & ', end='', file=f)
                print(' \\\\ ', file=f)
                if (i == 0):
                    print('        \\hline',file=f)
            print('        \\hline \n    \\end{tabular}} \n    \\caption{Caption} \n    \\label{tab:my_label} \n\\end{table}', file=f)
            
            # Efficiency:
            print('\n\nEfficiency: ', file=f)
            print('\\begin{table}[H] \n    \\centering \n    \\resizebox{\\textwidth}{!}{ \n    \\begin{tabular}{|l||',end='',file=f)
            print('c|' * (len(cuts_list)-1),end='',file=f)
            print('} \hline',file=f)
            for i in range(len(eff_list)):
                print('        ', end='', file=f)
                v = [row[i] for row in efficiencyList]
                print(*v, sep = ' & ', end='', file=f)
                print(' \\\\ ', file=f)
                if (i == 0):
                    print('        \\hline',file=f)
            print('        \\hline \n    \\end{tabular}} \n    \\caption{Caption} \n    \\label{tab:my_label} \n\\end{table}', file=f)
            f.close()

        elapsed_time = time.time() - start_time
        print  ('==============================SUMMARY==============================')
        print  ('Elapsed time (H:M:S)     :  ',time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
        print  ('Events Processed/Second  :  ',int(nevents_real/elapsed_time))
        print  ('Total Events Processed   :  ',nevents_real)
        print  ('===================================================================')
