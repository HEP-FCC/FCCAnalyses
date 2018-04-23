from heppy.framework.analyzer import Analyzer
from heppy.statistics.counter import Counter

class Selection(Analyzer):

    def beginLoop(self, setup):
        super(Selection, self).beginLoop(setup)
        self.counters.addCounter('cut_flow') 
        self.counters['cut_flow'].register('All events')
        self.counters['cut_flow'].register('At least one H -> mu+ mu- candidates')

    def process(self, event):
        self.counters['cut_flow'].inc('All events')

        higgses = event.higgses

        #select events with at least one Z -> l+ l- candidates
        if (len(higgses) < 1):
           return False
        self.counters['cut_flow'].inc('At least one H -> mu+ mu- candidates')
        
        return True
