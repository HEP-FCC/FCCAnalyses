'''Remove particles from a collection.'''

from heppy.framework.analyzer import Analyzer
import copy
import itertools


class ExtraLeptons(Analyzer):

    def process(self, event):
        '''Process the event.
        
        The event must contain:
         - self.cfg_ana.inputA
         - self.cfg_ana.inputB
         
        This method creates:
         - event.<self.cfg_ana.output>
        '''
        inputA = getattr(event, self.cfg_ana.inputA)
        inputB = getattr(event, self.cfg_ana.inputB)
        
        if len(inputB) > 1:
          output = [ ptc for ptc in inputA if ptc not in 
              [
                inputB[0].legs[0],
                inputB[0].legs[1],
                inputB[1].legs[0],
                inputB[1].legs[1],
              ]
            ]
        else:
          output = []
        
        if hasattr(self.cfg_ana, 'sort_key'):
            output.sort(key=self.cfg_ana.sort_key, reverse=True)
        setattr(event, self.cfg_ana.extra_leptons, output)
