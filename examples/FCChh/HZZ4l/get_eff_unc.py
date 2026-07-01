#Derive the uncertainty systematics, depending on the pT of the muon

import ROOT
import numpy as np
import matplotlib.pyplot as plt
import os
import json
from argparse import ArgumentParser
import copy

ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0)


# To work with RDF, need to compile the RDF function in C
ROOT.gInterpreter.Declare(
"""
using namespace ROOT;
float GetEfficiencyScaleFactorUp(float pt) {
	return 1.+(0.25*sqrt(2500./pow(pt, 2) + 25./pt + 1.))/100.;
}
""")

ROOT.gInterpreter.Declare(
"""
using namespace ROOT;
float GetEfficiencyScaleFactorDown(float pt) {
	return 1.-(0.25*sqrt(2500./pow(pt, 2) + 25./pt + 1.))/100.;
}
""")

def f(pt):
	return 0.25*np.sqrt(2500./pt**2 + 25./pt + 1.)

def SF_function(pt):
	return 1.+(0.25*np.sqrt(2500./pt**2 + 25./pt + 1.))/100.

def test_unc_fct():
	pt = np.arange(5., 100., 1)

	for tester_pt in np.arange(5., 100., 1):
		print("pT = {} , delta Eff in % = {:.2f} and SF = {:.4f}".format(tester_pt, f(tester_pt), SF_function(tester_pt)))

	plt.plot(pt, SF_function(pt), lw=2.0, color='blue',  label='mu')
	plt.plot(pt, 2*SF_function(pt), lw=2.0, color='green', label='e, gamma')
	plt.xlabel(r'$p_T [GeV]$', fontsize=18)
	plt.ylabel(r'Scale factor', fontsize=18)

	plt.legend()

	#plt.show()
	plt.savefig('SF_vs_pT.png',format='png')


def get_rdf(input_filepath):

	print("Getting rdf from:", input_filepath)
	rdf = None
	if input_filepath.endswith(".root"):
		try:
			rdf = ROOT.RDataFrame("events", input_filepath)
		except:
			print("File {} appears to be empty.".format(input_filepath))
			return
	else:
		print("Adding chunks ..")
		# rdf = ROOT.RDataFrame("events", input_filepath+"/chunk99.root")
		rdf = ROOT.RDataFrame("events", input_filepath+"/chunk*")

	if not rdf:
		print("Empty file for:", input_filepath, " Exiting.")
		return

	# print(rdf.GetColumnNames())

	return rdf

def plot_histo(rdf, var, outpath, outname, fileformat=".png"):
	temp_hist = rdf.Histo1D(var)
	canvas = ROOT.TCanvas("canvas", "canvas", 800, 800) 
	canvas.cd()
	temp_hist.Draw()
	canvas.SaveAs(os.path.join(outpath, outname+fileformat))

def plot_scalefactors(process_name, SF_vs_pT_dict, plotdir):
	out_path = os.path.join(plotdir, "EffScaleFactor_vs_pT_for_{}.png".format(process_name))
	
	x = list(SF_vs_pT_dict.keys())
	y = list(SF_vs_pT_dict.values())

	# Plotting
	plt.figure(figsize=(10, 6))
	plt.plot(x, y, marker='o')  # 'o' adds markers to the data points
	plt.title('Muon reconstruction efficiencies')
	plt.xlabel('Minimum pT(H) in GeV')
	plt.ylabel('Scalefactor (up)')
	plt.grid(True)
	plt.xticks(x)  # Set x ticks to be the keys of the dictionary
	plt.yticks([round(i, 2) for i in y])  # Customize y ticks to show rounded values
	plt.savefig(out_path)

