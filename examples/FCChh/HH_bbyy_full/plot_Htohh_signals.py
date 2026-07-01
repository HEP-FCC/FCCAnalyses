import ROOT
import os 
from collections import namedtuple
from array import array
import copy

ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0)



def plot_from_ws_inputs(wsinput_file, signals_list, outputpath):

    colour_sequence = [ "#e76300", "#ffa90e", "#656364", "#3f90da",  ]

    hist_file = ROOT.TFile.Open(wsinput_file)

    #get the bkgs hist:
    hist_ggjets = copy.deepcopy(hist_file.Get("mgp8_pp_ggjets_84TeV"))
    hist_ggjets.SetFillColorAlpha(ROOT.TColor.GetColor(colour_sequence[0]), 0.4)
    hist_ggjets.SetLineColor(ROOT.TColor.GetColor(colour_sequence[0]))
    hist_ggjets.SetLineWidth(2)
    hist_ggjets.SetTitle("#it{#gamma#gamma+jets}")
    hist_gjets =copy.deepcopy( hist_file.Get("mgp8_pp_gjets_84TeV"))
    hist_gjets.SetFillColorAlpha(ROOT.TColor.GetColor(colour_sequence[1]), 0.4)
    hist_gjets.SetLineColor(ROOT.TColor.GetColor(colour_sequence[1]))
    hist_gjets.SetLineWidth(2)
    hist_gjets.SetTitle("#it{#gamma+jets}")
    hist_stack = ROOT.THStack("hist_stack","")
    hist_stack.Add(hist_ggjets)
    hist_stack.Add(hist_gjets)

    #make one plot per signal
    for proc_name in signals_list:
        signal_mass = proc_name.split("GeV")[0].split("mH_")[1].strip()+" GeV"
        signal_label = "#it{{m_{{H}} = {}}}".format(signal_mass)

        print("Plotting signal:", proc_name)
        hist_signal = copy.deepcopy(hist_file.Get(proc_name))

        hist_signal.SetFillColorAlpha(ROOT.TColor.GetColor(colour_sequence[2]), 0.4)
        hist_signal.SetLineColor(ROOT.TColor.GetColor(colour_sequence[2]))
        hist_signal.SetLineWidth(2)
        hist_signal.SetTitle(signal_label)
        
        leg = ROOT.TLegend(0.6, 0.65, 0.90, 0.88)
        leg.AddEntry(hist_ggjets, hist_ggjets.GetTitle(), "f")
        leg.AddEntry(hist_gjets, hist_gjets.GetTitle(), "f")
        leg.AddEntry(hist_signal, hist_signal.GetTitle(), "l")

        canvas = ROOT.TCanvas("canvas", "canvas", 800, 800) 
        canvas.cd()
        canvas.SetLeftMargin(0.15)
        canvas.SetRightMargin(0.05)

        hist_stack.Draw("HIST")
        hist_signal.Draw("HIST SAME")

        hist_stack.SetMaximum(10e7)
        hist_stack.SetMinimum(1)

        hist_stack.GetXaxis().SetTitle("m_{bb#gamma#gamma} [GeV]")
        hist_stack.GetYaxis().SetTitle("Events")

        hist_signal.GetXaxis().SetTitle("m_{bb#gamma#gamma} [GeV]")
        hist_signal.GetYaxis().SetTitle("Events")

        ROOT.gPad.Update()

        leg.SetFillStyle( 0 )
        leg.SetBorderSize( 0 )
        leg.SetTextFont( 43 )
        leg.SetTextSize( 22 )
        leg.SetNColumns( 2 )
        leg.SetColumnSeparation(-0.05)
        leg.Draw()
        canvas.SetLogy(True)
        
        outname = os.path.join(outputpath, "hist_ws_input_{}.png".format(proc_name))
        print("Saving histogram")
        canvas.SaveAs(outname)
        canvas.Close()

    

def get_rdf(input_filepath):

    print("Getting rdf from:", input_filepath)

    if input_filepath.endswith(".root"):
        rdf = ROOT.RDataFrame("events", input_filepath)
    else:
        print("Adding chunks ..")
        # rdf = ROOT.RDataFrame("events", input_filepath+"/chunk99.root")
        rdf = ROOT.RDataFrame("events", input_filepath+"/chunk*")

    if not rdf:
        print("Empty file for:", input_filepath, " Exiting.")
        return

    # print(rdf.GetColumnNames())

    return rdf

