import uproot
from coffea.nanoevents import NanoEventsFactory, BaseSchema
import awkward as ak

# https://github.com/scikit-hep/uproot4/issues/122
uproot.open.defaults["xrootd_handler"] = uproot.source.xrootd.MultithreadedXRootDSource

filename = "p8_ee_Zuds_ecm91_k.root"
file = uproot.open(filename)
events = NanoEventsFactory.from_root(
    file,
    entry_stop=100000,
    #metadata={"dataset": "DoubleMuon"},
    schemaclass=BaseSchema,
    treepath='/events'
).events()
K0s_ = (events['Ks2pipi_indices'][:]>-1)*1
print(ak.max(ak.sum(K0s_, axis=1)))
#p = MyProcessor()
#out = p.process(events)
#out