def plot_syst_hist_compare(hist_nom, hist_up, hist_down, hist_name, outpath, fileformat=".png", do_ratio=True, do_logy=True):

	hist_nom.SetTitle("Nominal")
	hist_nom.SetLineColor(ROOT.kBlack)
	hist_nom.SetLineWidth(2)

	hist_up.SetTitle("Up")
	hist_up.SetLineColor(ROOT.kRed+2)
	hist_up.SetLineWidth(2)

	hist_down.SetTitle("Down")
	hist_down.SetLineColor(ROOT.kBlue+2)
	hist_down.SetLineWidth(2)

	if do_ratio:
		hist_ratio_up = hist_up.Clone()
		hist_ratio_up.Divide( hist_nom )

		hist_ratio_down = hist_down.Clone()
		hist_ratio_down.Divide( hist_nom )

		hist_nom.GetXaxis().SetLabelSize(0)
		hist_nom.GetXaxis().SetTitle("")
		hist_nom.GetXaxis().SetLabelSize(0)
		hist_nom.GetXaxis().SetTitle("")
		hist_name+="_ratio"
		
	if do_logy:
		hist_name+="_logY"
	
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
	
	hist_nom.Draw("HIST E")
	hist_up.Draw("HIST E SAME")
	hist_down.Draw("HIST E SAME")
	
	leg = ROOT.TLegend(0.77, 0.77, 0.95, 0.95)
	leg.SetFillStyle( 0 )
	leg.SetBorderSize( 0 )
	leg.SetMargin( 0.1)
	leg.SetTextFont( 43 )
	leg.SetTextSize( 20 )
	leg.SetColumnSeparation(-0.05)
	leg.AddEntry(hist_nom, hist_nom.GetTitle(), "l")
	leg.AddEntry(hist_up, hist_up.GetTitle(), "l")
	leg.AddEntry(hist_down, hist_down.GetTitle(), "l")
	leg.Draw()

	if do_ratio:
		pad_low.cd()
		hist_ratio_up.GetYaxis().SetTitle("Ratio")
		hist_ratio_up.GetYaxis().SetTitleOffset(1.95)
		hist_ratio_up.GetYaxis().SetNdivisions(6)

		hist_ratio_up.SetMaximum(1.01)
		hist_ratio_up.SetMinimum(0.99)

		pad_low.cd()
		pad_low.Update()
		hist_ratio_up.Draw("HIST")
		hist_ratio_down.Draw("HIST SAME")
		pad_low.RedrawAxis()

		canvas.RedrawAxis()
		canvas.Modified()
		canvas.Update()	

	outname = os.path.join(outpath, hist_name+fileformat)
	canvas.SaveAs(outname)

