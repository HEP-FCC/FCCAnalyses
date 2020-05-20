from heppy.framework.analyzer import Analyzer
from heppy.statistics.counter import Counter

class Selection(Analyzer):

    def beginLoop(self, setup):
        super(Selection, self).beginLoop(setup)
        self.counters.addCounter('cut_flow') 
        self.counters['cut_flow'].register('All events')
        self.counters['cut_flow'].register('At least 4 jets')
        self.counters['cut_flow'].register('At least 1 b-jet')
        self.counters['cut_flow'].register('Exactly 1 lepton')
        self.counters['cut_flow'].register('MET > 20GeV')


    def process(self, event):
        self.counters['cut_flow'].inc('All events')



        #select events with at least 4 jets
        if len(event.jets_nomuonnoelectron)<4:
            return False
        self.counters['cut_flow'].inc('At least 4 jets')

        #select events with at least 1 b-jet
        if len(event.selected_bs)<1:
            return False
        self.counters['cut_flow'].inc('At least 1 b-jet')

        #select events with exactly 1 lepton
        if (len(event.dressed_electrons) + len(event.dressed_muons) != 1 ):
            return False
        self.counters['cut_flow'].inc('Exactly 1 lepton')

        #select events with MET>20GeV
        if event.met.pt()<20.:
            return False
        self.counters['cut_flow'].inc('MET > 20GeV')

        
        return True
