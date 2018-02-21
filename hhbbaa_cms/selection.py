from heppy.framework.analyzer import Analyzer
from heppy.statistics.counter import Counter
from heppy.utils.deltar import deltaR

class Selection(Analyzer):

    def beginLoop(self, setup):
        super(Selection, self).beginLoop(setup)
        self.counters.addCounter('cut_flow') 
        self.counters['cut_flow'].register('All events')

    def process(self, event):
        self.counters['cut_flow'].inc('All events')
        return True