def get_SF_for_min_pT_cuts(process, base_inpath, base_plotpath, pT_step = 50, pT_range_min= 50, pT_range_max=550):
	# loop over all pT minimum cuts, and make a list of SF
	dict_SF_vs_pT = {}

	for pT_cut in range(pT_range_min, pT_range_max, pT_step):
		print("Getting Scalefactors for pT cut = ", pT_cut)

		#histogram templates for totals to fill:
		total_hist_nom = None
		total_hist_up = None
		total_hist_down = None

		for process in processes:
			print("Processing sample: ", process)
		
			infilename = "{}_sel3_pTH{}.root".format(process, pT_cut)
			infilepath = os.path.join(base_inpath, infilename)
			outfilename_up = "{}_sel3_pTH{}_SYST1UP.root".format(process, pT_cut)
			outfilepath_up = os.path.join(base_inpath, outfilename_up)
			outfilename_down = "{}_sel3_pTH{}_SYST1DOWN.root".format(process, pT_cut)
			outfilepath_down = os.path.join(base_inpath, outfilename_down)
			rdf = get_rdf(infilepath)

			if not rdf:
				continue

			rdf_up = (rdf.Define("SF_up_lead_lep1", "GetEfficiencyScaleFactorUp(leading_pair_lep1_pt)")
					.Define("SF_up_lead_lep2", "GetEfficiencyScaleFactorUp(leading_pair_lep2_pt)")
					.Define("SF_up_sublead_lep1", "GetEfficiencyScaleFactorUp(subleading_pair_lep1_pt)")
					.Define("SF_up_sublead_lep2", "GetEfficiencyScaleFactorUp(subleading_pair_lep2_pt)")
					.Define("SF_up_muons", "SF_up_lead_lep1*SF_up_lead_lep2*SF_up_sublead_lep1*SF_up_sublead_lep2")
				)

			rdf_up.Snapshot("events", outfilepath_up, ["SF_up_muons", "SF_up_lead_lep1", "SF_up_lead_lep2", "SF_up_sublead_lep1", "SF_up_sublead_lep2", "leading_pair_lep1_pt", "leading_pair_lep2_pt", "subleading_pair_lep1_pt", "subleading_pair_lep2_pt", "m_llll"])
			
			hist_base_name = "{}_pTH{}_hist_".format(process, pT_cut)
			plot_histo(rdf_up, "SF_up_muons", base_plotpath, hist_base_name+"SF_up_muons")
			plot_histo(rdf_up, "SF_up_lead_lep1", base_plotpath, hist_base_name+"SF_up_lead_lep1")
			plot_histo(rdf_up, "SF_up_lead_lep2", base_plotpath, hist_base_name+"SF_up_lead_lep2")
			plot_histo(rdf_up, "SF_up_sublead_lep1", base_plotpath, hist_base_name+"SF_up_sublead_lep1")
			plot_histo(rdf_up, "SF_up_sublead_lep2", base_plotpath, hist_base_name+"SF_up_sublead_lep2")

			#same for down
			rdf_down = (rdf.Define("SF_down_lead_lep1", "GetEfficiencyScaleFactorDown(leading_pair_lep1_pt)")
					.Define("SF_down_lead_lep2", "GetEfficiencyScaleFactorDown(leading_pair_lep2_pt)")
					.Define("SF_down_sublead_lep1", "GetEfficiencyScaleFactorDown(subleading_pair_lep1_pt)")
					.Define("SF_down_sublead_lep2", "GetEfficiencyScaleFactorDown(subleading_pair_lep2_pt)")
					.Define("SF_down_muons", "SF_down_lead_lep1*SF_down_lead_lep2*SF_down_sublead_lep1*SF_down_sublead_lep2")
				)

			rdf_down.Snapshot("events", outfilepath_down, ["SF_down_muons", "SF_down_lead_lep1", "SF_down_lead_lep2", "SF_down_sublead_lep1", "SF_down_sublead_lep2", "leading_pair_lep1_pt", "leading_pair_lep2_pt", "subleading_pair_lep1_pt", "subleading_pair_lep2_pt", "m_llll"])
			
			hist_base_name = "{}_pTH{}_hist_".format(process, pT_cut)
			plot_histo(rdf_down, "SF_down_muons", base_plotpath, hist_base_name+"SF_down_muons")
			plot_histo(rdf_down, "SF_down_lead_lep1", base_plotpath, hist_base_name+"SF_down_lead_lep1")
			plot_histo(rdf_down, "SF_down_lead_lep2", base_plotpath, hist_base_name+"SF_down_lead_lep2")
			plot_histo(rdf_down, "SF_down_sublead_lep1", base_plotpath, hist_base_name+"SF_down_sublead_lep1")
			plot_histo(rdf_down, "SF_down_sublead_lep2", base_plotpath, hist_base_name+"SF_down_sublead_lep2")

			#fill the histogram of the observable with the new SF and divide by nominal 
			hist_m_4mu_model = ROOT.RDF.TH1DModel("m_4mu_fitrange","m_4mu_fitrange", 30, 110., 140.)
			hist_m_4mu_nom = rdf.Histo1D(hist_m_4mu_model, "m_llll")
			hist_m_4mu_up = rdf_up.Histo1D(hist_m_4mu_model, "m_llll", "SF_up_muons")
			hist_m_4mu_down = rdf_down.Histo1D(hist_m_4mu_model, "m_llll", "SF_down_muons")

			#add to totals:
			if not total_hist_nom:
				total_hist_nom = copy.deepcopy(hist_m_4mu_nom.GetValue())
				total_hist_nom.SetTitle("total_hist_nom")
				total_hist_nom.SetName("total_hist_nom")

			else:
				total_hist_nom.Add(hist_m_4mu_nom.GetValue())
			
			if not total_hist_up:
				total_hist_up = copy.deepcopy(hist_m_4mu_up.GetValue())
				total_hist_up.SetTitle("total_hist_up")
				total_hist_up.SetName("total_hist_up")

			else:
				total_hist_up.Add(hist_m_4mu_up.GetValue())
			
			if not total_hist_down:
				total_hist_down = copy.deepcopy(hist_m_4mu_down.GetValue())
				total_hist_down.SetTitle("total_hist_down")
				total_hist_down.SetName("total_hist_down")

			else:
				total_hist_down.Add(hist_m_4mu_down.GetValue())

		#calculate: 
		nominal_yield = total_hist_nom.Integral()
		up_yield = total_hist_up.Integral()
		down_yield = total_hist_down.Integral()
		syst_var_up = up_yield/nominal_yield
		syst_var_down = down_yield/nominal_yield
		print("Nominal yield: {:.2f}".format(nominal_yield))
		print("Up syst yield: {:.2f}".format(up_yield))
		print("Down syst yield: {:.2f}".format(down_yield))
		print("Up systematic variation: {:.6f}".format(syst_var_up))
		print("Down systematic variation: {:.6f}".format(syst_var_down))

		#plot everything
		plot_syst_hist_compare(total_hist_nom, total_hist_up, total_hist_down, "hists_m_4mu_pT{}".format(pT_cut), base_plotpath)

		dict_SF_vs_pT[pT_cut] = syst_var_up
	
	return dict_SF_vs_pT

