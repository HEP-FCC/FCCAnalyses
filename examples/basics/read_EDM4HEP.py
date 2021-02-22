#This is a basic example showing how to read different objects like electrons, jets, ETmiss etc. from the EDM4HEP files 
# and how to access and store some simple variables in an output ntuple


import ROOT
import os
import argparse


### TODO: see if can be simplified/improved #####
#setup of the libraries, following the example:
print ("Load cxx analyzers ... ",)
ROOT.gSystem.Load("libedm4hep")
ROOT.gSystem.Load("libpodio")
ROOT.gSystem.Load("libFCCAnalyses")
ROOT.gErrorIgnoreLevel = ROOT.kFatal
_edm  = ROOT.edm4hep.ReconstructedParticleData()
_pod  = ROOT.podio.ObjectID()
_fcc  = ROOT.getMC_px

print ('edm4hep  ',_edm)
print ('podio    ',_pod)
print ('fccana   ',_fcc)

print ('Finished loading analyzers. Ready to go.')


#The analysis class handles which variables are defined and written to the output ntuple
class analysis():
	#__________________________________________________________
	def __init__(self, inputlist, outname, ncpu):
		self.outname = outname

		if ".root" not in outname:
			self.outname+=".root"

		ROOT.ROOT.EnableImplicitMT(ncpu)

		self.df = ROOT.RDataFrame("events", inputlist)

	#__________________________________________________________
	def run(self):

		df2 = (self.df
		
		#JETS:
		#TODO: count all jets in the event
		.Define("selected_jets", "selRP_pT(50.)(Jet)") 
		.Define("jet_pT",        "getRP_pt(Jet)")
		.Define("seljet_pT",     "getRP_pt(selected_jets)")
	
		
		#ELECTRONS
		#TODO: clean up 
		.Alias("Electron0", "Electron#0.index")
		# define the electron collection : TODO ADD EXPLANATION,
		.Define("electrons",  "getRP(Electron0, ReconstructedParticles)") 
		.Define("n_electrons",  "getRP_n(electrons)")
		.Define("pT_electrons",  "getRP_pt(electrons)")
		#select electrons with pT > 20 GeV
		.Define("selected_electrons", "selRP_pT(20.)(electrons)")
		# .Define("n_electrons_sel", "getRP_n(selected_electrons)")
		.Define("n_electrons_sel", "return selected_electrons.size()") #why does this not work?
		.Define("pT_electrons_sel",  "getRP_pt(selected_electrons)")

		#MUONS
		#TODO: clean up 
		# define an alias for muon index collection #why is this needed?
		.Alias("Muon0", "Muon#0.index")
		# define the muon collection
		.Define("muons",  "getRP(Muon0, ReconstructedParticles)") #dont get it
		.Define("n_muons",  "getRP_n(muons)")
		.Define("pT_muons",  "getRP_pt(muons)")
		#select electrons with pT > 20 GeV
		.Define("selected_muons", "selRP_pT(20.)(muons)")
		.Define("n_muons_sel", "getRP_n(selected_muons)")
		# .Define("n_electrons_sel", "return selected_electrons.size()") #why does this not work?
		.Define("pT_muons_sel",  "getRP_pt(selected_muons)")

		#LEPTONS:
		.Define("n_leps",  "getRP_n(muons)+getRP_n(electrons)")
		.Define("n_leps_sel",  "getRP_n(selected_muons)+getRP_n(selected_electrons)")


		#MISSING TRANSVERSE ENERGY
		.Define("MET", "getRP_pt(MissingET)")
		)

		# select branches for output file
		branchList = ROOT.vector('string')()
		for branchName in [
						"n_electrons",
						"n_electrons_sel",
						"pT_electrons",
						"pT_electrons_sel",
						"n_muons",
						"n_muons_sel",
						"pT_muons",
						"pT_muons_sel",
						"n_leps",
						"n_leps_sel",
						"MET",
						]:
			branchList.push_back(branchName)
		df2.Snapshot("events", self.outname, branchList)

if __name__ == "__main__":

	#TODO: UPDATE AND ADD A TESTER FILE TO THE REPO SOMEHOW? 
	default_input_tester = "/eos/experiment/fcc/hh/generation/DelphesEvents/fcc_v04/pwp8_pp_hh_lambda100_5f_hhbbzz_zleptonic/events_000087952.root"
	default_out_dir = "./"

	#parse input arguments:
	parser = argparse.ArgumentParser(description="Basic example how to access objects and simple variables with FCCAnalyses.")
	parser.add_argument('--input', '-i', metavar="INPUTFILE", dest="input_file", default=default_input_tester, help="Path to the input file. If not specified, runs over a default tester file.")
	parser.add_argument('--output', '-o', metavar="OUTPUTDIR", dest="out_dir", default=default_out_dir, help="Output directory. If not specified, sets to current directory.")
	args = parser.parse_args()

	#create the output dir, if it doesnt exist yet:
	if not os.path.exists(args.out_dir):
		os.mkdir(args.out_dir)

	#build the name/path of the output file:
	output_file = os.path.join(args.out_dir, args.input_file.split("/")[-1])

	#TODO: CLEAN UP
	#now run:
	print("##### Running basic example analysis #####")
	print("Input file: ", args.input_file)
	print("Output file: ", output_file)

	ncpus = 1
	analysis = analysis(args.input_file, output_file, ncpus)
	analysis.run()


