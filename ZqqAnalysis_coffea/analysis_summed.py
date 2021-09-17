import timeit
import uproot
import awkward as ak
import os
import h5py as h5
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from coffea import hist, processor
from coffea.nanoevents import NanoEventsFactory, BaseSchema, NanoAODSchema
from coffea.nanoevents.methods import vector

#import sys
#sys.modules['__main__'].__file__ = 'ipython'

ak.behavior.update(vector.behavior)

# https://stackoverflow.com/questions/1987694/how-to-print-the-full-numpy-array-without-truncation/24542498#24542498
def fullprint(*args, **kwargs):
  from pprint import pprint
  import numpy
  opt = numpy.get_printoptions()
  numpy.set_printoptions(threshold=numpy.inf)
  pprint(*args, **kwargs)
  numpy.set_printoptions(**opt)

def len_from_pt(pt):
    #avoid calling as this is not array-at-a-time
    return [len(x) for x in pt] 

def Writeh5(output, name,folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
    with h5.File(os.path.join(folder,'{0}.h5'.format(name)), "w") as fh5:
        dset = fh5.create_dataset("histos_neutralKaon", data=output['histos_neutralKaon'].value)
        dset = fh5.create_dataset("histos_chargedKaon", data=output['histos_chargedKaon'].value)
        dset = fh5.create_dataset("histos_neutralPion", data=output['histos_neutralPion'].value)
        dset = fh5.create_dataset("histos_chargedPion", data=output['histos_chargedPion'].value)
        dset = fh5.create_dataset("histos_electron", data=output['histos_electron'].value)
        dset = fh5.create_dataset("histos_muon", data=output['histos_muon'].value)
        dset = fh5.create_dataset("histos_photon", data=output['histos_photon'].value)
        dset = fh5.create_dataset("histos_protonNeutron", data=output['histos_protonNeutron'].value)
        #dset = fh5.create_dataset("data", data=output['data'])
        dset = fh5.create_dataset("pid", data=output['pid'].value)
        #dset = fh5.create_dataset("global", data=output['global'])
        #dset = fh5.create_dataset("px", data=output['px'])
        #dset = fh5.create_dataset("py", data=output['py'])
        #dset = fh5.create_dataset("pz", data=output['pz'])
        #dset = fh5.create_dataset("E", data=output['E'])
        #dset = fh5.create_dataset("invMass", data=output['invMass'])


class Channel():
    def __init__(self, name):
        self.name = name
        self.sel=None
        self.jets= None
        self.pfs=None
        self.pfs_pid=None
        self.glob = None
        self.jet = None
        self.pid = None
        

    def apply_jet_sel(self,quark='up'):
        jet_matched_pfs = self.jets[self.pfs.idx]

        #print(gen_electrons.pdgId)
        #Cuts on jets

        if quark=='up':
            pfs_mask = (np.abs(jet_matched_pfs.partonFlavour)==2) & (jet_matched_pfs.hadronFlavour==0)
        elif quark == 'strange':
            pfs_mask = (np.abs(jet_matched_pfs.partonFlavour)==3) & (jet_matched_pfs.hadronFlavour==0)
        elif quark == 'down':
            pfs_mask = (np.abs(jet_matched_pfs.partonFlavour)==1) & (jet_matched_pfs.hadronFlavour==0)
        else:
            pfs_mask = (np.abs(jet_matched_pfs.partonFlavour)==21) & (jet_matched_pfs.hadronFlavour==0)
            
        self.pfs = self.pfs[pfs_mask]


class MyProcessor(processor.ProcessorABC):
    def __init__(self):
        print('ONCE')
        
        #self._accumulator = processor.dict_accumulator({
        #    "sumw": processor.list_accumulator(),
        #})
        #self._accumulator = processor.list_accumulator()
        
        ##dict_accumulator = {}
        print('DONT FORGET TO UNCOMMENT')
        ML_accumulator = {
            #'histos': processor.column_accumulator(np.zeros([0,8,29,29])),
            #'histos_chargedKaon': processor.column_accumulator(np.zeros([0,29,29])),
            'histos_neutralKaon': processor.column_accumulator(np.zeros([0,29,29])),
            'histos_chargedKaon': processor.column_accumulator(np.zeros([0,29,29])),
            'histos_neutralPion': processor.column_accumulator(np.zeros([0,29,29])),
            'histos_chargedPion': processor.column_accumulator(np.zeros([0,29,29])),
            'histos_electron': processor.column_accumulator(np.zeros([0,29,29])),
            'histos_muon': processor.column_accumulator(np.zeros([0,29,29])),
            'histos_photon': processor.column_accumulator(np.zeros([0,29,29])),
            'histos_protonNeutron': processor.column_accumulator(np.zeros([0,29,29])),
            'pid': processor.column_accumulator(np.zeros([0])),
        }
        self._accumulator = processor.dict_accumulator( ML_accumulator )
        '''
        ML_accumulator = {
            
            'data': processor.list_accumulator(),
            'px': processor.list_accumulator(),
            'py': processor.list_accumulator(),
            'pz': processor.list_accumulator(),
            'E': processor.list_accumulator(),
            'pid': processor.list_accumulator(),
            'MC_px': processor.list_accumulator(),
            'MC_py': processor.list_accumulator(),
            'MC_pz': processor.list_accumulator(),
            'MC_E': processor.list_accumulator(),
            'MC_E_': processor.list_accumulator(),
            'MC_pdg': processor.list_accumulator(),
            'invMass': processor.list_accumulator(),
            'global': processor.list_accumulator(),
        }
        '''
        ##dict_accumulator['ML'] = processor.dict_accumulator(ML_accumulator)
        ##self._accumulator = processor.dict_accumulator( dict_accumulator )

    @property
    def accumulator(self):
        print('ACCUMULATOR')
        return self._accumulator



    def process(self, events):
        print('before')
        #why does commenting out the identity seem to work? No clue!
        output = self.accumulator#.identity()
        print('or after?')
        print('output type')
        #print(type(output['ML']['global']))
        #print('Event type')
        #print(type(events))
        
        jets = ak.zip({
            "t": events.jets_ee_kt_e,
            "x": events.jets_ee_kt_px,
            "y": events.jets_ee_kt_py,
            "z": events.jets_ee_kt_pz,
            "partonFlavour": events.jets_ee_kt_flavour,
            #"r": np.sqrt(events.jets_ee_kt_px**2+events.jets_ee_kt_py**2),
            #"theta": np.arctan2(np.sqrt(events.jets_ee_kt_px**2+events.jets_ee_kt_py**2), events.jets_ee_kt_pz),
        ##}, with_name="PtEtaPhiMCandidate")
        }, with_name="LorentzVector")

        '''
        jets = ak.zip({
            "t": events.jets_kt_e,
            "x": events.jets_kt_px,
            "y": events.jets_kt_py,
            "z": events.jets_kt_pz,
            "partonFlavour": events.jets_kt_flavour,
        ##}, with_name="PtEtaPhiMCandidate")
        }, with_name="LorentzVector")
        '''

        GenPartsf = ak.zip({
            "t": events.MC_e_final,
            "x": events.MC_px_final,
            "y": events.MC_py_final,
            "z": events.MC_pz_final,
            "pdg": events.MC_pdg_final,
            #"r": np.sqrt(events.MC_px_final**2+events.MC_py_final**2),
        }, with_name="LorentzVector")

        #RANDOMIZE FIRST OR SECOND JET!!!

        #Note that for now the implementation is hacky and we basically pass the jet constituents mask first for one jet and then for the other (this may become problematic if there are multiple jets), but this is fine for now as we focus on the exclusive ee_kt. In the future we might want to think about how we could pass both jets at once (19/08/2021)...
        
        #about the flavour -> ik that there is the possible mismatch of two quarks being labelled positive or negative partonFlavour, but I don't really care as I take this to be rare...
        
        print('/////////////////')
        print(jets.x)
        up_mask = (np.abs(jets.partonFlavour[:,0])==2)&(np.abs(jets.partonFlavour[:,1])==2)
        down_mask = (np.abs(jets.partonFlavour[:,0])==1)&(np.abs(jets.partonFlavour[:,1])==1)
        strange_mask = (np.abs(jets.partonFlavour[:,0])==3)&(np.abs(jets.partonFlavour[:,1])==3)
        charm_mask = (np.abs(jets.partonFlavour[:,0])==4)&(np.abs(jets.partonFlavour[:,1])==4)
        bottom_mask = (np.abs(jets.partonFlavour[:,0])==5)&(np.abs(jets.partonFlavour[:,1])==5)

        pid = 2*up_mask+down_mask+3*strange_mask+4*charm_mask+5*bottom_mask
        
        #below is code to reduce memory footprint
        up_mask
        down_mask
        strange_mask
        charm_mask
        bottom_mask
        

        
        
        
        firstjetGenPartsf = ak.copy(GenPartsf[events.jetconstituents_ee_kt[:,0]])

        #more attempts to free up memory...
        #secondjetGenPartsf = ak.copy(GenPartsf[events.jetconstituents_ee_kt[:,1]])
        del GenPartsf
        
        neutralKaon_mask = (np.abs(firstjetGenPartsf.pdg)==130)|(np.abs(firstjetGenPartsf.pdg)==310)
        chargedKaon_mask = (np.abs(firstjetGenPartsf.pdg)==321)
        neutralPion_mask = (np.abs(firstjetGenPartsf.pdg)==111)
        chargedPion_mask = (np.abs(firstjetGenPartsf.pdg)==211)
        electron_mask = (np.abs(firstjetGenPartsf.pdg)==11)
        muon_mask = (np.abs(firstjetGenPartsf.pdg)==13)
        photon_mask = (np.abs(firstjetGenPartsf.pdg)==22)
        protonNeutron_mask = (np.abs(firstjetGenPartsf.pdg)==2212)|(np.abs(firstjetGenPartsf.pdg)==2112)
        
        '''
        kaon_mask = ak.copy(np.abs(firstjetGenPartsf.pdg)==321)
        kaon_parts = firstjetGenPartsf[kaon_mask]
        kaons = (jets[ak.num(kaon_parts.t)>0])[:,0]
        kaons = jets[:,0]
        #kaon_parts = kaon_parts[ak.num(kaon_parts.t)>0]
        '''
        # PAY ATTENTION HERE CAUSE KAON CHANGES...

        theta_diff = jets.theta[:,0] - firstjetGenPartsf.theta
        phi_diff = jets.phi[:,0] - firstjetGenPartsf.phi
        phi_diff = ((phi_diff+np.pi)%2)-np.pi
        print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')

        #histogramming in a single event seems simple enough, but now I must proceed and apply it to all while avoiding loops cause speed. Helpful suggestion found here: https://stackoverflow.com/questions/18851471/numpy-histogram-on-multi-dimensional-array 
        #side note-> np is fine as the array is jagged overall but not per entry, could use coffea if I want to also (as coffea hist has values() to get values)
        #I will leave things off here, as a note for Monday -> implement this for arrays of all events. Once I have one image per event I can build NN and try to feed it images (even if they are baloney!)
        ##nphisto = np.histogram2d(firstjetGenPartsf.phi[0], firstjetGenPartsf.theta[0])
        #decrease image resolution to have low memory footprint
        nphisto = np.zeros([8,29,29])
        #nphisto = np.zeros([len(firstjetGenPartsf.phi),8,19,19])
        bins = np.linspace(-0.5,0.5,30)
        #histoZ, xbins, ybins = np.histogram2d(np.array(firstjetGenPartsf.phi[0]), np.array(firstjetGenPartsf.theta[0]), bins=bins)
        
        neutralKaon_phi_diff = phi_diff[neutralKaon_mask]
        chargedKaon_phi_diff = phi_diff[chargedKaon_mask]
        neutralPion_phi_diff = phi_diff[neutralPion_mask]
        chargedPion_phi_diff = phi_diff[chargedPion_mask]
        electron_phi_diff = phi_diff[electron_mask]
        muon_phi_diff = phi_diff[muon_mask]
        photon_phi_diff = phi_diff[photon_mask]
        protonNeutron_phi_diff = phi_diff[protonNeutron_mask]
        
        neutralKaon_theta_diff = theta_diff[neutralKaon_mask]
        chargedKaon_theta_diff = theta_diff[chargedKaon_mask]
        neutralPion_theta_diff = theta_diff[neutralPion_mask]
        chargedPion_theta_diff = theta_diff[chargedPion_mask]
        electron_theta_diff = theta_diff[electron_mask]
        muon_theta_diff = theta_diff[muon_mask]
        photon_theta_diff = theta_diff[photon_mask]
        protonNeutron_theta_diff = theta_diff[protonNeutron_mask]
        
        neutralKaon_weights = ((firstjetGenPartsf.p)/(jets.p[:,0]))[neutralKaon_mask]
        chargedKaon_weights = ((firstjetGenPartsf.p)/(jets.p[:,0]))[chargedKaon_mask]
        neutralPion_weights = ((firstjetGenPartsf.p)/(jets.p[:,0]))[neutralPion_mask]
        chargedPion_weights = ((firstjetGenPartsf.p)/(jets.p[:,0]))[chargedPion_mask]
        electron_weights = ((firstjetGenPartsf.p)/(jets.p[:,0]))[electron_mask]
        muon_weights = ((firstjetGenPartsf.p)/(jets.p[:,0]))[muon_mask]
        photon_weights = ((firstjetGenPartsf.p)/(jets.p[:,0]))[photon_mask]
        protonNeutron_weights = ((firstjetGenPartsf.p)/(jets.p[:,0]))[protonNeutron_mask]
        
        #Can shortened from 30, esp. for things like muons where we will never have 30 muons per jet
        neutralKaon_phi_diff = np.asarray(ak.fill_none(ak.pad_none(neutralKaon_phi_diff, 70, clip=True), 999))
        chargedKaon_phi_diff = np.asarray(ak.fill_none(ak.pad_none(chargedKaon_phi_diff, 70, clip=True), 999))
        neutralPion_phi_diff = np.asarray(ak.fill_none(ak.pad_none(neutralPion_phi_diff, 70, clip=True), 999))
        chargedPion_phi_diff = np.asarray(ak.fill_none(ak.pad_none(chargedPion_phi_diff, 70, clip=True), 999))
        electron_phi_diff = np.asarray(ak.fill_none(ak.pad_none(electron_phi_diff, 70, clip=True), 999))
        muon_phi_diff = np.asarray(ak.fill_none(ak.pad_none(muon_phi_diff, 70, clip=True), 999))
        photon_phi_diff = np.asarray(ak.fill_none(ak.pad_none(photon_phi_diff, 70, clip=True), 999))
        protonNeutron_phi_diff = np.asarray(ak.fill_none(ak.pad_none(protonNeutron_phi_diff, 70, clip=True), 999))
        
        neutralKaon_theta_diff = np.asarray(ak.fill_none(ak.pad_none(neutralKaon_theta_diff, 70, clip=True), 999))
        chargedKaon_theta_diff = np.asarray(ak.fill_none(ak.pad_none(chargedKaon_theta_diff, 70, clip=True), 999))
        neutralPion_theta_diff = np.asarray(ak.fill_none(ak.pad_none(neutralPion_theta_diff, 70, clip=True), 999))
        chargedPion_theta_diff = np.asarray(ak.fill_none(ak.pad_none(chargedPion_theta_diff, 70, clip=True), 999))
        electron_theta_diff = np.asarray(ak.fill_none(ak.pad_none(electron_theta_diff, 70, clip=True), 999))
        muon_theta_diff = np.asarray(ak.fill_none(ak.pad_none(muon_theta_diff, 70, clip=True), 999))
        photon_theta_diff = np.asarray(ak.fill_none(ak.pad_none(photon_theta_diff, 70, clip=True), 999))
        protonNeutron_theta_diff = np.asarray(ak.fill_none(ak.pad_none(protonNeutron_theta_diff, 70, clip=True), 999))
        
        #Write this padding into a function, and a subsequent loop from a list, or maybe channels? Turned out longer and uglier than I expected...
        neutralKaon_weights = np.asarray(ak.fill_none(ak.pad_none(neutralKaon_weights, 70, clip=True), 0))
        chargedKaon_weights = np.asarray(ak.fill_none(ak.pad_none(chargedKaon_weights, 70, clip=True), 0))
        neutralPion_weights = np.asarray(ak.fill_none(ak.pad_none(neutralPion_weights, 70, clip=True), 0))
        chargedPion_weights = np.asarray(ak.fill_none(ak.pad_none(chargedPion_weights, 70, clip=True), 0))
        electron_weights = np.asarray(ak.fill_none(ak.pad_none(electron_weights, 70, clip=True), 0))
        muon_weights = np.asarray(ak.fill_none(ak.pad_none(muon_weights, 70, clip=True), 0))
        photon_weights = np.asarray(ak.fill_none(ak.pad_none(photon_weights, 70, clip=True), 0))
        protonNeutron_weights = np.asarray(ak.fill_none(ak.pad_none(protonNeutron_weights, 70, clip=True), 0))
        

        
        # https://iscinumpy.gitlab.io/post/histogram-speeds-in-python/ -> could follow one of these approaches or simply histogram in root entirely... The upside to histogramming in root is that we will have to save generic h5 files which we could feed to any network...
        
        start_time = timeit.default_timer()
        '''
        for i in range(len(firstjetGenPartsf.phi)):
            nphisto[i,0] = np.histogram2d(np.array(phi_diff[neutralKaon_mask][i]), np.array(theta_diff[neutralKaon_mask][i]), bins=bins)[0]
            nphisto[i,1] = np.histogram2d(np.array(phi_diff[chargedKaon_mask][i]), np.array(theta_diff[chargedKaon_mask][i]), bins=bins)[0]
            nphisto[i,2] = np.histogram2d(np.array(phi_diff[neutralPion_mask][i]), np.array(theta_diff[neutralPion_mask][i]), bins=bins)[0]
            nphisto[i,3] = np.histogram2d(np.array(phi_diff[chargedPion_mask][i]), np.array(theta_diff[chargedPion_mask][i]), bins=bins)[0]
            nphisto[i,4] = np.histogram2d(np.array(phi_diff[electron_mask][i]), np.array(theta_diff[electron_mask][i]), bins=bins)[0]
            nphisto[i,5] = np.histogram2d(np.array(phi_diff[muon_mask][i]), np.array(theta_diff[muon_mask][i]), bins=bins)[0]
            nphisto[i,6] = np.histogram2d(np.array(phi_diff[photon_mask][i]), np.array(theta_diff[photon_mask][i]), bins=bins)[0]
            nphisto[i,7] = np.histogram2d(np.array(phi_diff[protonNeutron_mask][i]), np.array(theta_diff[protonNeutron_mask][i]), bins=bins)[0]
        '''
        for i in range(len(firstjetGenPartsf.phi)):
            if(bottom_mask[i]): 
                nphisto[0] += np.histogram2d(neutralKaon_phi_diff[i], neutralKaon_theta_diff[i], bins=bins, weights=neutralKaon_weights[i])[0]
                nphisto[1] += np.histogram2d(chargedKaon_phi_diff[i], chargedKaon_theta_diff[i], bins=bins, weights=chargedKaon_weights[i])[0]
                nphisto[2] += np.histogram2d(neutralPion_phi_diff[i], neutralPion_theta_diff[i], bins=bins, weights=neutralPion_weights[i])[0]
                nphisto[3] += np.histogram2d(chargedPion_phi_diff[i], chargedPion_theta_diff[i], bins=bins, weights=chargedPion_weights[i])[0]
                nphisto[4] += np.histogram2d(electron_phi_diff[i], electron_theta_diff[i], bins=bins, weights=electron_weights[i])[0]
                nphisto[5] += np.histogram2d(muon_phi_diff[i], muon_theta_diff[i], bins=bins, weights=muon_weights[i])[0]
                nphisto[6] += np.histogram2d(photon_phi_diff[i], photon_theta_diff[i], bins=bins, weights=photon_weights[i])[0]
                nphisto[7] += np.histogram2d(protonNeutron_phi_diff[i], protonNeutron_theta_diff[i], bins=bins, weights=protonNeutron_weights[i])[0]
            else:
                continue
        elapsed = timeit.default_timer() - start_time
        print('ELAPSED TIME -> '+str(elapsed))
        
        #nphisto = nphisto[pid!=0]
        #pid = pid[pid!=0]
        '''
        print(firstjetGenPartsf.mass[1])

        print(firstjetGenPartsf.t[1])
        print(ak.sum(firstjetGenPartsf.t,axis=1))
        print(jets.t[:,0])
        '''
        '''
        print(len(events.jetconstituents_ee_kt[0][0])+len(events.jetconstituents_ee_kt[0][1]))
        print(events.jetconstituents_ee_kt[1,0])
        print('.............................')
        print((GenPartsf.t[events.jetconstituents_ee_kt[:,0]])[1])
        print((GenPartsf[events.jetconstituents_ee_kt[:,0]].t)[1])
        print(type(events.jetconstituents_ee_kt[0]))
        '''
        #print('output type pre')
        #print(type(output['ML']['global']))
        ##########output['ML']['global']+= jets.partonFlavour.tolist()#PFCands.pt[0].tolist()
        #output['global']+= processor.column_accumulator(np.array(jets.x))#PFCands.pt[0].tolist()
        print('?????????????????')
        print((output['histos_chargedKaon'].value).shape)
        print(nphisto[1].shape)
        #print(np.expand_dims(nphisto[1], axis=0).shape)
        output['histos_neutralKaon']+= processor.column_accumulator(np.expand_dims(nphisto[0], axis=0))#PFCands.pt[0].tolist()
        output['histos_chargedKaon']+= processor.column_accumulator(np.expand_dims(nphisto[1], axis=0))#PFCands.pt[0].tolist()
        output['histos_neutralPion']+= processor.column_accumulator(np.expand_dims(nphisto[2], axis=0))#PFCands.pt[0].tolist()
        output['histos_chargedPion']+= processor.column_accumulator(np.expand_dims(nphisto[3], axis=0))#PFCands.pt[0].tolist()
        output['histos_electron']+= processor.column_accumulator(np.expand_dims(nphisto[4], axis=0))#PFCands.pt[0].tolist()
        output['histos_muon']+= processor.column_accumulator(np.expand_dims(nphisto[5], axis=0))#PFCands.pt[0].tolist()
        output['histos_photon']+= processor.column_accumulator(np.expand_dims(nphisto[6], axis=0))#PFCands.pt[0].tolist()
        output['histos_protonNeutron']+= processor.column_accumulator(np.expand_dims(nphisto[7], axis=0))#PFCands.pt[0].tolist()
        #output['histos_chargedKaon']+= processor.column_accumulator(nphisto[1])#PFCands.pt[0].tolist()
        output['pid']+= processor.column_accumulator(np.array(pid))
        print((output['histos_chargedKaon'].value).shape)
        ##output['sumw']+= jets.partonFlavour.tolist()#PFCands.pt[0].tolist()
        '''
        output['ML']['pid']+= jets.partonFlavour.tolist()#PFCands.pt[0].tolist()
        output['ML']['px']+= jets.x.tolist()#PFCands.pt[0].tolist()
        output['ML']['py']+= jets.y.tolist()#PFCands.pt[0].tolist()
        output['ML']['pz']+= jets.z.tolist()#PFCands.pt[0].tolist()
        output['ML']['E']+= jets.t.tolist()#PFCands.pt[0].tolist()
        output['ML']['invMass']+= jets.mass.tolist()#PFCands.pt[0].tolist()
        output['ML']['MC_pdg_jet']+= GenPartsf.pdg.tolist()#PFCands.pt[0].tolist()
        output['ML']['MC_px_jet']+= GenPartsf.x.tolist()#PFCands.pt[0].tolist()
        output['ML']['MC_py_jet']+= GenPartsf.y.tolist()#PFCands.pt[0].tolist()
        output['ML']['MC_pz_jet']+= GenPartsf.z.tolist()#PFCands.pt[0].tolist()
        #output['ML']['MC_E']+= GenPartsf.t[events.jetconstituents_kt]#PFCands.pt[0].tolist()
        #output['ML']['MC_E_']+= GenPartsf[events.jetconstituents_kt].t.tolist()#PFCands.pt[0].tolist()
        '''
        '''
        print(output['ML']['MC_E'])
        print('...................')
        print(output['ML']['MC_E_'])
        '''
        #match_mask = (events.JetPFCands_pFCandsIdx < PFCands.counts) & (events.JetPFCands_jetIdx < Jets.counts) & (events.JetPFCands_pFCandsIdx > -1)
        #PFCands = PFCands[events.JetPFCands_pFCandsIdx[match_mask]].deepcopy()
        #PFCands.add_attributes(idx=df["JetPFCands_jetIdx"][match_mask])

        #print(type(events.Jet.fields))
        #print(type(jets.energy))
        #print(events.PFCands.energy[7])
        #print('output type post')
        #print(type(output['ML']['global']))
        return output

    def postprocess(self, accumulator):
        print('POSTPROCESS')
        return accumulator

#p = MyProcessor()
filename = "rootFiles//p8_ee_Zbb_ecm91.root"
file = uproot.open(filename)
'''
events = NanoEventsFactory.from_root(
    file,
    entry_stop=1,
    ##metadata={"dataset": "DoubleMuon"},
    #schemaclass=BaseSchema,
    schemaclass= NanoAODSchema,
    treepath="/events",
).events()
'''
#events = processor.LazyDataFrame(file['events'], entrystop=20000000)
#out = p.process(events)

fileset = {'JetandStuff': [filename]}
print("fileset")
print(fileset)
'''
output = processor.run_uproot_job(fileset,
    treename='events',
    processor_instance=MyProcessor(),
    executor=processor.futures_executor,
    #executor_args={'workers':opt.cpu},
    executor_args={'schema': None},#processor.LazyDataFrame},
    maxchunks =3,
    chunksize = 1000,
)
'''

output = processor.run_uproot_job(fileset,
    treename='events',
    processor_instance=MyProcessor(),
    executor=processor.futures_executor,
    #executor_args={'workers':opt.cpu},
    executor_args={'schema': None, 'workers':4,},#processor.LazyDataFrame},
    maxchunks =20,
    chunksize = 5000,
)


#print(output)
#print(len(output['nConsti'].value))
#Writeh5(output, 'nConsti_b', 'h5_output')
output['histos_neutralKaon'] = processor.column_accumulator(np.sum(output['histos_neutralKaon'].value, axis=0))
output['histos_chargedKaon'] = processor.column_accumulator(np.sum(output['histos_chargedKaon'].value, axis=0))
output['histos_neutralPion'] = processor.column_accumulator(np.sum(output['histos_neutralPion'].value, axis=0))
output['histos_chargedPion'] = processor.column_accumulator(np.sum(output['histos_chargedPion'].value, axis=0))
output['histos_electron'] = processor.column_accumulator(np.sum(output['histos_electron'].value, axis=0))
output['histos_muon'] = processor.column_accumulator(np.sum(output['histos_muon'].value, axis=0))
output['histos_photon'] = processor.column_accumulator(np.sum(output['histos_photon'].value, axis=0))
output['histos_protonNeutron'] = processor.column_accumulator(np.sum(output['histos_protonNeutron'].value, axis=0))
Writeh5(output, 'Zbb_weighted_summed', 'h5_output')
#print(len(out['ML']['pid']))
#print(len(out['ML']['global']))

print('REMEMBER LOOP MASK')




### NOTE FOR MONDAY ######
'''
I am still working on adapting the coffea code, in particular I am checking the rearranging but this seems to be done syntax aside. We lose some functionality here but oh well... Could always use PYROOT where needed...

On the to do list:
    1. add the class structure
    2. add the histogramming/pfcands analysis, for now same plots just for pdgid
    3. add the h5 file saving
    4. build and train network in colab
------------------------------------------
    5. polish things in coffea like using a proper processor

'''










