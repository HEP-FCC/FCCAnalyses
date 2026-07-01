#Derive the uncertainty systematics, depending on the pT of the muon

import ROOT
import numpy as np
import matplotlib.pyplot as plt
import os
import json
from argparse import ArgumentParser

ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0)


# To work with RDF, need to compile the RDF function in C
ROOT.gInterpreter.Declare(
"""
using namespace ROOT;
float GetEfficiencyScaleFactorUp(float pt) {
	return 1.+2.*(0.25*sqrt(2500./pow(pt, 2) + 25./pt + 1.))/100.;
}
""")

ROOT.gInterpreter.Declare(
"""
using namespace ROOT;
float GetEfficiencyScaleFactorDown(float pt) {
	return 1.-2.*(0.25*sqrt(2500./pow(pt, 2) + 25./pt + 1.))/100.;
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

def plot_scalefactors(process_name, SF_vs_pT_dict, plotdir, obj_type):
	out_path = os.path.join(plotdir, "EffScaleFactor_vs_pT_for_{}.png".format(process))
	
	x = list(SF_vs_pT_dict.keys())
	y = list(SF_vs_pT_dict.values())

	# Plotting
	plt.figure(figsize=(10, 6))
	plt.plot(x, y, marker='o')  # 'o' adds markers to the data points
	plt.title('{} reconstruction efficiencies'.format(obj_type))
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
		
			infilename = "{}_sel3_pTH{}.root".format(process, pT_cut)
			infilepath = os.path.join(base_inpath, infilename)
			outfilename_up = "{}_sel3_pTH{}_SYST1UP.root".format(process, pT_cut)
			outfilepath_up = os.path.join(base_inpath, outfilename_up)
			outfilename_down = "{}_sel3_pTH{}_SYST1DOWN.root".format(process, pT_cut)
			outfilepath_down = os.path.join(base_inpath, outfilename_down)
			rdf = get_rdf(infilepath)

			if not rdf:
				continue

			rdf_up = (rdf.Define("SF_up_muplus", "GetEfficiencyScaleFactorUp(mu_plus_pt[0])")
					.Define("SF_up_muminus", "GetEfficiencyScaleFactorUp(mu_minus_pt[0])")
					.Define("SF_up_muons", "SF_up_muplus*SF_up_muminus")
				)

			rdf_up.Snapshot("events", outfilepath_up, ["SF_up_muons", "SF_up_muplus", "SF_up_muminus", "mu_plus_pt", "mu_minus_pt", "m_mumu"])
			
			hist_base_name = "{}_pTH{}_hist_".format(process, pT_cut)
			plot_histo(rdf_up, "SF_up_muons", base_plotpath, hist_base_name+"SF_up_muons")
			plot_histo(rdf_up, "SF_up_muplus", base_plotpath, hist_base_name+"SF_up_muplus")
			plot_histo(rdf_up, "SF_up_muminus", base_plotpath, hist_base_name+"SF_up_muminus")

			#same for down
			rdf_down = (rdf.Define("SF_down_muplus", "GetEfficiencyScaleFactorDown(mu_plus_pt[0])")
					.Define("SF_down_muminus", "GetEfficiencyScaleFactorDown(mu_minus_pt[0])")
					.Define("SF_down_muons", "SF_down_muplus*SF_down_muminus")
				)

			rdf_down.Snapshot("events", outfilename_down, ["SF_down_muons", "SF_down_muplus", "SF_down_muminus", "mu_plus_pt", "mu_minus_pt", "m_mumu"])
			
			hist_base_name = "{}_pTH{}_hist_".format(process, pT_cut)
			plot_histo(rdf_down, "SF_down_muons", base_plotpath, hist_base_name+"SF_down_muons")
			plot_histo(rdf_down, "SF_down_muplus", base_plotpath, hist_base_name+"SF_down_muplus")
			plot_histo(rdf_down, "SF_down_muminus", base_plotpath, hist_base_name+"SF_down_muminus")

			#fill the histogram of the observable with the new SF and divide by nominal 
			hist_m_mumu_model = ROOT.RDF.TH1DModel("m_mumu_zoom","m_mumu_zoom", 100, 120., 130.)
			hist_m_mumu_nom = rdf.Histo1D(hist_m_mumu_model, "m_mumu")
			hist_m_mumu_up = rdf_up.Histo1D(hist_m_mumu_model, "m_mumu", "SF_up_muons")
			hist_m_mumu_down = rdf_down.Histo1D(hist_m_mumu_model, "m_mumu", "SF_down_muons")

			#calculate: 
			nominal_yield = hist_m_mumu_nom.GetValue().Integral()
			up_yield = hist_m_mumu_up.GetValue().Integral()
			down_yield = hist_m_mumu_down.GetValue().Integral()
			syst_var_up = up_yield/nominal_yield
			syst_var_down = down_yield/nominal_yield
			print("Nominal yield: {:.2f}".format(nominal_yield))
			print("Up syst yield: {:.2f}".format(up_yield))
			print("Down syst yield: {:.2f}".format(down_yield))
			print("Up systematic variation: {:.6f}".format(syst_var_up))
			print("Down systematic variation: {:.6f}".format(syst_var_down))

			#plot everything
			plot_syst_hist_compare(hist_m_mumu_nom.GetValue(), hist_m_mumu_up.GetValue(), hist_m_mumu_down.GetValue(), "hists_m_mumu_pT{}".format(pT_cut), base_plotpath)

			dict_SF_vs_pT[pT_cut] = syst_var_up
	
	return dict_SF_vs_pT

def get_SF_for_excl_pT_bins(process, base_inpath, base_outpath, base_plotpath, obj_type="photons"):
	# loop over all pT minimum cuts, and make a list of SF
	dict_SF_vs_pT = {}

	ttH_categories = [ 
		# Reco pT bins
		"pT_yy_bin1", 
		"pT_yy_bin2", 
		"pT_yy_bin3", 
		"pT_yy_bin4", 
		"pT_yy_bin5", 
		"pT_yy_bin6", 
		#Central
		#first truth pT bin
		"TTH_CEN_PTH_0_60_pT_yy_bin1",
		"TTH_CEN_PTH_0_60_pT_yy_bin2",
		"TTH_CEN_PTH_0_60_pT_yy_bin3",
		"TTH_CEN_PTH_0_60_pT_yy_bin4",
		"TTH_CEN_PTH_0_60_pT_yy_bin5",
		"TTH_CEN_PTH_0_60_pT_yy_bin6",
		#second truth pT bin
		"TTH_CEN_PTH_60_120_pT_yy_bin1",
		"TTH_CEN_PTH_60_120_pT_yy_bin2",
		"TTH_CEN_PTH_60_120_pT_yy_bin3",
		"TTH_CEN_PTH_60_120_pT_yy_bin4",
		"TTH_CEN_PTH_60_120_pT_yy_bin5",
		"TTH_CEN_PTH_60_120_pT_yy_bin6",
		#third truth pT bin
		"TTH_CEN_PTH_120_200_yy_bin1",
		"TTH_CEN_PTH_120_200_pT_yy_bin2",
		"TTH_CEN_PTH_120_200_pT_yy_bin3",
		"TTH_CEN_PTH_120_200_pT_yy_bin4",
		"TTH_CEN_PTH_120_200_pT_yy_bin5",
		"TTH_CEN_PTH_120_200_pT_yy_bin6",
		#fourth truth pT bin
		"TTH_CEN_PTH_200_300_pT_yy_bin1",
		"TTH_CEN_PTH_200_300_pT_yy_bin2",
		"TTH_CEN_PTH_200_300_pT_yy_bin3",
		"TTH_CEN_PTH_200_300_pT_yy_bin4",
		"TTH_CEN_PTH_200_300_pT_yy_bin5",
		"TTH_CEN_PTH_200_300_pT_yy_bin6",
		#fifth truth pT bin
		"TTH_CEN_PTH_300_450_pT_yy_bin1",
		"TTH_CEN_PTH_300_450_pT_yy_bin2",
		"TTH_CEN_PTH_300_450_pT_yy_bin3",
		"TTH_CEN_PTH_300_450_pT_yy_bin4",
		"TTH_CEN_PTH_300_450_pT_yy_bin5",
		"TTH_CEN_PTH_300_450_pT_yy_bin6",
		#sixth truth pT bin
		"TTH_CEN_PTH_450_inf_pT_yy_bin1",
		"TTH_CEN_PTH_450_inf_pT_yy_bin2",
		"TTH_CEN_PTH_450_inf_pT_yy_bin3",
		"TTH_CEN_PTH_450_inf_pT_yy_bin4",
		"TTH_CEN_PTH_450_inf_pT_yy_bin5",
		"TTH_CEN_PTH_450_inf_pT_yy_bin6",
		#Forward
		"TTH_FWD_pT_yy_bin1",
		"TTH_FWD_pT_yy_bin2",
		"TTH_FWD_pT_yy_bin3",
		"TTH_FWD_pT_yy_bin4",
		"TTH_FWD_pT_yy_bin5",
		"TTH_FWD_pT_yy_bin6",
	]

	for category in ttH_categories:
		print("Getting Scalefactors for category: ", category, "and object:", obj_type )
	
		infilename = "{}_{}.root".format(process, category)
		infilepath = os.path.join(base_inpath, infilename)
		outfilename_up = "{}_{}_{}_SYST1UP.root".format(process, category, obj_type)
		outfilepath_up = os.path.join(base_outpath, outfilename_up)
		outfilename_down = "{}_{}_{}_SYST1DOWN.root".format(process, category, obj_type)
		outfilepath_down = os.path.join(base_outpath, outfilename_down)
		rdf = get_rdf(infilepath)

		if not rdf:
			continue
		
		if obj_type == "photons":

			rdf_up = (rdf.Define("SF_up_y1", "GetEfficiencyScaleFactorUp(pT_y1)")
					.Define("SF_up_y2", "GetEfficiencyScaleFactorUp(pT_y2)")
					.Define("SF_up_photons", "SF_up_y1*SF_up_y2")
				)

			rdf_up.Snapshot("events", outfilepath_up, ["SF_up_photons", "SF_up_y1", "SF_up_y2", "pT_y1", "pT_y2", "m_yy"])
		
			hist_base_name = "{}_{}_{}_hist_up".format(process, category, obj_type)
			plot_histo(rdf_up, "SF_up_photons", base_plotpath, hist_base_name+"SF_up_photons")
			plot_histo(rdf_up, "SF_up_y1", base_plotpath, hist_base_name+"SF_up_y1")
			plot_histo(rdf_up, "SF_up_y2", base_plotpath, hist_base_name+"SF_up_y2")

			#same for down
			rdf_down = (rdf.Define("SF_down_y1", "GetEfficiencyScaleFactorDown(pT_y1)")
					.Define("SF_down_y2", "GetEfficiencyScaleFactorDown(pT_y2)")
					.Define("SF_down_photons", "SF_down_y1*SF_down_y2")
				)

			rdf_down.Snapshot("events", outfilepath_down, ["SF_down_photons", "SF_down_y1", "SF_down_y2", "pT_y1", "pT_y2", "m_yy"])
		
			hist_base_name = "{}_{}_{}_hist_down".format(process, category, obj_type)
			plot_histo(rdf_down, "SF_down_photons", base_plotpath, hist_base_name+"SF_down_photons")
			plot_histo(rdf_down, "SF_down_y1", base_plotpath, hist_base_name+"SF_down_y1")
			plot_histo(rdf_down, "SF_down_y2", base_plotpath, hist_base_name+"SF_down_y2")

			#fill the histogram of the observable with the new SF and divide by nominal 
			hist_m_yy_model = ROOT.RDF.TH1DModel("m_yy_fitrange","m_yy_fitrange", 30, 110., 140.)
			hist_m_yy_nom = rdf.Histo1D(hist_m_yy_model, "m_yy")
			hist_m_yy_up = rdf_up.Histo1D(hist_m_yy_model, "m_yy", "SF_up_photons")
			hist_m_yy_down = rdf_down.Histo1D(hist_m_yy_model, "m_yy", "SF_down_photons")

			#calculate: 
			nominal_yield = hist_m_yy_nom.GetValue().Integral()
			up_yield = hist_m_yy_up.GetValue().Integral()
			down_yield = hist_m_yy_down.GetValue().Integral()
			syst_var_up = up_yield/nominal_yield
			syst_var_down = down_yield/nominal_yield
			print("Nominal yield: {:.2f}".format(nominal_yield))
			print("Up syst yield: {:.2f}".format(up_yield))
			print("Down syst yield: {:.2f}".format(down_yield))
			print("Up systematic variation: {:.6f}".format(syst_var_up))
			print("Down systematic variation: {:.6f}".format(syst_var_down))

			#plot everything
			plot_syst_hist_compare(hist_m_yy_nom.GetValue(), hist_m_yy_up.GetValue(), hist_m_yy_down.GetValue(), "hists_m_yy_{}_{}_{}".format(process, category, obj_type), base_plotpath)

		elif obj_type == "bjets":

			rdf_up = (rdf.Define("SF_up_b1", "GetEfficiencyScaleFactorUp(pT_b1)")
					.Define("SF_up_b2", "GetEfficiencyScaleFactorUp(pT_b2)")
					.Define("SF_up_bjets", "SF_up_b1*SF_up_b2")
				)

			rdf_up.Snapshot("events", outfilepath_up, ["SF_up_bjets", "SF_up_b1", "SF_up_b2", "pT_b1", "pT_b2", "m_yy"])
		
			hist_base_name = "{}_{}_{}_hist_up".format(process, category, obj_type)
			plot_histo(rdf_up, "SF_up_bjets", base_plotpath, hist_base_name+"SF_up_bjets")
			plot_histo(rdf_up, "SF_up_b1", base_plotpath, hist_base_name+"SF_up_b1")
			plot_histo(rdf_up, "SF_up_b2", base_plotpath, hist_base_name+"SF_up_b2")

			#same for down
			rdf_down = (rdf.Define("SF_down_b1", "GetEfficiencyScaleFactorDown(pT_b1)")
					.Define("SF_down_b2", "GetEfficiencyScaleFactorDown(pT_b2)")
					.Define("SF_down_bjets", "SF_down_b1*SF_down_b2")
				)

			rdf_down.Snapshot("events", outfilepath_down, ["SF_down_bjets", "SF_down_b1", "SF_down_b2", "pT_b1", "pT_b2", "m_yy"])
		
			hist_base_name = "{}_{}_{}_hist_down".format(process, category, obj_type)
			plot_histo(rdf_down, "SF_down_bjets", base_plotpath, hist_base_name+"SF_down_bjets")
			plot_histo(rdf_down, "SF_down_b1", base_plotpath, hist_base_name+"SF_down_b1")
			plot_histo(rdf_down, "SF_down_b2", base_plotpath, hist_base_name+"SF_down_b2")

			#fill the histogram of the observable with the new SF and divide by nominal 
			hist_m_yy_model = ROOT.RDF.TH1DModel("m_yy_fitrange","m_yy_fitrange", 30, 110., 140.)
			hist_m_yy_nom = rdf.Histo1D(hist_m_yy_model, "m_yy")
			hist_m_yy_up = rdf_up.Histo1D(hist_m_yy_model, "m_yy", "SF_up_bjets")
			hist_m_yy_down = rdf_down.Histo1D(hist_m_yy_model, "m_yy", "SF_down_bjets")

			#calculate: 
			nominal_yield = hist_m_yy_nom.GetValue().Integral()
			up_yield = hist_m_yy_up.GetValue().Integral()
			down_yield = hist_m_yy_down.GetValue().Integral()
			syst_var_up = up_yield/nominal_yield
			syst_var_down = down_yield/nominal_yield
			print("Nominal yield: {:.2f}".format(nominal_yield))
			print("Up syst yield: {:.2f}".format(up_yield))
			print("Down syst yield: {:.2f}".format(down_yield))
			print("Up systematic variation: {:.6f}".format(syst_var_up))
			print("Down systematic variation: {:.6f}".format(syst_var_down))

			#plot everything
			plot_syst_hist_compare(hist_m_yy_nom.GetValue(), hist_m_yy_up.GetValue(), hist_m_yy_down.GetValue(), "hists_m_yy_{}_{}_{}".format(process, category, obj_type), base_plotpath)

		else:
			raise Exception("ERROR! Unrecognised object type. Only supporting photons or bjets.")

		dict_SF_vs_pT[category] = syst_var_up
	
	return dict_SF_vs_pT

# #_____________________________________________________________________________________________________
# def efficiency_uncertainty_function(pt):
#     return 0.25*np.sqrt(2500./pt**2 + 25./pt + 1.)

# #_____________________________________________________________________________________________________

if __name__ == "__main__":
	#plot and check first
	# test_unc_fct() 

	parser = ArgumentParser()
	parser.add_argument('--energy', default='84TeV', help='Energy point to run at. Options: 84TeV (default)')
	parser.add_argument('--prodTag', default='fcc_v07', help='Production tag to run with. Options: fcc_v07 (default), fcc_v06')
	parser.add_argument('--detector', default='II', help='Detector scenario to run with. Options: I, II (default)')
	parser.add_argument('-o,' '--output', default='plots_Hyy_scalefactors', dest="output", help='Base name for the output directory')
	parser.add_argument('--type', dest="obj_type", default='photons', help='Whether to run for photons or b-jets.')
	args = parser.parse_args()

	#input and output dirs
	base_inpath = "/eos/user/e/elmazzeo/ttH@FCC-hh/results/2025-03-14/categories/"
	base_outpath = "/eos/experiment/fcc/hh/analysis_ntuples/ttHyy_effSyst/"
	base_plotpath = args.output

	if not os.path.exists(base_plotpath):
		os.mkdir(base_plotpath)

	processes = [
					"mgp8_pp_tth01j_5f_{}_haaexcl".format(args.energy), #SIGNAL
				
				]
	dict_of_SFs = {}

	for process in processes:
		print("Processing sample: ", process)

		dict_SF_vs_pT = get_SF_for_excl_pT_bins(process, base_inpath, base_outpath, base_plotpath, obj_type =args.obj_type)

		dict_of_SFs[process] = dict_SF_vs_pT
		plot_scalefactors(process, dict_SF_vs_pT, base_plotpath, args.obj_type)
	
	print(dict_of_SFs)
	
	json_filename = "{}_SF_eff_vs_pT_{}".format(args.obj_type, args.energy)
	json_filepath = os.path.join(base_outpath, json_filename+".json")
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
	