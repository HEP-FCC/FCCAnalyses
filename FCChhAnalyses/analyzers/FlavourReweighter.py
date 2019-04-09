from heppy.framework.analyzer import Analyzer
from heppy.utils.deltar import deltaR

import collections

import math
import random

class FlavourReweighter(Analyzer):

    def process(self, event):
 
        output_jets = []

        jet_collection = getattr(event, self.cfg_ana.input_jets)
        tag_rates = self.cfg_ana.tag_rates
  
        sumtag=0
        sumtag_list=[]
        pdg_list=[]
        for t in tag_rates:
            sumtag+=t[1]
            sumtag_list.append(sumtag)
            pdg_list.append(t[0])

        if abs(sumtag-1.)>0.0001: print "sum tag is greater than one, this violates unitarity!!!  ",sumtag

        for jet in jet_collection:
    
            rannum=random.uniform(0., 1.)
            for i in xrange(len(sumtag_list)):
                if sumtag_list[i]>rannum:
                    setattr(jet, 'flavour', pdg_list[i])
                    print 'ran  ',rannum,'  sumtag_list[i]  ',sumtag_list[i],'  pdg_list[i]  ',pdg_list[i]
                    output_jets.append(jet)
                    break

        setattr(event, self.cfg_ana.output_jets, output_jets)
