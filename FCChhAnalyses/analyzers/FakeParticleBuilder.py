from heppy.framework.analyzer import Analyzer
import collections

import math
import random

class FakeParticleBuilder(Analyzer):
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
    # assume sum of bias is 1
    # returns postion of jet according to fake probabilities
    
    def roll(self, massDist):
        randRoll = random.random() # in [0,1)
        sum = 0
        result = 0
        for mass in massDist:
            sum += mass
            if randRoll < sum:
                return result
            result+=1

    def process(self, event):
        '''event must contain
        
        * self.cfg_ana.input_objects: collection of objects to be selected
           These objects must be usable by the filtering function
           self.cfg_ana.filter_func.
        '''
        input_collection = getattr(event, self.cfg_ana.input_objects)
        
        output_collection = []
        weight_collection = []
        fake_collection = []

	'''probabilities = []
        for jet in input_collection:
	     probabilities.append(self.cfg_ana.fake_prob(jet.pt()))
	     print jet.pt(), self.cfg_ana.fake_prob(jet.pt())'''
	
	prob_dict = { jet : self.cfg_ana.fake_prob(jet.pt()) for jet in input_collection}

        #print '-----------------------------'
	
	sum_prob = 0
	for key, val in prob_dict.iteritems():
	   sum_prob += val

	normalized_prob_dict = { jet : self.cfg_ana.fake_prob(jet.pt())/sum_prob for jet in input_collection}
	
	# compute event weight
	weight_factor = 0
	
	for key, val in prob_dict.iteritems():
	    weight_factor += val
	    #print key.pt(), val, weight_factor

	#print ''
	
	# taking the sum works only for very small probabilites!!!
	sum_probabilities = 0
	for key, val in normalized_prob_dict.iteritems():
	   sum_probabilities += val
	   #print key.pt(), sum_probabilities
        
	#print ''

        if len(input_collection) > 0:
	    position = self.roll(normalized_prob_dict.values())
	
	    #print position

            # fill output jet collection (without converted jet)
	    output_collection = [obj for obj in input_collection if obj != input_collection[position]]
	
	    #for jet in output_collection:
	        #print jet.pt()	 
				 
            # fill output fake collection
	    fake_collection.append(input_collection[position])

            # fill new event weight
            event.weight = event.weight*sum_prob

            #print event.weight, event.weight*sum_prob
	setattr(event, self.cfg_ana.output_jets, output_collection)
	setattr(event, self.cfg_ana.output_fakes, fake_collection)
	#setattr(event, self.cfg_ana.output_weights, weight_collection)

	#print position, event.weight*sum_prob
