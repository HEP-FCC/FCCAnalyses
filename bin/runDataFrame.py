import yaml
import ROOT 
import sys
from array import array

class runDataFrame():

    #__________________________________________________________
    def __init__(self, basedir, processes):
        self.basedir      = basedir
        self.process_list = processes


    #__________________________________________________________
    def run(self,ncpu=10, fraction=1):

        for pr in self.process_list:
            doc = None
            outfile=self.basedir+pr+'/merge.yaml'
            with open(outfile) as ftmp:
                try:
                    doc = yaml.load(ftmp, Loader=yaml.FullLoader)
                except yaml.YAMLError as exc:
                    print(exc)
                except IOError as exc:
                    print "I/O error({0}): {1}".format(exc.errno, exc.strerror)
                    print "outfile ",outfile
                finally:
                    print 'file succesfully opened'


            filelist  = [doc['merge']['outdir']+f[0] for f in doc['merge']['outfiles']]
            eventlist = [f[1] for f in doc['merge']['outfiles']]
        
            if fraction<1:
                tmplist=[]
                nevents_target=int(doc['merge']['nevents']*fraction)
                nevents_real=0
                print 'nevents_target  ',nevents_target
                print 'nevents_target  ',doc['merge']['nevents']*fraction

                for ev in range(len(eventlist)):
                    if nevents_real>nevents_target:break
                    nevents_real+=eventlist[ev]
                    tmplist.append(filelist[ev])

            filelist=tmplist
            if len(filelist)==0:
                print "fraction too small, no files left: exit"
                sys.exit(3)
        
            print "Create list object from ", 
            fileListRoot = ROOT.vector('string')()
            for fileName in filelist:
                fileListRoot.push_back(fileName)
                print fileName, " ",
                print " ..."


            print 'About to run process {} with {} events'.format(pr,nevents_real)
            import analysis as ana
            import time
            start_time = time.time()
            myana=ana.analysis(fileListRoot,pr+'.root',ncpu)
            myana.run()
            elapsed_time = time.time() - start_time
            print  'elapsed time (H:M:S) ',time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
            print  'events per second: ',nevents_real/elapsed_time

        outf = ROOT.TFile( pr+'.root', 'update' )
        meta = ROOT.TTree( 'metadata', 'metadata informations' )
        n = array( 'i', [ 0 ] )
        meta.Branch( 'eventsProcessed', n, 'eventsProcessed/I' )
        n[0]=nevents_real
        meta.Fill()
        outf.Write()
        outf.Close()