def draw_separate_hist(hist, plot_name, outputpath, x_label):
    canvas = ROOT.TCanvas("canvas", "canvas", 800, 800) 
    canvas.cd()

    canvas.SetLeftMargin(0.16)
    canvas.SetRightMargin(0.03)

    leg = ROOT.TLegend(0.6, 0.65, 0.90, 0.88)
    leg.AddEntry(hist.GetValue(), hist.GetTitle(), "l")

    hist.GetYaxis().SetTitle("Events")
    hist.GetXaxis().SetTitle(x_label)

    hist.Draw("HIST")
    # canvas.SetLogy(True)

    
    # leg.AddEntry(hist, hist.GetTitle(), "l")
    leg.SetFillStyle( 0 )
    leg.SetBorderSize( 0 )
    leg.SetTextFont( 43 )
    leg.SetTextSize( 22 )
    leg.SetNColumns( 2 )
    leg.SetColumnSeparation(-0.05)
    leg.Draw()
    
    outname = os.path.join(outputpath, "hist_{}.png".format(plot_name))
    print("Saving separate histogram")
    canvas.SaveAs(outname)


def plot_Htohh_signals(inputpath, outputpath, plot_specs, plot_name, signals_list):

    has_variable_binning = False
    model = None 

    if not isinstance(plot_specs.nbins, int):
        print("VAR BINS")
        has_variable_binning = True
        hist_binEdges = array("d", plot_specs.nbins)
        hist_nBins = len(plot_specs.nbins)-1
        #init the histogram with variable bin widths:
        model = ROOT.RDF.TH1DModel(plot_name+"_model_hist", plot_name, hist_nBins, hist_binEdges)

    else:
        model = ROOT.RDF.TH1DModel(plot_name+"_model_hist", plot_name, plot_specs.nbins, plot_specs.xmin, plot_specs.xmax)
    
    hist_list = []
    hist_stack = ROOT.THStack("hist_stack","")
    leg = ROOT.TLegend(0.6, 0.65, 0.90, 0.88)
    colour_index = 0

    for signal in signals_list:
        signal_mass = signal.split("GeV")[0].split("mH_")[1].strip()+" GeV"
        print(signal_mass)
        
        filepath = os.path.join(inputpath, signal+".root") #using merged versions
        rdf = get_rdf(filepath)

        tmp_hist = rdf.Histo1D(model, plot_specs.name)
        tmp_hist.SetLineColor(30+colour_index)
        tmp_hist.SetLineWidth(2)
        tmp_hist.GetXaxis().SetTitle(plot_specs.label)
        tmp_hist.GetXaxis().SetTitleOffset(1.35)
        tmp_hist.GetYaxis().SetTitle("Fraction of events")
        tmp_hist.SetTitle(signal_mass)

        #normalise to unit area
        tmp_hist.Scale(1./tmp_hist.Integral())
        
        hist_name = "hist_{}_{}.png".format(plot_name, signal)
        draw_separate_hist(tmp_hist, signal+"_"+plot_name, outputpath, plot_specs.label)

        hist_to_add = copy.deepcopy(tmp_hist.GetValue())
        # hist_to_add.SetTitle(HT_titles[HT_slice_file])

        hist_list.append(hist_to_add)

        colour_index+=1

    for hist in hist_list:
        hist_stack.Add(hist)

        # hist_stack.Add(hist_to_add)
        leg.AddEntry(hist, hist.GetTitle(), "l")

    #setup canvas
    canvas = ROOT.TCanvas("canvas", "canvas", 800, 800) 
    canvas.cd()
    canvas.SetLeftMargin(0.16)
    canvas.SetRightMargin(0.03)

    hist_stack.Draw("HIST NOSTACK")

    hist_stack.GetXaxis().SetTitle(plot_specs.label)
    hist_stack.GetYaxis().SetTitle("Fraction of events")

    leg.SetHeader("Signal masses")
    leg.SetFillStyle( 0 )
    leg.SetBorderSize( 0 )
    leg.SetTextFont( 43 )
    leg.SetTextSize( 22 )
    leg.SetNColumns( 2 )
    leg.SetColumnSeparation(-0.05)
    leg.Draw()
    # canvas.SetLogy(True)
    
    outname = os.path.join(outputpath, "hist_{}.png".format(plot_name))
    print("Saving histogram")
    canvas.SaveAs(outname)

