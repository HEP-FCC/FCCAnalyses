from heppy.framework.analyzer import Analyzer
from heppy.particles.fcc.particle import Particle
from heppy.particles.fcc.jet import Jet
from heppy.particles.fcc.vertex import Vertex 
from heppy.particles.fcc.particle_MCparticle_link import ParticleMCParticleLink
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


        def get_tag(tag_label):
            pycoll = None
            if hasattr(self.cfg_ana, tag_label):
                tag_name = getattr( self.cfg_ana, tag_label)
                tags = store.get( tag_name )
                if tags == None:
                    raise MissingCollection(
                        'tag {} is missing'.format(tag_name)
                        )
            return tags


        # store only 1st event weight for now
        event.weight = - 999.
        if hasattr(self.cfg_ana, 'weights'):
            coll_name = getattr( self.cfg_ana, 'weights' )
            weightcoll = store.get( coll_name )
            if weightcoll:
                event.weight = weightcoll[0].value()

        if hasattr(self.cfg_ana, 'gen_particles'):
            get_collection(Particle, 'gen_particles')

        if hasattr(self.cfg_ana, 'rec_particles'):
            get_collection(Particle, 'rec_particles')
        
        if hasattr(self.cfg_ana, 'gen_rec_links'):
            get_collection(ParticleMCParticleLink, 'gen_rec_links')

        if hasattr(self.cfg_ana, 'gen_vertices'):
            get_collection(Vertex, 'gen_vertices', False)

        if hasattr(self.cfg_ana, 'gen_jets'):
            get_collection(Jet, 'gen_jets')

        
        # last empty entries allows for bk compatibility
        algos = ['pf', 'calo', 'trk', '']
        cones = ['02', '04', '08', '15', '']
        

        for algo in algos:
            for cone in cones:
                jets = dict()

                if hasattr(self.cfg_ana, '{}jets{}'.format(algo,cone)):
                   jetcoll = get_collection(Jet, '{}jets{}'.format(algo,cone))
                   if jetcoll:
                       for jet in jetcoll:
                           jets[jet] = jet

                       if hasattr(self.cfg_ana, '{}jetsFlavor{}'.format(algo,cone)):
                           for flav in get_tag('{}jetsFlavor{}'.format(algo,cone)):
                               jets[Jet(flav.jet())].tags['flav'] = flav.tag()

                       if hasattr(self.cfg_ana, '{}bTags{}'.format(algo,cone)):
                           for bjet in get_tag('{}bTags{}'.format(algo,cone)):
                               jets[Jet(bjet.jet())].tags['bf'] = bjet.tag()

                       if hasattr(self.cfg_ana, '{}cTags{}'.format(algo,cone)):
                           for cjet in get_tag('{}cTags{}'.format(algo,cone)):
                               jets[Jet(cjet.jet())].tags['cf'] = cjet.tag()

                       if hasattr(self.cfg_ana, '{}tauTags{}'.format(algo,cone)):
                           for taujet in get_tag('{}tauTags{}'.format(algo,cone)):
                               jets[Jet(taujet.jet())].tags['tauf'] = taujet.tag()

                       # store N-subjettiness up to 3
                       if hasattr(self.cfg_ana, '{}jetsOneSubJettiness{}'.format(algo,cone)):
                           for tjet in get_tag('{}jetsOneSubJettiness{}'.format(algo,cone)):
                               jets[Jet(tjet.jet())].tau1 = tjet.tag()

                       if hasattr(self.cfg_ana, '{}jetsTwoSubJettiness{}'.format(algo,cone)):
                           for tjet in get_tag('{}jetsTwoSubJettiness{}'.format(algo,cone)):
                               jets[Jet(tjet.jet())].tau2 = tjet.tag()
                       if hasattr(self.cfg_ana, '{}jetsThreeSubJettiness{}'.format(algo,cone)):
                           for tjet in get_tag('{}jetsThreeSubJettiness{}'.format(algo,cone)):
                               jets[Jet(tjet.jet())].tau3 = tjet.tag()

                       # store subjets according to various algorithms
                       # the first entry of subjets list is the "cleaned" fastjet itself
                       from collections import defaultdict
                       # trimming
                       if hasattr(self.cfg_ana, '{}subjetsTrimming{}'.format(algo,cone)) and hasattr(self.cfg_ana, '{}subjetsTrimmingTagged{}'.format(algo,cone)):
                            relations = defaultdict(list)
                            for tjet in get_tag('{}subjetsTrimmingTagged{}'.format(algo,cone)):
                                 for i in range(tjet.subjets_size()):
                                     relations[Jet(tjet.jet())].append(Jet(tjet.subjets(i)))
                            for jet, subjets in relations.items():
                                jets[jet].subjetsTrimming = subjets

                       # pruning
                       if hasattr(self.cfg_ana, '{}subjetsPruning{}'.format(algo,cone)) and hasattr(self.cfg_ana, '{}subjetsPruningTagged{}'.format(algo,cone)):
                            relations = defaultdict(list)
                            for tjet in get_tag('{}subjetsPruningTagged{}'.format(algo,cone)):
                                 for i in range(tjet.subjets_size()):
                                     relations[Jet(tjet.jet())].append(Jet(tjet.subjets(i)))
                            for jet, subjets in relations.items():
                                jets[jet].subjetsPruning = subjets

                       # soft drop
                       if hasattr(self.cfg_ana, '{}subjetsSoftDrop{}'.format(algo,cone)) and hasattr(self.cfg_ana, '{}subjetsSoftDropTagged{}'.format(algo,cone)):
                            relations = defaultdict(list)
                            for tjet in get_tag('{}subjetsSoftDropTagged{}'.format(algo,cone)):
                                 for i in range(tjet.subjets_size()):
                                     relations[Jet(tjet.jet())].append(Jet(tjet.subjets(i)))
                            for jet, subjets in relations.items():
                                jets[jet].subjetsSoftDrop = subjets

                if hasattr(self.cfg_ana, '{}jetConst{}'.format(algo,cone)) and hasattr(self.cfg_ana, '{}jets{}'.format(algo,cone)):
                    from collections import defaultdict
                    particle_relations = defaultdict(list)
                    for tjet in store.get('{}jets{}'.format(algo,cone)):
                        for i in range(tjet.particles_size()):
                            particle_relations[Jet(tjet)].append(Particle(tjet.particles(i)))
                    for jet, particles in particle_relations.items():
                        jets[jet].jetConstituents = particles 

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
