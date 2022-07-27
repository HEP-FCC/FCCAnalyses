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
            'pid_Kl': processor.column_accumulator(np.zeros([0])),
            'Kl_p': processor.column_accumulator(np.zeros([0])),
            'dKl_theta': processor.column_accumulator(np.zeros([0])),
            'dKl_phi': processor.column_accumulator(np.zeros([0])),
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
        



        # Here cuts are implemented theta cut > ~ 14deg |p|>40 GeV

        jets_mask = (np.cos(jets.theta)<0.97) & (jets.p>40)

        event_mask = (ak.num(jets[jets_mask].theta, axis=1)==2) & (pid!=0)


        jets_cut = ak.copy(jets[event_mask])
        GenPartsf_cut = ak.copy(GenPartsf[event_mask])
        pid = pid[event_mask]

        # A remark: It is important to cut on jet constituents after having assigned to constituents to their respective jet, as these cuts jet consitutent arrays will no longer match the indices
        # given in events.jetconstituents_ee_kt. In this example we consider only the leading jet.

        # Here cuts are imposed on the jetConstituents of the leading jet theta cut > ~ 14 deg pt>500 GeV 
        leadingjetGenPartsf = ak.copy(GenPartsf[events.jetconstituents_ee_kt[:,0]])
        
        leadingjetGenPartsf = leadingjetGenPartsf[event_mask]
        
        jetConstituents_mask = (np.cos(leadingjetGenPartsf.theta)<0.97) & (leadingjetGenPartsf.r>0.5)
        leadingjetGenPartsf = leadingjetGenPartsf[jetConstituents_mask]


        # Here we compute first the Z_candidates

        Z_cand = jets_cut[:,0] + jets_cut[:,1]

        # Here we compute |p| distribution of long Kaons in the leading jet

        longKaon_mask = (np.abs(leadingjetGenPartsf.pdg)==130)
        longKaon_p = leadingjetGenPartsf[longKaon_mask].p

        # Here we compute the angular distance of long Kaons in the leading jet

        theta_diff = jets_cut.theta[:,0] - leadingjetGenPartsf[longKaon_mask].theta
        phi_diff = jets_cut.phi[:,0] - leadingjetGenPartsf[longKaon_mask].phi
        phi_diff = ((phi_diff+np.pi)%(2*np.pi))-np.pi

        
        pid_Kl = ak.flatten(ak.broadcast_arrays(pid, phi_diff)[0], axis=None)

        output['Z_mass']+= processor.column_accumulator(np.asarray(Z_cand.mass))
        output['pid']+= processor.column_accumulator(np.asarray(pid))
        output['pid_Kl']+= processor.column_accumulator(np.asarray(pid_Kl))
        output['Kl_p']+= processor.column_accumulator(np.asarray(ak.flatten(longKaon_p)))
        output['dKl_theta']+= processor.column_accumulator(np.asarray(ak.flatten(theta_diff)))
        output['dKl_phi']+= processor.column_accumulator(np.asarray(ak.flatten(phi_diff)))

        return output

    def postprocess(self, accumulator):
        return accumulator

filename = "outputs/FCCee/Zqq/p8_ee_Zuds_ecm91.root"
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
pid_Kl = output['pid_Kl'].value
Kl_p = output['Kl_p'].value
dKl_theta = output['dKl_theta'].value
dKl_phi = output['dKl_phi'].value


# Here the Z invariant mass is histogrammed using coffea histograms.

Z_cand_hist = hist.Hist(
    "Events",
    hist.Cat("flavour", "Quark flavour"),
    hist.Bin("m", r"$m_{q \bar{q}}$ [GeV]", 30, 90.75, 91.65),
)

for i_f, flav in enumerate(["down", "up", "strange"]):
    Z_cand_hist.fill(
        flavour=flav,
        m=Z_mass[(pid==(i_f+1))],
    )

ax = hist.plot1d(
    Z_cand_hist,
    overlay="flavour",
    stack=True,
    fill_opts={'alpha': .5, 'edgecolor': (0,0,0,0.3)}
)

ax.get_legend().shadow = True
ax.set_title(r'$Z \rightarrow q\bar{q}$ invariant mass')

plt.savefig('examples/FCCee/Zqq/Zpeak.png')

plt.clf()

Kl_p_hist = hist.Hist(
    "Constituent Count",
    hist.Cat("flavour", "Quark flavour"),
    hist.Bin("p", "|$p$| [GeV]", 38, 0, 37),
)

for i_f, flav in enumerate(["down", "up", "strange"]):
    Kl_p_hist.fill(
        flavour=flav,
        p=Kl_p[(pid_Kl==(i_f+1))],
    )

ax = hist.plot1d(
    Kl_p_hist,
    overlay="flavour",
    stack=True,
    fill_opts={'alpha': .5, 'edgecolor': (0,0,0,0.3)}
)


ax.get_legend().shadow = True
ax.set_title(r'$K_{L}$ |p| distribution in $Z \rightarrow q\bar{q}$ leading jets')

plt.savefig('examples/FCCee/Zqq/Kl_p.pdf')

plt.clf()


Kl_angle_hist = hist.Hist(
    "Constituent Count",
    hist.Bin("theta", r"$\Delta \theta$ [rad]", 29, -0.5, 0.5),
    hist.Bin("phi", r"$\Delta \phi$ [rad]", 29, -0.5, 0.5),
)


Kl_angle_hist.fill(theta=dKl_theta[(pid_Kl==3)], phi=dKl_phi[(pid_Kl==3)])

ax = hist.plot2d(
    Kl_angle_hist,
    xaxis = "phi",
)

ax.set_title(r'$K_{L}$ distribution in $Z \rightarrow s\bar{s}$ leading jets')

plt.savefig('examples/FCCee/Zqq/Kl_angle_hist.pdf')