#compare myy vs m_yy uncorrected - directly from ntuples not from the processed!
def plot_compare_myy_wCorrection(inputpath, signals_list, outputpath, do_ratio=True, do_logy=False, plot_format="png"):
    colour_sequence = [ "#3f90da", "#a96b59", "#92dadd" ]

    plot_specs_corrected = PlotSpecs(name="m_yy",  nbins= 80, xmin=115., xmax=135., label="m_{#gamma#gamma} [GeV]" )
    plot_specs_uncorrected = PlotSpecs(name="m_yy_uncorr",  nbins= 80, xmin=115., xmax=135., label="m_{#gamma#gamma} [GeV]" )
    plot_name = "myy_corr_vs_uncorr"
    has_variable_binning = False
    model = None 

    if not isinstance(plot_specs_corrected.nbins, int):
        print("VAR BINS")
        has_variable_binning = True
        hist_binEdges = array("d", plot_specs_corrected.nbins)
        hist_nBins = len(plot_specs_corrected.nbins)-1
        #init the histogram with variable bin widths:
        model = ROOT.RDF.TH1DModel(plot_name+"_model_hist", plot_name, hist_nBins, hist_binEdges)

    else:
        model = ROOT.RDF.TH1DModel(plot_name+"_model_hist", plot_name, plot_specs_corrected.nbins, plot_specs_corrected.xmin, plot_specs_corrected.xmax)
    

    signals_list =["mgp8_pp_Htohh_mH_300GeV_84TeV_hhbbaa"] #TEMP OPVERWRITE
    for signal in signals_list:
        signal_mass = signal.split("GeV")[0].split("mH_")[1].strip()+" GeV"
        signal_label = "#it{{m_{{H}} = {}}}".format(signal_mass)
        filepath = os.path.join(inputpath, signal)
        histname = "hist_compare_myy_corr_vs_uncorr_{}".format(signal)
        print("Reading files for:", filepath)

        rdf = get_rdf(filepath)

        #corrected:
        hist_corr = rdf.Histo1D(model, plot_specs_corrected.name)
        hist_corr.SetLineColor(ROOT.TColor.GetColor(colour_sequence[0]))
        hist_corr.SetFillColorAlpha(ROOT.TColor.GetColor(colour_sequence[0]), 0.3)
        hist_corr.SetLineWidth(2)
        hist_corr.GetXaxis().SetTitle(plot_specs_corrected.label)
        hist_corr.GetXaxis().SetTitleOffset(1.35)
        hist_corr.GetYaxis().SetTitle("Fraction of events")
        hist_corr.SetTitle("Corrected")
        #normalise to unit area
        hist_corr.Scale(1./hist_corr.Integral())

        #uncorrected:
        hist_uncorr = rdf.Histo1D(model, plot_specs_uncorrected.name)
        hist_uncorr.SetLineColor(ROOT.TColor.GetColor(colour_sequence[1]))
        hist_uncorr.SetFillColorAlpha(ROOT.TColor.GetColor(colour_sequence[1]), 0.3)
        hist_uncorr.SetLineWidth(2)
        hist_uncorr.GetXaxis().SetTitle(plot_specs_uncorrected.label)
        hist_uncorr.GetXaxis().SetTitleOffset(1.35)
        hist_uncorr.GetYaxis().SetTitle("Fraction of events")
        hist_uncorr.SetTitle("Uncorrected")
         #normalise to unit area
        hist_uncorr.Scale(1./hist_uncorr.Integral())

        #setup canvas
        canvas = ROOT.TCanvas("canvas", "canvas", 800, 800) 
        canvas.SetLogy(do_logy)
        canvas.cd()

        canvas.SetLeftMargin(0.16)

        if do_ratio:
            hist_ratio = copy.deepcopy(hist_corr.GetValue())
            hist_ratio.SetName("hist_ratio")
            hist_ratio.Divide(hist_uncorr.GetValue())
            histname+="_ratio"
            hist_ratio.GetYaxis().SetTitle("Ratio corr/uncorr")

            pad_up = ROOT.TPad("pad_up", "pad_up", 0., 0., 1., 1.)
            pad_up.SetFillStyle(0)
            pad_up.SetBottomMargin(0.32)
            # pad_up.SetTopMargin(0.03)
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
            
            hist_corr.GetXaxis().SetLabelSize(0)
            hist_corr.GetXaxis().SetTitle("")
            hist_uncorr.GetXaxis().SetLabelSize(0)
            hist_uncorr.GetXaxis().SetTitle("")

        #draw histograms and legend
        hist_corr.Draw("HIST SAME")
        hist_uncorr.Draw("HIST SAME")

        #title label
        latex = ROOT.TLatex()
        latex.SetNDC()
        latex.SetTextAlign(31)
        latex.SetTextSize(0.04)
        latex.DrawLatex(0.90, 0.94, "#it{FCCAnalyses: FCC-hh Simulation (Delphes)}")

        #labels:
        energy = "84 TeV"
        legend_label = "H #rightarrow hh #rightarrow bb#gamma#gamma"

        latex.SetNDC(ROOT.kTRUE)  # Use normalized device coordinates
        latex.SetTextAlign(13)  
        latex.SetTextSize(0.03)
        latex.DrawLatex(0.18, 0.87, "#bf{{#it{{#sqrt{{s}} = {}}}}}".format(energy).strip())
        latex.DrawLatex(0.18, 0.83, "#bf{{#it{{{}}}}}".format(legend_label).strip())
        latex.DrawLatex(0.18, 0.79, "#bf{{#it{{{}}}}}".format(signal_label).strip())


        leg = ROOT.TLegend(0.75, 0.75, 0.88, 0.88)
        leg.SetFillStyle( 0 )
        leg.SetBorderSize( 0 )
        # leg.SetMargin( 0.1)
        leg.SetTextFont( 43 )
        leg.SetTextSize( 20 )
        # leg.SetColumnSeparation(-0.05)
        # leg.SetNColumns(2)
        leg.AddEntry(hist_corr.GetValue(), hist_corr.GetTitle(), "l")
        leg.AddEntry(hist_uncorr.GetValue(), hist_uncorr.GetTitle(), "l")
        leg.Draw()

        if do_ratio:
            pad_up.Update()
            pad_low.cd()

            pad_low.cd()
            pad_low.Update()
            hist_ratio.Draw("E0P")
            pad_low.RedrawAxis()

            canvas.RedrawAxis()
            canvas.Modified()
            canvas.Update()	

        histfile_path = os.path.join(outputpath, "{}.{}".format(histname, plot_format))
        canvas.SaveAs(histfile_path)



