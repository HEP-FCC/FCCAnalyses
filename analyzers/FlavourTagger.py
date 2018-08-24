from heppy.framework.analyzer import Analyzer
from heppy.utils.deltar import deltaR

import collections

import math
import random

class FlavourTagger(Analyzer):

    def process(self, event):

        output_jets = []

        jet_collection = getattr(event, self.cfg_ana.input_jets)
        gen_collection = getattr(event, self.cfg_ana.input_genparticles)

        drMax = self.cfg_ana.dr_match
        pdgTags = self.cfg_ana.pdg_tags
        ptratio = self.cfg_ana.ptr_min

        # need to be specified in order of priority (taus need to be fixed by including visible decay products, 
        # right now includes all decays)
        
        for jet in jet_collection:
           # print jet
            matched_partons = []
            #matched_pt = []
            #matched_status = []

            for part in gen_collection:
                pdg = abs(part.pdgid())

                # set to 0 pdg = 1,2,3,21
                if pdg in [3, 2, 1, 21]:
                    pdg = 0

                dR = jet.p4().DeltaR(part.p4())

                if dR < drMax and pdg in pdgTags and part.pt() > ptratio*jet.pt() :
                    matched_partons.append(pdg)
                    #print "--found : pT=",part.pt()," eta=",part.eta()," phi=",part.phi()," dR=",dR," pdg=",pdg," status=",part.status()
                   
            # put 0 as a default (even when no match is found)
            pdgBest = 0
            matched_partons.sort(key=lambda x: pdgTags.index(x))
            if len(matched_partons) > 0:
               pdgBest = matched_partons[0]

            setattr(jet, 'flavour', pdgBest)
            output_jets.append(jet)
        
        setattr(event, self.cfg_ana.output_jets, output_jets)
