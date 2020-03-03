import ROOT


class runDataFrameFinal():

    #__________________________________________________________
    def __init__(self, basedir, processes, cuts, variables):
        self.basedir   = basedir
        self.processes = processes
        self.variables = variables
        self.cuts      = cuts

    #__________________________________________________________
    def run(self,ncpu=5):
        print "EnableImplicitMT: {}".format(ncpu)
        ROOT.ROOT.EnableImplicitMT(ncpu)
        print "Load cxx analyzers ... ",
        ROOT.gSystem.Load("libdatamodel")
        ROOT.gSystem.Load("libFCCAnalyses")
        ROOT.gErrorIgnoreLevel = ROOT.kFatal
        count=0
        for cut in self.cuts:
            print 'running over cut : ',cut

            for pr in self.processes:
                print '   running over process : ',pr
                fin    = self.basedir+pr+'.root' #input file
                fout   = self.basedir+pr+'_final_sel{}.root'.format(count) #output file for tree
                fhisto = self.basedir+pr+'_final_selhisto{}.root'.format(count) #output file for histograms
                RDF = ROOT.ROOT.RDataFrame
                df  = RDF("events",fin )
                df_cut = df.Filter(cut)
                snapshot_tdf = df_cut.Snapshot("events", fout)

                tftest=ROOT.TFile.Open(fout).Get()
                tttest=tftest.Get("events")
                print tttest
                tf    = ROOT.TFile.Open(fhisto,'RECREATE')
                for v in self.variables:
                    model = ROOT.RDF.TH1DModel(v, ";{};".format(self.variables[v]["title"]), self.variables[v]["bin"], self.variables[v]["xmin"],  self.variables[v]["xmax"])
                    h     = snapshot_tdf.Histo1D(model,self.variables[v]["name"])
                    h.Write()
                tf.Close()
        count+=1

