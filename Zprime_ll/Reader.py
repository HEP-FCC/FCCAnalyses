from heppy.framework.analyzer import Analyzer
from heppy.particles.fcc.particle import Particle
from heppy.particles.fcc.jet import Jet
from heppy.particles.fcc.vertex import Vertex 
from heppy.particles.fcc.met import Met
import heppy.configuration

import math

class MissingCollection(Exception):
    pass

class Reader(Analyzer):
    '''Reads events in FCC EDM format, and creates lists of objects adapted to an
    analysis in python.

    Configuration: 
    ----------------------
    
    Example: 
    
    from heppy.analyzers.fcc.Reader import Reader
    source = cfg.Analyzer(
      Reader,
      mode = 'ee',
      # all the parameters below are optional: 
      gen_particles = 'GenParticle',
      # gen_vertices = '<gen_vertices_name>', 
      # gen_jets = '<gen_jets_name>',
      # jets = '<jets_name>',
    )

    * mode: 

    'ee', 'pp', or 'ep'.

    In 'ee' mode, particle-like objects are sorted by decreasing energy. 
    in other modes, by decreasing pt.

    * gen_particles: 

    Name of the collection of gen particles in the input 
    root file. Open the root file with root, and print the events TTree 
    to see which collections are present in your input file.

    * gen_vertices: 
    
    Name of the collection of gen vertices
   
    * gen_jets: 
    
    Name of the collection of gen jets.
    
    * jets: 
    
    Name of the collection of reconstructed jets
  
    You can find out about the names of the collections by opening
    the root file with root, and by printing the events TTree.

    Creates: 
    --------    

    if self.cfg_ana.gen_particles is set: 
    - event.gen_particles: gen particles
    - event.gen_particles_stable: stable gen_particles except neutrinos

    if the respective parameter is set (see above): 
    - event.gen_vertices: gen vertices (needed for gen particle history)
    - event.gen_jets: gen jets
    - event.jets: reconstructed jets  
    '''
    
    def process(self, event):
        store = event.input

        def get_collection(class_object, coll_label, sort=True):
            pycoll = None
            if hasattr(self.cfg_ana, coll_label):
                coll_name = getattr( self.cfg_ana, coll_label)
                coll = store.get( coll_name )
                if coll == None:
                    raise MissingCollection(
                        'collection {} is missing'.format(coll_name)
                        )
                pycoll = map(class_object, coll)
                if sort:
                    pycoll.sort(reverse=True)
                setattr(event, coll_label, pycoll)
            return pycoll


        # store only 1st event weight for now
        event.weight = - 999.
        if hasattr(self.cfg_ana, 'weights'):
            coll_name = getattr( self.cfg_ana, 'weights' )
            weightcoll = store.get( coll_name )
            if weightcoll:
                event.weight = weightcoll[0].value()

        if hasattr(self.cfg_ana, 'gen_particles'):
            get_collection(Particle, 'gen_particles')

        if hasattr(self.cfg_ana, 'gen_vertices'):
            get_collection(Vertex, 'gen_vertices', False)

        if hasattr(self.cfg_ana, 'gen_jets'):
            get_collection(Jet, 'gen_jets')

        jetcoll = get_collection(Jet, 'jets')
        if jetcoll:
            jets = dict()
            for jet in jetcoll:
                jets[jet] = jet
            if hasattr(self.cfg_ana, 'bTags'):
                for bjet in store.get(self.cfg_ana.bTags):
                    jets[Jet(bjet.jet())].tags['bf'] = bjet.tag()

            if hasattr(self.cfg_ana, 'cTags'):
                for cjet in store.get(self.cfg_ana.cTags):
                    jets[Jet(cjet.jet())].tags['cf'] = cjet.tag()

            if hasattr(self.cfg_ana, 'tauTags'):
                for taujet in store.get(self.cfg_ana.tauTags):
                    jets[Jet(taujet.jet())].tags['tauf'] = taujet.tag()

        ############################
        #  jet substructure stuff  #
        ############################
        
        fatjetcoll = get_collection(Jet, 'fatjets')
        if fatjetcoll:
            fatjets = dict()
            for jet in fatjetcoll:
                fatjets[jet] = jet
            # store N-subjettiness up to 3
            if hasattr(self.cfg_ana, 'jetsOneSubJettiness'):
                for tjet in store.get(self.cfg_ana.jetsOneSubJettiness):
                    fatjets[Jet(tjet.jet())].tau1 = tjet.tag()

            if hasattr(self.cfg_ana, 'jetsTwoSubJettiness'):
                for tjet in store.get(self.cfg_ana.jetsTwoSubJettiness):
                    fatjets[Jet(tjet.jet())].tau2 = tjet.tag()
            if hasattr(self.cfg_ana, 'jetsThreeSubJettiness'):
                for tjet in store.get(self.cfg_ana.jetsThreeSubJettiness):
                    fatjets[Jet(tjet.jet())].tau3 = tjet.tag()

            from collections import defaultdict
            # store subjets according to various algorithms
            # the first entry of subjets list is the "cleaned" fastjet itself
            
            # trimming
            if hasattr(self.cfg_ana, 'subjetsTrimming') and hasattr(self.cfg_ana, 'subjetsTrimmingTagged'):
                 relations = defaultdict(list)
                 for tjet in store.get(self.cfg_ana.subjetsTrimmingTagged):
                      for i in range(tjet.subjets_size()):
                          relations[Jet(tjet.jet())].append(Jet(tjet.subjets(i)))
                 for fatjet, subjets in relations.items():
                     fatjets[fatjet].subjetsTrimming = subjets

            # pruning
            if hasattr(self.cfg_ana, 'subjetsPruning') and hasattr(self.cfg_ana, 'subjetsPruningTagged'):
                 relations = defaultdict(list)
                 for tjet in store.get(self.cfg_ana.subjetsPruningTagged):
                      for i in range(tjet.subjets_size()):
                          relations[Jet(tjet.jet())].append(Jet(tjet.subjets(i)))
                 for fatjet, subjets in relations.items():
                     fatjets[fatjet].subjetsPruning = subjets

            # soft drop
            if hasattr(self.cfg_ana, 'subjetsSoftDrop') and hasattr(self.cfg_ana, 'subjetsSoftDropTagged'):
                 relations = defaultdict(list)
                 for tjet in store.get(self.cfg_ana.subjetsSoftDropTagged):
                      for i in range(tjet.subjets_size()):
                          relations[Jet(tjet.jet())].append(Jet(tjet.subjets(i)))
                 for fatjet, subjets in relations.items():
                     fatjets[fatjet].subjetsSoftDrop = subjets


        class Iso(object):
            def __init__(self):
                self.sumpt=-9999
                self.sume=-9999
                self.num=-9999

        electrons = dict()
        if hasattr(self.cfg_ana, 'electrons'):
            event.electrons = map(Particle, store.get(self.cfg_ana.electrons))
            event.electrons.sort(reverse=True)
            for ele in event.electrons:
                ele.iso = Iso()
                electrons[ele]=ele
            if hasattr(self.cfg_ana, 'electronITags'):
                for ele in store.get(self.cfg_ana.electronITags):
                    electrons[Particle(ele.particle())].iso = Iso()
                    electrons[Particle(ele.particle())].iso.sumpt = electrons[Particle(ele.particle())].pt()*ele.tag()
            if hasattr(self.cfg_ana, 'electronsToMC'):
                for ele in store.get(self.cfg_ana.electronsToMC):
                    if ele.sim() and ele.rec():
                        electrons[Particle(ele.rec())].gen = Particle(ele.sim())

        muons = dict()
        if hasattr(self.cfg_ana, 'muons'):
            event.muons = map(Particle, store.get(self.cfg_ana.muons))
            event.muons.sort(reverse=True)   
            for mu in event.muons:
                mu.iso = Iso()
                muons[mu]=mu
            if hasattr(self.cfg_ana, 'muonITags'):
                for mu in store.get(self.cfg_ana.muonITags):
                    muons[Particle(mu.particle())].iso = Iso()
                    muons[Particle(mu.particle())].iso.sumpt = muons[Particle(mu.particle())].pt()*mu.tag()
            if hasattr(self.cfg_ana, 'muonsToMC'):
                for mu in store.get(self.cfg_ana.muonsToMC):
                    if mu.sim() and mu.rec():
                        muons[Particle(mu.rec())].gen = Particle(mu.sim())


        photons = dict()
        if hasattr(self.cfg_ana, 'photons'):
            event.photons = map(Particle, store.get(self.cfg_ana.photons))
            event.photons.sort(reverse=True)   
            for pho in event.photons:
                pho.iso = Iso()
                photons[pho]=pho
            if hasattr(self.cfg_ana, 'photonITags'):
                for pho in store.get(self.cfg_ana.photonITags):
                    photons[Particle(pho.particle())].iso = Iso()
                    photons[Particle(pho.particle())].iso.sumpt = photons[Particle(pho.particle())].pt()*pho.tag()

            # a single reco photon can have relation to multiple sim particle (ele, pho)
            # reco photon will thus have a list of gen particles attached		
            if hasattr(self.cfg_ana, 'photonsToMC'):
                from collections import defaultdict
                relations = defaultdict(list)
                for pho in store.get(self.cfg_ana.photonsToMC):
                    if pho.sim() and pho.rec():
                        relations[Particle(pho.rec())].append(Particle(pho.sim()))
                for rec, sim in relations.items():
                    photons[rec].gen = sim


        if hasattr(self.cfg_ana, 'pfcharged'):
            pfcharged  = get_collection(Particle, 'pfcharged', False)
        if hasattr(self.cfg_ana, 'pfphotons'):
            pfphotons  = get_collection(Particle, 'pfphotons', False)
        if hasattr(self.cfg_ana, 'pfneutrals'):
            pfneutrals = get_collection(Particle, 'pfneutrals', False)


        met = get_collection(Met, 'met', False)
        if met:
            event.met = event.met[0]
