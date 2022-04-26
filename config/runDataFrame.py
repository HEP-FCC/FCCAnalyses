
#root://eospublic.cern.ch//
#!/usr/bin/env python
import yaml
import ROOT
import sys
from array import array
import os.path

class runDataFrame():

    #__________________________________________________________
    def __init__(self, basedir, processes, outlist=[]):
        self.basedir      = basedir
        self.process_list = processes
        self.output_list  = outlist

    #__________________________________________________________
    def run(self,inputana, ncpu=10, fraction=1, outDir="myLocalOutputs", chunks=-1, comp="group_u_FCC.local_gen"):

        if chunks>0:
            self.runBatch(inputana, ncpu, fraction, outDir, chunks, comp = "group_u_FCC.local_gen")
        else:
            self.runLocal(inputana, ncpu, fraction, outDir)

    #__________________________________________________________
    def runLocal(self,inputana, ncpu, fraction, outDir):
        print ("EnableImplicitMT: {}".format(ncpu))

        if not os.path.exists(outDir) and outDir!='':
            os.system("mkdir -p {}".format(outDir))
        if outDir!='' and outDir[-1]!='/':
            outDir+='/'
        counter=0
        for pr in self.process_list:
            outName=pr
            if len(self.output_list)==len(self.process_list):
                outName=self.output_list[counter]

            doc = None
            yamlfile=self.basedir+pr+'/merge.yaml'

            if 'https://fcc-physics-events.web.cern.ch' in self.basedir:
                print ('getting info from the web')
                import urllib.request
                outname=yamlfile.split('/')[-1]
                outname=outname.replace('.yaml','_{}.yaml'.format(pr))
                urllib.request.urlretrieve(yamlfile, outname)
                yamlfile=outname

            with open(yamlfile) as ftmp:
                try:
                    doc = yaml.load(ftmp, Loader=yaml.FullLoader)
                except yaml.YAMLError as exc:
                    print(exc)
                except IOError as exc:
                    print ("I/O error({0}): {1}".format(exc.errno, exc.strerror))
                    print ("outfile ",outfile)
                finally:
                    print ('file succesfully opened')


            filelist  = [doc['merge']['outdir']+f[0] for f in doc['merge']['outfiles']]
            eventlist = [f[1] for f in doc['merge']['outfiles']]

            if fraction<1:
                tmplist=[]
                nevents_target=int(doc['merge']['nevents']*fraction)
                nevents_real=0

                for ev in range(len(eventlist)):
                    if nevents_real>nevents_target:break
                    nevents_real+=eventlist[ev]
                    tmplist.append(filelist[ev])
                filelist=tmplist

            else:
                nevents_real=int(doc['merge']['nevents'])

            if len(filelist)==0:
                print ("fraction too small, no files left: exit")
                sys.exit(3)

            noutfiles=1
            if isinstance(self.process_list, dict):
                noutfiles=self.process_list[pr]
                if noutfiles > len(filelist) : noutfiles = len(filelist)
                if noutfiles>1 and not os.path.exists(outDir+outName):
                    os.system("mkdir -p {}".format(outDir+outName))
            nfilesperjob=int(len(filelist)/noutfiles)
            #if len(filelist)/noutfiles>nfilesperjob:nfilesperjob+=1
            print ('About to run process {} with {} events in {} consecutive local jobs with {} files per job'.format(pr,nevents_real,noutfiles,nfilesperjob))
            #import analysis as ana
            ana = __import__(os.path.abspath(inputana).replace('.py', '').replace('/','.'))

            import time
            outNameFull=''
            for nout in range(noutfiles):
                filecount=0
                print ("For job {}, create list object from ".format(nout),)
                fileListRoot = ROOT.vector('string')()
                if noutfiles>1:
                    outNameFull='{}/flat_chunk_{}.root'.format(outName,nout)
                else: outNameFull=outName+'.root'

                for fileName in filelist:
                    if (filecount>=nout*nfilesperjob and filecount<(nout+1)*nfilesperjob) or (filecount>=nout*nfilesperjob and nout==noutfiles-1):
                        fileListRoot.push_back(fileName)
                        print (fileName, " ",)
                        print (" ...")
                    filecount+=1

                start_time = time.time()
                myana=ana.analysis(fileListRoot,outDir+outNameFull,ncpu)
                myana.run()
                elapsed_time = time.time() - start_time
                print  ('==============================SUMMARY==============================')
                print  ('Elapsed time (H:M:S)     :  ',time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
                print  ('Events Processed/Second  :  ',int(nevents_real/elapsed_time))
                print  ('Total Events Processed   :  ',int(nevents_real))
                print  ('===================================================================')

                outf = ROOT.TFile( outDir+outNameFull, 'update' )
                meta = ROOT.TTree( 'metadata', 'metadata informations' )
                n = array( 'i', [ 0 ] )
                meta.Branch( 'eventsProcessed', n, 'eventsProcessed/I' )
                n[0]=nevents_real
                meta.Fill()
                p = ROOT.TParameter(int)( "eventsProcessed", n[0])
                p.Write()
                outf.Write()
                outf.Close()
                counter+=1

    #__________________________________________________________
    def runBatch(self, inputana, ncpu, fraction, outDir, chunks, comp):
        print ("EnableImplicitMT: {}".format(ncpu))

        if not os.path.exists(outDir) and outDir!='':
            os.system("mkdir -p {}".format(outDir))
        if outDir!='' and outDir[-1]!='/':
            outDir+='/'
        counter=0
        for pr in self.process_list:
            outName=pr
            if len(self.output_list)==len(self.process_list):
                outName=self.output_list[counter]

            doc = None
            yamlfile=self.basedir+pr+'/merge.yaml'

            if 'https://fcc-physics-events.web.cern.ch' in self.basedir:
                print ('getting info from the web')
                import urllib.request
                outname=yamlfile.split('/')[-1]
                outname=outname.replace('.yaml','_{}.yaml'.format(pr))
                urllib.request.urlretrieve(yamlfile, outname)
                yamlfile=outname

            with open(yamlfile) as ftmp:
                try:
                    doc = yaml.load(ftmp, Loader=yaml.FullLoader)
                except yaml.YAMLError as exc:
                    print(exc)
                except IOError as exc:
                    print ("I/O error({0}): {1}".format(exc.errno, exc.strerror))
                    print ("outfile ",outfile)
                finally:
                    print ('file succesfully opened')


            filelist  = [doc['merge']['outdir']+f[0] for f in doc['merge']['outfiles']]
            eventlist = [f[1] for f in doc['merge']['outfiles']]

            if fraction<1:
                tmplist=[]
                nevents_target=int(doc['merge']['nevents']*fraction)
                nevents_real=0

                for ev in range(len(eventlist)):
                    if nevents_real>nevents_target:break
                    nevents_real+=eventlist[ev]
                    tmplist.append(filelist[ev])
                filelist=tmplist

            else:
                nevents_real=int(doc['merge']['nevents'])

            if len(filelist)==0:
                print ("fraction too small, no files left: exit")
                sys.exit(3)


            chunkList=[]
            eventList=[]
            #nFiles=int(len(filelist)/chunks)+1
            nFiles=chunks
            counterFiles=0
            counterEvents=0
            counterFilesTot=0
            counterChunks=0
            print ('Will chunk ',len(filelist),' files in ',int(nevents_real/nFiles),' jobs of ',nFiles,' n files each')

            print ("Create list object for chunk ",counterChunks,"  ",)
            fileListRoot = ROOT.vector('string')()
            for fileName in filelist:
                fileListRoot.push_back(fileName)
                print ("    ",fileName, " ",)
                print ("    ...")
                counterFiles+=1
                counterEvents+=eventlist[counterFilesTot]
                counterFilesTot+=1
                if counterFiles==nFiles or counterFilesTot==len(filelist):
                    fileListRoot_tmp = ROOT.vector('string')()
                    for itt in fileListRoot:
                        fileListRoot_tmp.push_back(itt)
                    chunkList.append(fileListRoot_tmp)
                    eventList.append(counterEvents)
                    print ("    ",counterEvents,"  events")
                    fileListRoot.clear()

                    counterChunks+=1
                    if counterFiles<len(filelist) and counterFilesTot!=len(filelist):print ("Create list object for chunk ",counterChunks,"  ",)
                    counterFiles=0
                    counterEvents=0

            print ('About to send {} with {} jobs for a total of {} events'.format(pr,chunks,nevents_real))

            Dir = os.getcwd()
            logdir=Dir+"/BatchOutputs/{}".format(pr)
            if not os.path.exists(logdir):
                os.system("mkdir -p {}".format(logdir))

            condor_file_str=''
            for ch in range(len(chunkList)):
                frunname = '{}/job{}_chunk{}.sh'.format(logdir,pr,ch)
                print(frunname)
                condor_file_str+=frunname+" "

                frun = None
                try:
                    frun = open(frunname, 'w')
                except IOError as e:
                    print ("I/O error({0}): {1}".format(e.errno, e.strerror))
                    time.sleep(10)
                    frun = open(frunname, 'w')

                subprocess.getstatusoutput('chmod 777 %s'%(frunname))
                frun.write('#!/bin/bash\n')
                frun.write('unset LD_LIBRARY_PATH\n')
                frun.write('unset PYTHONHOME\n')
                frun.write('unset PYTHONPATH\n')
                frun.write('source /cvmfs/sw.hsf.org/key4hep/setup.sh\n')
                frun.write('export PYTHONPATH=/afs/cern.ch/user/h/helsens/FCCsoft/HEP-FCC/FCCAnalyses:$PYTHONPATH\n')
                frun.write('export LD_LIBRARY_PATH=/afs/cern.ch/user/h/helsens/FCCsoft/HEP-FCC/FCCAnalyses/install/lib:$LD_LIBRARY_PATH\n')
                frun.write('export ROOT_INCLUDE_PATH=/afs/cern.ch/user/h/helsens/FCCsoft/HEP-FCC/FCCAnalyses/install/include/FCCAnalyses:$ROOT_INCLUDE_PATH\n')
                frun.write('export LD_LIBRARY_PATH=`python -m awkward.config --libdir`:$LD_LIBRARY_PATH\n')
                frun.write('export LD_LIBRARY_PATH=/afs/cern.ch/user/h/helsens/FCCsoft/HEP-FCC/FCCeePhysicsPerformance/case-studies/flavour/dataframe/install/lib:$LD_LIBRARY_PATH\n')
                frun.write('export ROOT_INCLUDE_PATH=/afs/cern.ch/user/h/helsens/FCCsoft/HEP-FCC/FCCeePhysicsPerformance/case-studies/flavour/dataframe/install/include/FCCAnalysesFlavour:$ROOT_INCLUDE_PATH\n')


                frun.write('mkdir job{}_chunk{}\n'.format(pr,ch))
                frun.write('cd job{}_chunk{}\n'.format(pr,ch))
                frun.write('export EOS_MGM_URL=\"root://eospublic.cern.ch\"\n')
                frun.write('python {} output.root '.format(inputana))
                for ff in range(chunkList[ch].size()): frun.write(' {}'.format(chunkList[ch].at(ff)))
                frun.write(' {}\n'.format(eventList[ch]))
                frun.write('mkdir -p {}/{}\n'.format(outDir,pr))
                frun.write('python /afs/cern.ch/work/h/helsens/public/FCCutils/eoscopy.py output.root {}/{}/flat_chunk_{}.root\n'.format(outDir,pr,ch))
                frun.write('cd ..\n')
                frun.write('rm -rf job{}_chunk{}\n'.format(pr, ch))
                frun.close()


            condor_file_str=condor_file_str.replace("//","/")
            frunname_condor = 'job_desc_{}.cfg'.format(pr)
            frunfull_condor = '%s/%s'%(logdir,frunname_condor)
            frun_condor = None
            try:
                frun_condor = open(frunfull_condor, 'w')
            except IOError as e:
                print ("I/O error({0}): {1}".format(e.errno, e.strerror))
                time.sleep(10)
                frun_condor = open(frunfull_condor, 'w')
            subprocess.getstatusoutput('chmod 777 %s'%frunfull_condor)
            #
            frun_condor.write('executable     = $(filename)\n')
            frun_condor.write('Log            = %s/condor_job.%s.$(ClusterId).$(ProcId).log\n'%(logdir,pr))
            frun_condor.write('Output         = %s/condor_job.%s.$(ClusterId).$(ProcId).out\n'%(logdir,pr))
            frun_condor.write('Error          = %s/condor_job.%s.$(ClusterId).$(ProcId).error\n'%(logdir,pr))
            frun_condor.write('getenv         = True\n')
            frun_condor.write('environment    = "LS_SUBCWD=%s"\n'%logdir) # not sure
            frun_condor.write('requirements   = ( (OpSysAndVer =?= "CentOS7") && (Machine =!= LastRemoteHost) && (TARGET.has_avx2 =?= True) )\n')
            frun_condor.write('on_exit_remove = (ExitBySignal == False) && (ExitCode == 0)\n')
            frun_condor.write('max_retries    = 3\n')
            frun_condor.write('+JobFlavour    = "workday"\n')
            frun_condor.write('+AccountingGroup = "{}"\n'.format(comp))
            frun_condor.write('RequestCpus = %s\n'%ncpu)
            frun_condor.write('queue filename matching files %s\n'%condor_file_str)
            frun_condor.close()

            cmdBatch="condor_submit %s"%frunfull_condor
            print (cmdBatch)
            job=self.SubmitToCondor(cmdBatch,10)

            counter+=1

#__________________________________________________________
    def getCommandOutput(self, command):
        p = subprocess.Popen(command, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE,universal_newlines=True)
        (stdout,stderr) = p.communicate()
        return {"stdout":stdout, "stderr":stderr, "returncode":p.returncode}

#__________________________________________________________
    def SubmitToCondor(self, cmd, nbtrials):
        submissionStatus=0
        cmd=cmd.replace('//','/') # -> dav : is it needed?
        for i in range(nbtrials):
            outputCMD = self.getCommandOutput(cmd)
            stderr=outputCMD["stderr"].split('\n')
            stdout=outputCMD["stdout"].split('\n') # -> dav : is it needed?

            if len(stderr)==1 and stderr[0]=='' :
                print ("------------GOOD SUB")
                submissionStatus=1
            else:
                print ("++++++++++++ERROR submitting, will retry")
                print ("Trial : "+str(i)+" / "+str(nbtrials))
                print ("stderr : ",len(stderr))
                print (stderr)
                time.sleep(10)

            if submissionStatus==1:
                return 1

            if i==nbtrials-1:
                print ("failed sumbmitting after: "+str(nbtrials)+" trials, will exit")
                return 0
