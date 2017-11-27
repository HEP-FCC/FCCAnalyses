from heppy.framework.analyzer import Analyzer
from heppy.statistics.counter import Counter

class Selection(Analyzer):

    def beginLoop(self, setup):
        super(Selection, self).beginLoop(setup)
        self.counters.addCounter('cut_flow') 
        self.counters['cut_flow'].register('All events')
        self.counters['cut_flow'].register('At least 2 muons')


    def process(self, event):
        self.counters['cut_flow'].inc('All events')
        
        #select events with at least 2 muons
        if len(event.selected_muons)<2:
            return False
        self.counters['cut_flow'].inc('At least 2 muons')

        return True
