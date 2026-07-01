import ROOT
import os 
from collections import namedtuple
from array import array
import copy

ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptTitle(0)

from plot_HT_split_check import get_rdf

PlotSpecs = namedtuple('PlotSpecs', ['name', 'xmin', 'xmax', 'label', 'nbins'])

ProcessSpecs = namedtuple('ProcessSpecs', ['name', 'label', 'filepath', 'colour'])

#compare two histograms
def plot_hist_compare(hist_name, plot_specs, process1, process2, out_dir, norm_info="", yaxis_label="Events", 
                        do_ratio=True, file_format="png", do_logy=False, tree_name="events", weight_name="", do_norm_unit=False ):

    rdf1 = get_rdf(process1.filepath)
    rdf2 = get_rdf(process2.filepath)


    # hist_model = ROOT.RDF.TH1DModel(hist_name, hist_name, plot_specs.nbins, plot_specs.xmin, plot_specs.xmax)
    #going to need a TH1Model to fill:
    has_variable_binning = False
    if not isinstance(plot_specs.nbins, int):
        has_variable_binning = True
        hist_binEdges = array("d", plot_specs.nbins)
        hist_nBins = len(plot_specs.nbins)-1
        #init the histogram with variable bin widths:
        hist_model = ROOT.RDF.TH1DModel(hist_name, hist_name, hist_nBins, hist_binEdges)


    else:
        hist_model = ROOT.RDF.TH1DModel(hist_name, hist_name, plot_specs.nbins, plot_specs.xmin, plot_specs.xmax)

    

    #get the histograms:
    if weight_name:
        hist1 = rdf1.Histo1D(hist_model, plot_specs.name, weight_name).GetValue()  
        hist2 = rdf2.Histo1D(hist_model, plot_specs.name, weight_name).GetValue()  
    else:
        hist1 = rdf1.Histo1D(hist_model, plot_specs.name).GetValue()  
        hist2 = rdf2.Histo1D(hist_model, plot_specs.name).GetValue()  


    hist1.SetTitle(process1.label)
    hist1.SetLineWidth(2)
    hist1.SetLineColor(process1.colour)
    hist1.GetYaxis().SetTitle(yaxis_label)
    hist1.GetXaxis().SetTitle(plot_specs.label)
    hist1.Sumw2()

    
    hist2.SetTitle(process2.label)
    hist2.SetLineWidth(2)
    hist2.SetLineColor(process2.colour)
    hist2.GetYaxis().SetTitle(yaxis_label)
    hist2.GetXaxis().SetTitle(plot_specs.label)
    hist2.Sumw2()

    if norm_info:
        sow1 = rdf1.Histo1D("weight", "weight").Integral() #TO CHECK THAT THIS IS CORRECT
        # print(sow1)
        sow2 = rdf2.Histo1D("weight", "weight").Integral()
        # print(sow2)
        hist_name+="_normed"
        hist1.Scale(norm_info.lumi*norm_info.kfactor*norm_info.xsection/sow1)
        hist2.Scale(norm_info.lumi*norm_info.kfactor*norm_info.xsection/sow2)

    elif do_norm_unit:
        hist1.Scale(1./hist1.Integral())
        hist2.Scale(1./hist2.Integral())
        hist_name+="_unitNormed"

    #set output file name
    if do_ratio:
        hist_ratio = hist1.Clone()
        hist_ratio.Divide( hist2 )
        hist1.GetXaxis().SetLabelSize(0)
        hist1.GetXaxis().SetTitle("")
        hist2.GetXaxis().SetLabelSize(0)
        hist2.GetXaxis().SetTitle("")
        hist_name+="_ratio"
        
    if do_logy:
        hist_name+="_logY"


    histfile_name = "{}.{}".format(hist_name, file_format)
    histfile_path = os.path.join(out_dir, histfile_name)

    #setup canvas
    canvas = ROOT.TCanvas("canvas", "canvas", 800, 800) 
    canvas.SetLogy(do_logy)
    canvas.cd()

    canvas.SetLeftMargin(0.16)

    if do_ratio:
        pad_up = ROOT.TPad("pad_up", "pad_up", 0., 0., 1., 1.)
        pad_up.SetFillStyle(0)
        pad_up.SetBottomMargin(0.32)
        pad_up.SetTopMargin(0.03)
        pad_up.SetLeftMargin(0.13)
        pad_up.SetRightMargin(0.05)
        pad_up.SetLogy(do_logy)
        pad_up.Draw()

        pad_low = ROOT.TPad("pad_low", "pad_low", 0., 0., 1., 1.);
        pad_low.SetFillStyle(0)
        pad_low.SetBottomMargin(0.12)
        pad_low.SetTopMargin(0.72)
        pad_low.SetLeftMargin(0.13)
        pad_low.SetRightMargin(0.05)
        pad_low.SetGrid()
        pad_low.Draw()

        pad_up.cd()

    #draw histograms and legend
    hist1.Draw("HIST SAME")
    hist2.Draw("HIST SAME")

    leg = ROOT.TLegend(0.77, 0.77, 0.95, 0.95)
    leg.SetFillStyle( 0 )
    leg.SetBorderSize( 0 )
    leg.SetMargin( 0.1)
    leg.SetTextFont( 43 )
    leg.SetTextSize( 20 )
    leg.SetColumnSeparation(-0.05)
    if norm_info:
        leg.SetHeader("{} fb^{{-1}}".format(norm_info.lumi))
    leg.AddEntry(hist1, hist1.GetTitle(), "l")
    leg.AddEntry(hist2, hist2.GetTitle(), "l")
    leg.Draw()

    if do_ratio:
        pad_low.cd()
        hist_ratio.GetYaxis().SetTitle("Ratio")
        hist_ratio.GetYaxis().SetTitleOffset(1.95)
        hist_ratio.GetYaxis().SetNdivisions(6)

        pad_low.cd()
        pad_low.Update()
        hist_ratio.Draw("E0P")
        pad_low.RedrawAxis()

        canvas.RedrawAxis()
        canvas.Modified()
        canvas.Update()	


    canvas.SaveAs(histfile_path)


