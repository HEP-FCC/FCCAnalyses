from heppy.framework.analyzer import Analyzer
from heppy.particles.tlv.resonance import Resonance2 as Resonance

import pprint 
import itertools

class LeptonicHiggsBuilder(Analyzer):
    '''Builds a list of Z resonances from an input lepton collection. 
       Elements in this list consist in pairs of leptons. A given lepton can appear
       only in one pair of the list.

    Example:

    from heppy.analyzers.LeptonicHiggsBuilder import LeptonicHiggsBuilder
    zeds = cfg.Analyzer(
      LeptonicHiggsBuilder,
      output = 'zeds',
      leptons = 'leptons',
    )

    * output : resulting Z resonances are stored in this collection, 
    sorted according to their distance to the nominal Z mass. The first 
    resonance in this collection is thus the best one. 
    
    Additionally, a collection zeds_legs (in this case) is created to contain the 
    legs of the best resonance. 

    * leptons : collection of leptons that will be combined into resonances.

    '''

    def matches(self, zed, zeds) :
        for z in zeds:    
            if ( zed.leg1() is z.leg1() or 
                 zed.leg1() is z.leg2() or 
                 zed.leg2() is z.leg1() or 
                 zed.leg2() is z.leg2() ) : 
                return True
		
    def isLeptonic(self, zed) :
        if ( zed.leg1().pdgid() == -zed.leg2().pdgid() ) :
            return True

    def process(self, event):
        legs = getattr(event, self.cfg_ana.leptons)

        uncleaned_zeds = []

        # first form all possible combinations, regardless of flavor or charge
        for leg1, leg2 in itertools.combinations(legs,2):
            uncleaned_zeds.append( Resonance(leg1, leg2, 25) )

        # check that leptons occur only in one pair and that they are same flavor, opp charge. 
        zeds = []
        for z in uncleaned_zeds:
           if not self.matches(z, zeds) : zeds.append(z) 
        
        # sorting according to distance to nominal mass
        nominal_mass = 125
        zeds.sort(key=lambda x: abs(x.m()-nominal_mass))
        setattr(event, self.cfg_ana.output, zeds)
        
        # getting legs of best resonance
        legs = []
        if len(zeds):
            legs = zeds[0].legs
        setattr(event, '_'.join([self.cfg_ana.output, 'legs']), legs)