def get_SF_for_excl_pT_bins(processes, base_inpath, base_plotpath, pT_step = 50, pT_range_min= 50, pT_range_max=550):
	# loop over all pT minimum cuts, and make a list of SF
	dict_SF_vs_pT = {}

	for pT_cut_min in range(pT_range_min, pT_range_max, pT_step):
		pT_cut_max = pT_cut_min+pT_step
		pT_bin_identifier = "pTH{}_{}".format(pT_cut_min, pT_cut_max)
		print("Getting Scalefactors for pT bin = ", pT_cut_min, "to",pT_cut_max )

		#histogram templates for totals to fill:
		total_hist_nom = None
		total_hist_up = None
		total_hist_down = None

		for process in processes:
			print("Processing sample: ", process)
		
			infilename = "{}_sel3_pTH{}_{}.root".format(process, pT_cut_min, pT_cut_max)
			infilepath = os.path.join(base_inpath, infilename)
			outfilename_up = "{}_sel3_pTH{}_{}_SYST1UP.root".format(process, pT_cut_min, pT_cut_max)
			outfilepath_up = os.path.join(base_inpath, outfilename_up)
			outfilename_down = "{}_sel3_pTH{}_{}_SYST1DOWN.root".format(process, pT_cut_min, pT_cut_max)
			outfilepath_down = os.path.join(base_inpath, outfilename_down)
			rdf = get_rdf(infilepath)

			if not rdf:
				continue

			rdf_up = (rdf.Define("SF_up_lead_lep1", "GetEfficiencyScaleFactorUp(leading_pair_lep1_pt)")
					.Define("SF_up_lead_lep2", "GetEfficiencyScaleFactorUp(leading_pair_lep2_pt)")
					.Define("SF_up_sublead_lep1", "GetEfficiencyScaleFactorUp(subleading_pair_lep1_pt)")
					.Define("SF_up_sublead_lep2", "GetEfficiencyScaleFactorUp(subleading_pair_lep2_pt)")
					.Define("SF_up_muons", "SF_up_lead_lep1*SF_up_lead_lep2*SF_up_sublead_lep1*SF_up_sublead_lep2")
				)

			rdf_up.Snapshot("events", outfilepath_up, ["SF_up_muons", "SF_up_lead_lep1", "SF_up_lead_lep2", "SF_up_sublead_lep1", "SF_up_sublead_lep2", "leading_pair_lep1_pt", "leading_pair_lep2_pt", "subleading_pair_lep1_pt", "subleading_pair_lep2_pt", "m_llll"])
			
			hist_base_name = "{}_pTH{}_{}_hist_up".format(process, pT_cut_min, pT_cut_max)
			plot_histo(rdf_up, "SF_up_muons", base_plotpath, hist_base_name+"SF_up_muons")
			plot_histo(rdf_up, "SF_up_lead_lep1", base_plotpath, hist_base_name+"SF_up_lead_lep1")
			plot_histo(rdf_up, "SF_up_lead_lep2", base_plotpath, hist_base_name+"SF_up_lead_lep2")
			plot_histo(rdf_up, "SF_up_sublead_lep1", base_plotpath, hist_base_name+"SF_up_sublead_lep1")
			plot_histo(rdf_up, "SF_up_sublead_lep2", base_plotpath, hist_base_name+"SF_up_sublead_lep2")

			#same for down
			rdf_down = (rdf.Define("SF_down_lead_lep1", "GetEfficiencyScaleFactorDown(leading_pair_lep1_pt)")
					.Define("SF_down_lead_lep2", "GetEfficiencyScaleFactorDown(leading_pair_lep2_pt)")
					.Define("SF_down_sublead_lep1", "GetEfficiencyScaleFactorDown(subleading_pair_lep1_pt)")
					.Define("SF_down_sublead_lep2", "GetEfficiencyScaleFactorDown(subleading_pair_lep2_pt)")
					.Define("SF_down_muons", "SF_down_lead_lep1*SF_down_lead_lep2*SF_down_sublead_lep1*SF_down_sublead_lep2")
				)

			rdf_down.Snapshot("events", outfilepath_down, ["SF_down_muons", "SF_down_lead_lep1", "SF_down_lead_lep2", "SF_down_sublead_lep1", "SF_down_sublead_lep2", "leading_pair_lep1_pt", "leading_pair_lep2_pt", "subleading_pair_lep1_pt", "subleading_pair_lep2_pt", "m_llll"])
			
			hist_base_name = "{}_pTH{}_{}_hist_down".format(process, pT_cut_min, pT_cut_max)
			plot_histo(rdf_down, "SF_down_muons", base_plotpath, hist_base_name+"SF_down_muons")
			plot_histo(rdf_down, "SF_down_lead_lep1", base_plotpath, hist_base_name+"SF_down_lead_lep1")
			plot_histo(rdf_down, "SF_down_lead_lep2", base_plotpath, hist_base_name+"SF_down_lead_lep2")
			plot_histo(rdf_down, "SF_down_sublead_lep1", base_plotpath, hist_base_name+"SF_down_sublead_lep1")
			plot_histo(rdf_down, "SF_down_sublead_lep2", base_plotpath, hist_base_name+"SF_down_sublead_lep2")

			#fill the histogram of the observable with the new SF and divide by nominal 
			hist_m_4mu_model = ROOT.RDF.TH1DModel("m_4mu_fitrange","m_4mu_fitrange", 30, 110., 140.)
			hist_m_4mu_nom = rdf.Histo1D(hist_m_4mu_model, "m_llll")
			hist_m_4mu_up = rdf_up.Histo1D(hist_m_4mu_model, "m_llll", "SF_up_muons")
			hist_m_4mu_down = rdf_down.Histo1D(hist_m_4mu_model, "m_llll", "SF_down_muons")

			#add to totals:
			if not total_hist_nom:
				total_hist_nom = copy.deepcopy(hist_m_4mu_nom.GetValue())
				total_hist_nom.SetTitle("total_hist_nom")
				total_hist_nom.SetName("total_hist_nom")

			else:
				total_hist_nom.Add(hist_m_4mu_nom.GetValue())
			
			if not total_hist_up:
				total_hist_up = copy.deepcopy(hist_m_4mu_up.GetValue())
				total_hist_up.SetTitle("total_hist_up")
				total_hist_up.SetName("total_hist_up")

			else:
				total_hist_up.Add(hist_m_4mu_up.GetValue())
			
			if not total_hist_down:
				total_hist_down = copy.deepcopy(hist_m_4mu_down.GetValue())
				total_hist_down.SetTitle("total_hist_down")
				total_hist_down.SetName("total_hist_down")

			else:
				total_hist_down.Add(hist_m_4mu_down.GetValue())

		#calculate: 
		nominal_yield = total_hist_nom.Integral()
		up_yield = total_hist_up.Integral()
		down_yield = total_hist_down.Integral()
		syst_var_up = up_yield/nominal_yield
		syst_var_down = down_yield/nominal_yield
		print("Nominal yield: {:.2f}".format(nominal_yield))
		print("Up syst yield: {:.2f}".format(up_yield))
		print("Down syst yield: {:.2f}".format(down_yield))
		print("Up systematic variation: {:.6f}".format(syst_var_up))
		print("Down systematic variation: {:.6f}".format(syst_var_down))

		#plot everything
		plot_syst_hist_compare(total_hist_nom, total_hist_up, total_hist_down, "hists_m_4mu_pT{}".format(pT_bin_identifier), base_plotpath)
		dict_SF_vs_pT[pT_bin_identifier] = syst_var_up
	
	return dict_SF_vs_pT