if __name__ == "__main__":

    PlotSpecs = namedtuple('PlotSpecs', ['name', 'xmin', 'xmax', 'label', 'nbins'])
    
    plots = {
            "m_bbyy":PlotSpecs(name="hh_m", nbins= 80, xmin=250., xmax=1150., label="m_{bb#gamma#gamma} [GeV]", ), 
            "m_bb":PlotSpecs(name="hbb_m", nbins= 80, xmin=75., xmax=205., label="m_{bb} [GeV]", ), 
            "m_yy":PlotSpecs(name="haa_m", nbins= 80, xmin=115., xmax=135., label="m_{#gamma#gamma} [GeV]", ), 
            "pT_gamma1":PlotSpecs(name="a1_pt", nbins= 80, xmin=0., xmax=250., label="m_{#gamma_{1}} [GeV]", ), 
            "pT_gamma2":PlotSpecs(name="a2_pt", nbins= 80, xmin=0., xmax=250., label="m_{#gamma_{2}} [GeV]", ), 

    }

    # signals_list=["mgp8_pp_Htohh_mH_300GeV_84TeV_hhbbaa"]

    signals_list = [
            'mgp8_pp_Htohh_mH_300GeV_84TeV_hhbbaa', 
            # 'mgp8_pp_Htohh_mH_350GeV_84TeV_hhbbaa', 
            # 'mgp8_pp_Htohh_mH_400GeV_84TeV_hhbbaa', 'mgp8_pp_Htohh_mH_450GeV_84TeV_hhbbaa',
            # 'mgp8_pp_Htohh_mH_500GeV_84TeV_hhbbaa', 'mgp8_pp_Htohh_mH_550GeV_84TeV_hhbbaa',
            # 'mgp8_pp_Htohh_mH_600GeV_84TeV_hhbbaa', 'mgp8_pp_Htohh_mH_650GeV_84TeV_hhbbaa',
            # 'mgp8_pp_Htohh_mH_700GeV_84TeV_hhbbaa', 'mgp8_pp_Htohh_mH_750GeV_84TeV_hhbbaa',
            # 'mgp8_pp_Htohh_mH_800GeV_84TeV_hhbbaa', 'mgp8_pp_Htohh_mH_850GeV_84TeV_hhbbaa',
            # 'mgp8_pp_Htohh_mH_900GeV_84TeV_hhbbaa', 'mgp8_pp_Htohh_mH_950GeV_84TeV_hhbbaa',
            # 'mgp8_pp_Htohh_mH_1000GeV_84TeV_hhbbaa', 
    ]

    input_dir = "/eos/experiment/fcc/hh/analysis_ntuples/fcc_v07/II/bbyy_analysis/merged/"
    input_dir_ntuples = "/eos/experiment/fcc/hh/analysis_ntuples/fcc_v07/II/bbyy_analysis/"

    plot_path = "/eos/user/b/bistapf/bbyy_resonant_search_plots/"

    wsinput_file = "/eos/experiment/fcc/hh/analysis_ntuples/fcc_v07/II/bbyy_analysis/ws_inputs/resonant_Htohh_bbyy_analysis_hists.root"

    #plot comparison of corrected vs uncorrected m_yy from the FCCAna ntuples (before processing)
    plot_compare_myy_wCorrection(input_dir_ntuples, signals_list, plot_path)
    exit()

    #plot directly from the ws inputs
    plot_from_ws_inputs(wsinput_file, signals_list, plot_path)
    exit()

    #plot from the processed chunks (with preselection only)
    for plot_name, plot_specs in plots.items():
        plot_Htohh_signals(input_dir, plot_path, plot_specs, plot_name, signals_list)