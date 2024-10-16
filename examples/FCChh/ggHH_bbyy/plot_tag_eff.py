from collections import namedtuple
import ROOT
import argparse
import os 
import numpy as np

ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptTitle(0)

def getHfromRDF(hist):
    h = None
    t = hist.GetValue()
    h = t.Clone()
    return h

def makePlots(dict_of_vars, sel_cutstring, input_filepath, out_dir_base, out_format = ".png", do_log_y=False):

   if not os.path.exists(out_dir_base):
      os.mkdir(out_dir_base)

   rdf = ROOT.RDataFrame("events", input_filepath)

   if sel_cutstring:
      rdf = rdf.Filter(sel_cutstring) #apply the selection

   if not rdf:
      print("Empty file for:", input_filepath, " Exiting.")
      return

   for plot_name, plot in dict_of_vars.items():
      print("Plotting:", plot_name)

      has_variable_binning = False
      if not isinstance(plot.nbins, int):
         has_variable_binning = True
         hist_binEdges = np.array(ref_var.nbins, dtype=float)
         hist_nBins = len(plot.nbins)-1
         model = ROOT.RDF.TH1DModel(plot_name+"_model_hist", plot_name, hist_nBins, hist_binEdges)
      else:
         model = ROOT.RDF.TH1DModel(plot_name+"_model_hist", plot_name, plot.nbins, plot.xmin, plot.xmax)

      tmp_hist = rdf.Histo1D(model, plot.name)
      if not tmp_hist.GetEntries():
         print("Empty histogram for:", input_filepath, " Exiting.")
         return

      tmp_hist.GetXaxis().SetTitle(plot.label)
      tmp_hist.GetYaxis().SetTitle("Raw MC events")
      tmp_hist.SetFillColor(ROOT.kCyan+2)
      tmp_hist.SetLineColor(ROOT.kCyan+2)

      #write out
      if sel_cutstring == "":
         filename = "bbtautau_noSel_"+plot_name+out_format
      else:
         filename = "bbtautau_withSel_"+plot_name+out_format
      fileout = os.path.join(out_dir_base, filename)

      canvas = ROOT.TCanvas("canvas", "canvas", 800, 800) 
      tmp_hist.Draw("hist same")
      canvas.SaveAs(fileout)

def makeEffPlots(dict_of_vars, ref_var, sel_cutstring, input_filepath, out_dir_base, out_format = ".png", do_log_y=False):

        if not os.path.exists(out_dir_base):
                os.mkdir(out_dir_base)

        rdf = ROOT.RDataFrame("events", input_filepath)

        if sel_cutstring:
                rdf = rdf.Filter(sel_cutstring) #apply the selection

        if not rdf:
                print("Empty file for:", input_filepath, " Exiting.")
                return

        #denominator hist
        print("Plotting at denominator:", ref_var.name)
        has_variable_binning = False
        
        if not isinstance(ref_var.nbins, int):
           has_variable_binning = True
           hist_binEdges = np.array(ref_var.nbins, dtype=float)
           hist_nBins = len(ref_var.nbins)-1
           model = ROOT.RDF.TH1DModel(ref_var.name+"_model_hist", ref_var.name, hist_nBins, hist_binEdges)
        else:
           model = ROOT.RDF.TH1DModel(ref_var.name+"_model_hist", ref_var.name, ref_var.nbins, ref_var.xmin, ref_var.xmax)
        
        tmp_hist_den = rdf.Histo1D(model, ref_var.name)
       
        if not tmp_hist_den.GetEntries():
           print("Empty histogram for:", input_filepath, " Exiting.")
           return
        else:
           print("Number entries denumerator: ", tmp_hist_den.GetEntries())
        tmp_den = getHfromRDF(tmp_hist_den)
        #tmp_hist.GetXaxis().SetTitle(plot.label)
        #tmp_hist.GetYaxis().SetTitle("Raw MC events")
        #tmp_hist.SetFillColor(ROOT.kCyan+2)
        #tmp_hist.SetLineColor(ROOT.kCyan+2)

        for plot_name, plot in dict_of_vars.items():
                print("Plotting:", plot_name)

                has_variable_binning = False
                if not isinstance(plot.nbins, int):
                        has_variable_binning = True
                        hist_binEdges = np.array(ref_var.nbins, dtype=float)
                        hist_nBins = len(plot.nbins)-1
                        model = ROOT.RDF.TH1DModel(plot_name+"_model_hist", plot_name, hist_nBins, hist_binEdges)
                else:
                        model = ROOT.RDF.TH1DModel(plot_name+"_model_hist", plot_name, plot.nbins, plot.xmin, plot.xmax)

                tmp_hist_num = rdf.Histo1D(model, plot.name)               
 
                if not tmp_hist_num.GetEntries():
                        print("Empty histogram for:", input_filepath, " Exiting.")
                        return
                else:
                        print("Number entries numerator: ", tmp_hist_num.GetEntries())

                tmp_num = getHfromRDF(tmp_hist_num)
               
                if ROOT.TEfficiency.CheckConsistency(tmp_num, tmp_den):
                   Eff = ROOT.TEfficiency(tmp_num, tmp_den)
                   Eff.SetTitle(";"+plot.label+";Efficiency")
                   Eff.SetTitle(plot_name)
                   ptext = ROOT.TPaveText(.7,.85,.85,.9,option='NDC')
                   if "loose" in plot_name:
                      ptext.AddText("loose tag")
                   elif "medium" in plot_name:
                      ptext.AddText("medium tag")  
                   elif "tight" in plot_name:
                      ptext.AddText("tight tag")   
                   else:
                      ptext.AddText(plot_name)                     
         #write out
                   if sel_cutstring == "":
                      filename = "bbtautau_noSel_Eff"+plot_name+out_format
                   else:
                      filename = "bbtautau_withSel_Eff"+plot_name+out_format
                   fileout = os.path.join(out_dir_base, filename)

                   canvas = ROOT.TCanvas("canvas", "canvas", 900, 700) 
                   canvas.SetGrid()
                   Eff.Draw("AP")
                   canvas.Update()
                   graph = Eff.GetPaintedGraph()
                   graph.SetMinimum(0.6)
                   graph.SetMaximum(1) 
                   canvas.Update() 
                   canvas.SetLogx()
                   ptext.Draw()
                   canvas.SaveAs(fileout)
                else:
                   print("The histograms are not consistent!")


