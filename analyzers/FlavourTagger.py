from heppy.framework.analyzer import Analyzer
from heppy.utils.deltar import deltaR

import collections

import math
import random

class FlavourTagger(Analyzer):
    '''Select objects from the input_objects collection 
    and store them in the output collection. The objects are not copied
    in the process. 

    Example:
    
    from heppy.analyzers.Selector import Selector
    def is_lepton(ptc):
      """Returns true if the particle energy is larger than 5 GeV
      and if its pdgid is +-11 (electrons) or +-13 (muons)
      return ptc.e()> 5. and abs(ptc.pdgid()) in [11, 13]

    leptons = cfg.Analyzer(
      Selector,
      'sel_leptons',
      output = 'leptons',
      input_objects = 'rec_particles',
      filter_func = is_lepton 
      )

    * input_objects : the input collection.
        If a dictionary, the filtering function is applied to the dictionary values,
        and not to the keys.

    * output : the output collection

    * filter_func : a function object.
    IMPORTANT NOTE: lambda statements should not be used, as they
    do not work in multiprocessing mode. looking for a solution...
    
    '''

    def process(self, event):
        '''event must contain
        
        * self.cfg_ana.input_objects: collection of objects to be selected
           These objects must be usable by the filtering function
           self.cfg_ana.filter_func.
        '''

        output_jets = []

        jet_collection = getattr(event, self.cfg_ana.input_jets)
        gen_collection = getattr(event, self.cfg_ana.input_genparticles)

        pt_ordered = self.cfg_ana.pt_ordered
        leading_pt = self.cfg_ana.leading_pt

        drMax = self.cfg_ana.dr_match
        pdgTags = self.cfg_ana.pdg_tags
        ptratio = self.cfg_ana.ptr_min

        # need to be specified in order of priority (taus need to be fixed by including visible decay products, 
        # right now includes all decays)
        
        for jet in jet_collection:
           # print jet
            matched_partons = []
            matched_pt = []
            matched_status = []

            for part in gen_collection:
                pdg = abs(part.pdgid())

                # set to 0 pdg = 1,2,3,21
                if pdg in [3, 2, 1, 21]:
                    pdg = 0

                dR = jet.p4().DeltaR(part.p4())

                if dR < drMax and pdg in pdgTags and part.pt() > ptratio*jet.pt() :
                    matched_partons.append(pdg)
                    matched_pt.append(part.pt())
                    matched_status.append(part.status())
                    #print part
            # put 0 as a default (even when no match is found)
            pdgBest = 0
            
            #print 'matched parton   ',matched_partons
            #print 'matched pt       ',matched_pt
            #print 'matched status   ',matched_status

            if len(matched_pt)>0 and pt_ordered:
                matched_pt , matched_partons = zip(*sorted(zip(matched_pt, matched_partons), reverse=True))
                #print 'matched parton ord  ',matched_partons
                #print 'matched pt     ord  ',matched_pt

            # set pdgBest to highest rank tag number
            for pdg in pdgTags:
                for part_pdg in matched_partons:
                    if part_pdg == pdg:
                        pdgBest = pdg
                        break
                break
            
            if leading_pt and len(matched_pt)>0:
                pdgBest = matched_partons[0]

            #print matched_partons
            #print 'best match', pdgBest
            
            setattr(jet, 'flavour', pdgBest)
            output_jets.append(jet)
        
        setattr(event, self.cfg_ana.output_jets, output_jets)