# #_____________________________________________________________________________________________________
# def efficiency_uncertainty_function(pt):
#     return 0.25*np.sqrt(2500./pt**2 + 25./pt + 1.)

# #_____________________________________________________________________________________________________

if __name__ == "__main__":
	#plot and check first
	# test_unc_fct() 

	parser = ArgumentParser()
	parser.add_argument('--energy', default='100TeV', help='Energy point to run at. Options: 100TeV (default), 84TeV, 72TeV')
	parser.add_argument('--prodTag', default='fcc_v07', help='Production tag to run with. Options: fcc_v07 (default), fcc_v06')
	parser.add_argument('--detector', default='II', help='Detector scenario to run with. Options: I, II (default)')
	parser.add_argument('-o,' '--output', default='/eos/user/b/bistapf/plots_H4mu_eff_SF/', dest="output", help='Base name for the output directory')
	parser.add_argument('--doExclBins', action='store_true', help="Use exclusive pT bins (rather than min pT cuts) for the inputs to simultaneous fit.")
	args = parser.parse_args()

	#input and output dirs
	base_inpath = "/eos/experiment/fcc/hh/analysis_ntuples/{}/{}/H4l_analysis/{}/final/".format( args.prodTag, args.detector, args.energy)
	print(base_inpath)

	base_outpath = base_inpath
	base_plotpath = os.path.join(args.output, args.energy)

	if args.doExclBins:
		base_plotpath += "_exclPTBins"

	if not os.path.exists(base_plotpath):
		os.mkdir(base_plotpath)

	if args.energy == "100TeV":
		processes = [
						"mgp8_pp_h012j_5f_hllll", #SIGNAL
						"mgp8_pp_vbf_h01j_5f_hllll",
						"mgp8_pp_tth01j_5f_hllll",
						"mgp8_pp_vh012j_5f_hllll",
					]
	elif args.energy == "84TeV" or args.energy == "72TeV" or args.energy == "120TeV":
		processes = [
						"mgp8_pp_h012j_5f_{}_hllll".format(args.energy), #SIGNAL
						"mgp8_pp_vbf_h01j_5f_{}_hllll".format(args.energy),
						"mgp8_pp_tth01j_5f_{}_hllll".format(args.energy),
						"mgp8_pp_vh012j_5f_{}_hllll".format(args.energy),
					]
	else:
		raise Exception("Unsupported energy option! Choose from 100TeV, 84TeV, 72TeV or 120TeV!")
	dict_of_SFs = {}

	if args.doExclBins:
		dict_SF_vs_pT = get_SF_for_excl_pT_bins(processes, base_inpath, base_plotpath)
	else:
		dict_SF_vs_pT = get_SF_for_min_pT_cuts(processes, base_inpath, base_plotpath)

	dict_of_SFs["H4mu_signal_{}".format(args.energy)] = dict_SF_vs_pT
	plot_scalefactors("H4mu_signal_merged", dict_SF_vs_pT, base_plotpath)
	
	print(dict_of_SFs)
	
	json_filepath = "/afs/cern.ch/user/b/bistapf/combine_EL9/H4mu_analysis/"
	json_filename = "SF_eff_vs_pT_{}_scen{}_merged".format(args.energy, args.detector)
	if args.doExclBins:
		json_filename+="_exclPTbins"
	json_filepath = os.path.join(json_filepath, json_filename+".json")
	print("Writing file:", json_filepath)
	with open(json_filepath, 'w') as json_file:
		json.dump(dict_of_SFs, json_file)

   
   
	# #plot the total SF as a check:
	# hist_SF_muons = rdf.Histo1D("SF_muons")
	# hist_SF_muplus = rdf.Histo1D("SF_muplus")
	# hist_SF_muminus = rdf.Histo1D("SF_muminus")

	# #setup canvas
	# canvas = ROOT.TCanvas("canvas", "canvas", 800, 800) 
	# canvas.cd()
	# hist_SF_muons.Draw()
	# canvas.SaveAs("./hist_SF_muons.png")

	# canvas.Clear()
	# hist_SF_muplus.Draw()
	# canvas.SaveAs("./hist_SF_muplus.png")\

	# canvas.Clear()
	# hist_SF_muminus.Draw()
	# canvas.SaveAs("./hist_SF_muminus.png")

	# #fill the histogram of the observable with the new SF and divide by nominal 
	# hist_m_mumu_model = ROOT.RDF.TH1DModel("m_mumu_1bin","m_mumu_1bin", 1, 124., 126.)
	# hist_m_mumu_nom = rdf.Histo1D(hist_m_mumu_model, "m_mumu")
	# hist_m_mumu_up = rdf.Histo1D(hist_m_mumu_model, "m_mumu", "SF_muons")

	# #calculate: 
	# nominal_yield = hist_m_mumu_nom.GetValue().Integral()
	# up_yield = hist_m_mumu_up.GetValue().Integral()
	# syst_var_up = up_yield/nominal_yield
	# print("Nominal yield: {:.2f}".format(nominal_yield))
	# print("Up syst yield: {:.2f}".format(up_yield))
	# print("Up systematic variation: {:.2f}".format(syst_var_up))
	# print("Integral of SF histogram:", hist_SF_muons.GetValue().Integral())
	# print("Sum of SF column weight:", rdf.Sum("SF_muons").GetValue())
	