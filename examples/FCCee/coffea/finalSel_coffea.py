import uproot
import awkward as ak
import h5py as h5
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from coffea import hist, processor
from coffea.nanoevents.methods import vector


ak.behavior.update(vector.behavior)



# As detailed in the coffea docs, the core of the analysis script is the Processor class defined below. The Processor.process function will be called on every batch being processed.  

class MyProcessor(processor.ProcessorABC):
    def __init__(self):
       

        # We begin by defining the accumulator which will hold all quantities we intend to output. In this case it will be only the Z invariant mass and the flavour of the quarks.
        
        Z_accumulator = {
            'Z_mass': processor.column_accumulator(np.zeros([0])),
            'pid': processor.column_accumulator(np.zeros([0])),
        }
        self._accumulator = processor.dict_accumulator( Z_accumulator )

    @property
    def accumulator(self):
        return self._accumulator



    def process(self, events):
        
        output = self.accumulator.identity()
        

        # Here, the jets are defined LorentzVector classes (meaning several attributes and operations, such as jets.eta, will be accessible)

        jets = ak.zip({
            "t": events.jets_ee_kt_e,
            "x": events.jets_ee_kt_px,
            "y": events.jets_ee_kt_py,
            "z": events.jets_ee_kt_pz,
            "partonFlavour": events.jets_ee_kt_flavour,
        }, with_name="LorentzVector")


        # The (stable) gen level particles are defined similarly, but with their corresponding arrays

        GenPartsf = ak.zip({
            "t": events.MC_e_f,
            "x": events.MC_px_f,
            "y": events.MC_py_f,
            "z": events.MC_pz_f,
            "pdg": events.MC_pdg_f,
        }, with_name="LorentzVector")


        
        # Here the flavour mask is defined by requiring both the quark and antiquark initiated jets to have the same flavour (which is non-negative). Unmatched or incorrectly matched jets result in a flavour of 0.
 
        up_mask = (np.abs(jets.partonFlavour[:,0])==2)&(np.abs(jets.partonFlavour[:,1])==2)
        down_mask = (np.abs(jets.partonFlavour[:,0])==1)&(np.abs(jets.partonFlavour[:,1])==1)
        strange_mask = (np.abs(jets.partonFlavour[:,0])==3)&(np.abs(jets.partonFlavour[:,1])==3)
        charm_mask = (np.abs(jets.partonFlavour[:,0])==4)&(np.abs(jets.partonFlavour[:,1])==4)
        bottom_mask = (np.abs(jets.partonFlavour[:,0])==5)&(np.abs(jets.partonFlavour[:,1])==5)

        pid = 2*up_mask+down_mask+3*strange_mask+4*charm_mask+5*bottom_mask
        


        # jets[:,::2] selects only the leading jet of an event, while jets[:,1::2] selects the subleading. In this way the Z candidates are computed, having the same LorentzVector structure as the jets from which they are computed.

        Z_cand = jets[:,::2]+jets[:,1::2]
        



        #----------------------------------------------------------------------------------------------------------------------------------------------------------------------
        #########################
        #ASIDE: Jet constituents#
        #########################
    
        # Though not relevant in this simple example, in most cases one will want to have access to the jet constituents clustered into the first and second jets. This is possible by passing events.jetconstituents_ee_kt as a mask to the (stable) gen level particles. The events.jetconstituents_ee_kt array contains the indices of each (stable) gen level particle clustered into a given jet, and can thus be used to define a new collection consisting only the the particles in a given jet. 

        # For instance, the jet constituents of the leading jet are defined as 

        firstjetGenPartsf = ak.copy(GenPartsf[events.jetconstituents_ee_kt[:,0]])

        # While the jet consituents of the sub-leading jet are defined as

        secondjetGenPartsf = ak.copy(GenPartsf[events.jetconstituents_ee_kt[:,1]])
        #------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        # Here the Z candidates with undefined flavours are removed. Note that this syntax is general and could be used for any cuts e.g. kinematic
        # Requiring a jet mass > 80 GeV would be 
        # Z_cand = Z_cand[Z_cand.mass>80]

        Z_cand = Z_cand[pid!=0]
        pid = pid[pid!=0]
        

        output['Z_mass']+= processor.column_accumulator(np.asarray(ak.flatten(Z_cand.mass)))
        output['pid']+= processor.column_accumulator(np.asarray(pid))

        return output

    def postprocess(self, accumulator):
        return accumulator

filename = "outputs/FCCee/coffea/p8_ee_Zuds_ecm91.root"
fileset = {'Zqq': [filename]}

# The processor run_uproot_job loads the events via uproot and executes process function on the defined batches. The 'maxchunks' argument defined the maximum number of chunks that will be processed, while the 'chunksize' defines the number of events per chunk. The 'workers' argument defines how many parallel processes are run. 

output = processor.run_uproot_job(fileset,
    treename='events',
    processor_instance=MyProcessor(),
    executor=processor.futures_executor,
    executor_args={'schema': None, 'workers':4,},
    maxchunks =20,
    chunksize = 5000,
)


##########
#PLOTTING#
##########

Z_mass = output['Z_mass'].value
pid = output['pid'].value

# Here the Z invariant mass is histogrammed using coffea histograms. Subsequently, the invariant mass and quark flavour is saved as an .h5 file.

Z_cand = hist.Hist(
    "Events",
    hist.Cat("flavour", "Quark flavour"),
    hist.Bin("m", r"$m_{q \bar{q}}$ [GeV]", 30, 90.75, 91.65),
)

for i_f, flav in enumerate(["down", "up", "strange"]):
    Z_cand.fill(
        flavour=flav,
        m=Z_mass[(pid==(i_f+1))],
    )

ax = hist.plot1d(
    Z_cand,
    overlay="flavour",
    stack=True,
    fill_opts={'alpha': .5, 'edgecolor': (0,0,0,0.3)}
)

ax.get_legend().shadow = True
ax.set_title(r'$Z \rightarrow q\bar{q}$ invariant mass')

plt.savefig('examples/FCCee/coffea/Zpeak.pdf')

h5_file = h5.File('examples/FCCee/coffea/Zpeak.h5', 'w')
h5_file.create_dataset("Z_mass", data=Z_mass)
h5_file.create_dataset("pid", data=pid)