def plot_bbyy_bkgs_jetmatching_check(input_dir_old, input_dir_new, output_dir):
    print("Plotting checks on pre-selection variables in bbyy")

    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    plots = {
            "n_sel_bjets":PlotSpecs(name="nbjets", xmin=0., xmax=10., label="n b-jets", nbins=10), 
            "n_sel_photons":PlotSpecs(name="ngamma", xmin=0., xmax=10., label="n photons", nbins=10), 
            "m_bb":PlotSpecs(name="m_bb", xmin=0., xmax=300., label="m_{bb} in GeV", nbins=60), 
            "m_yy":PlotSpecs(name="m_yy", xmin=50., xmax=250., label="m_{bb} in GeV", nbins=60), 
            # "pT_mumu_HTslices":PlotSpecs(name="pT_mumu", xmin=0., xmax=1100., label="pT_{#mu#mu} [GeV]", 
            # 							nbins=[ 0., 100., 300., 500., 700., 900., 1100. ]), 

    }

    list_of_samples = ["mgp8_pp_h012j_5f_haa"]

    for sample in list_of_samples:

        #first slice:
        old_ntuples = os.path.join(input_dir_old, sample)
        new_ntuples = os.path.join(input_dir_new, sample)

        processes_sample = {
                                "Old":ProcessSpecs(name=sample, label="fcc_v05 - NO JET MATCHING", filepath=old_ntuples, colour=36 ),
                                "New":ProcessSpecs(name=sample, label="fcc_v07", filepath=new_ntuples, colour=46 ),

        }

        for plot_name, plot_specs in plots.items():
            plot_hist_compare("{}_compare_{}".format(sample, plot_name), plot_specs, processes_sample["Old"], processes_sample["New"], output_dir, norm_info="", yaxis_label="Events", 
                            do_ratio=True, file_format="png", do_logy=False, tree_name="events", weight_name="", do_norm_unit=False )



if __name__ == "__main__":

    plot_bbyy_bkgs_jetmatching_check(
                                "/eos/experiment/fcc/hh/analysis_ntuples/fcc_v07/I/bbyy_analysis_nopresel/", 
                                "/eos/experiment/fcc/hh/analysis_ntuples/fcc_v07/I/bbyy_analysis_nopresel/", 
                                "./plot_bbyy_jetmatching_preselvars_check/")



    