if __name__ == "__main__":

   parser = argparse.ArgumentParser(description="Plot b-tagging efficiencies from Delphes")
   parser.add_argument('--input', '-i', metavar="INPUTDIR", dest="inFile", required=True, help="Path to the input file.")
   parser.add_argument('--outdir', '-o', metavar="OUTPUTDIR", dest="outDir", required=True, help="Output directory.")
   args = parser.parse_args()

   #use a custom namedntuple to transfer the plotting info
   PlotSpecs = namedtuple('PlotSpecs', ['name', 'xmin', 'xmax', 'label', 'nbins'])

   #plot some variables without any selection:
   bbyy_plots_nosel = {
      "n_b_jets_loose":PlotSpecs(name="n_b_jets_loose", xmin=0, xmax=5, label="n_b_jets_loose", nbins=5),
      "n_b_jets_medium":PlotSpecs(name="n_b_jets_medium", xmin=0, xmax=5, label="n_b_jets_medium", nbins=5),
      "n_b_jets_tight":PlotSpecs(name="n_b_jets_tight", xmin=0, xmax=5, label="n_b_jets_tight", nbins=5),
      "n_jets_genmatched_b": PlotSpecs(name="n_jets_genmatched_b", xmin=0, xmax=5, label="n_jets_genmatched_b", nbins=5),
      "n_bjets_loose_genmatched_b": PlotSpecs(name="n_bjets_loose_genmatched_b", xmin=0, xmax=5, label="n_bjets_loose_genmatched_b", nbins=5),
      "n_bjets_medium_genmatched_b": PlotSpecs(name="n_bjets_medium_genmatched_b", xmin=0, xmax=5, label="n_bjets_medium_genmatched_b", nbins=5),
      "n_bjets_tight_genmatched_b": PlotSpecs(name="n_bjets_tight_genmatched_b", xmin=0, xmax=5, label="n_bjets_tight_genmatched_b", nbins=5),
   }

   sel_cuts_empty = ""
   makePlots(bbyy_plots_nosel, sel_cuts_empty, args.inFile, args.outDir)

   #bjet tagging efficiencies:
   binedges=[20,50,100,200,500,1000,5000] #same pT binning as in the delphes card
   bbyy_plot_pTeff={
      "pT_bjets_loose_genmatched_b":PlotSpecs(name="pT_bjets_loose_genmatched_b", xmin=0., xmax=1000., label="p_{T} bjets [GeV]", nbins=binedges),
      "pT_bjets_medium_genmatched_b":PlotSpecs(name="pT_bjets_medium_genmatched_b", xmin=0., xmax=1000., label="p_{T} bjets [GeV]", nbins=binedges),
      "pT_bjets_tight_genmatched_b":PlotSpecs(name="pT_bjets_tight_genmatched_b", xmin=0., xmax=1000., label="p_{T} bjets [GeV]", nbins=binedges),
   }
   #select only one eta bin:
   sel_cuts_eta_4 = "n_jets_genmatched_b == 2 && abs(eta_jets_genmatched_b[0]) < 4. && abs(eta_jets_genmatched_b[1]) < 4."

   pT_ref = PlotSpecs(name="pT_jets_genmatched_b", xmin=0., xmax=1000., label="p_{T} #tau_{h} [GeV]", nbins=binedges)
   eta_ref = PlotSpecs(name="eta_jets_genmatched_b", xmin=-5, xmax=5., label="#eta  #tau_{h}", nbins=20)

   makeEffPlots(bbyy_plot_pTeff, pT_ref, sel_cuts_eta_4, args.inFile, args.outDir)

# run it with:
# python plot_tag_eff.py -i <file> -o <out_name>
