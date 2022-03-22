
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
    def run(self,ncpu=10, fraction=1, outDir=''):
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
            import analysis as ana
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
