#This is a basic example showing how to read different objects like electrons, jets, ETmiss etc. from the EDM4HEP files
# and how to access and store some simple variables in an output ntuple

# Mandatory: RDFanalysis class where the user defines the operations on the TTree
class RDFanalysis():
    #__________________________________________________________
    # Mandatory: analysers function to define the analysers to process, please make sure you return the last dataframe, in this example it is df2
    def analysers(df):
        df2 = (df
				#Access the various objects and their properties with the following syntax: .Define("<your_variable>", "<accessor_fct (name_object)>")
				#This will create a column in the RDataFrame named <your_variable> and filled with the return value of the <accessor_fct> for the given collection/object
				#Accessor functions are the functions found in the C++ analyzers code that return a certain variable, e.g. <namespace>::get_n(object) returns the number
				#of these objects in the event and <namespace>::get_pt(object) returns the pT of the object. Here you can pick between two namespaces to access either
				#reconstructed (namespace = ReconstructedParticle) or MC-level objects (namespace = MCParticle).
				#For the name of the object, in principle the names of the EDM4HEP collections are used - photons, muons and electrons are an exception, see below

				#OVERVIEW: Accessing different objects and counting them
				#JETS
				.Define("n_jets", "ReconstructedParticle::get_n(Jet)") #count how many jets are in the event in total

				#PHOTONS
				.Alias("Photon0", "Photon#0.index")
				.Define("photons",  "ReconstructedParticle::get(Photon0, ReconstructedParticles)")
				.Define("n_photons",  "ReconstructedParticle::get_n(photons)") #count how many photons are in the event in total

				#ELECTRONS AND MUONS
				#TODO: ADD EXPLANATION OF THE EXTRA STEPS
				.Alias("Electron0", "Electron#0.index")
				.Define("electrons",  "ReconstructedParticle::get(Electron0, ReconstructedParticles)")
				.Define("n_electrons",  "ReconstructedParticle::get_n(electrons)") #count how many electrons are in the event in total

				.Alias("Muon0", "Muon#0.index")
				.Define("muons",  "ReconstructedParticle::get(Muon0, ReconstructedParticles)")
				.Define("n_muons",  "ReconstructedParticle::get_n(muons)") #count how many muons are in the event in total

				#OBJECT SELECTION: Consider only those objects that have pT > certain threshold
				.Define("selected_jets", "ReconstructedParticle::sel_pt(50.)(Jet)") #select only jets with a pT > 50 GeV
				.Define("selected_electrons", "ReconstructedParticle::sel_pt(20.)(electrons)") #select only electrons with a pT > 20 GeV
				.Define("selected_muons", "ReconstructedParticle::sel_pt(20.)(muons)")

				#SIMPLE VARIABLES: Access the basic kinematic variables of the selected jets, works analogously for electrons, muons
				.Define("seljet_pT",     "ReconstructedParticle::get_pt(selected_jets)") #transverse momentum pT
				.Define("seljet_eta",     "ReconstructedParticle::get_eta(selected_jets)") #pseudorapidity eta
				.Define("seljet_phi",     "ReconstructedParticle::get_phi(selected_jets)") #polar angle in the transverse plane phi

				#EVENTWIDE VARIABLES: Access quantities that exist only once per event, such as the missing transverse energy
				.Define("MET", "ReconstructedParticle::get_pt(MissingET)") #absolute value of MET
				.Define("MET_x", "ReconstructedParticle::get_px(MissingET)") #x-component of MET
				.Define("MET_y", "ReconstructedParticle::get_py(MissingET)") #y-component of MET
				.Define("MET_phi", "ReconstructedParticle::get_phi(MissingET)") #angle of MET
             )
       return df2

    #__________________________________________________________
    # Mandatory: output function, please make sure you return the branchlist as a python list
    def output():
       branchList = [
	   "n_jets",
	   "n_photons",
	   "n_electrons",
	   "n_muons",
	   "seljet_pT",
	   "seljet_eta",
	   "seljet_phi",
	   "MET",
	   "MET_x",
	   "MET_y",
	   "MET_phi",
	    ]
       return branchList
