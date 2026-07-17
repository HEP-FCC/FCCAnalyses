"""Flatten the per-event stage1 tree to a per-jet ntuple for training.

Reads the stage1 `events` tree with uproot (vectorised) and writes the per-jet
`tree` with PyROOT. The one-hot `recojet_is{FLAVOUR}` label is inferred from the
input file name (`H{f}{f}` for Higgs samples, `_ee_{f}{f}_` for Z samples).

Usage: python stage2.py input_file output_file n_start n_final

Note: a previous per-entry PyROOT implementation read RVec<RVec<float>> branches
with nested cppyy indexing, which corrupts the heap (segfault on tau samples).
Reading the branches vectorised with uproot avoids that and is much faster.
"""
import sys
import numpy as np
import uproot
import awkward as ak
from array import array
from ROOT import TFile, TTree
from examples.FCCee.weaver.config import variables_pfcand, variables_jet, flavors

if len(sys.argv) < 5:
    print(" Usage: python stage2.py input_file output_file n_start n_final")
    sys.exit(1)

input_file, output_file = sys.argv[1], sys.argv[2]
n_start, n_final = int(sys.argv[3]), int(sys.argv[4])

branches_pfcand = list(variables_pfcand.keys())
branches_jet = list(variables_jet.keys())
if not branches_jet or not branches_pfcand:
    print("ERROR: empty branch list from config")
    sys.exit(1)

## jet flavour from the file name: "H{f}{f}" (Higgs) or "_ee_{f}{f}_" (Z)
match_flavor = {}
for f in flavors:
    ff = f + f
    match_flavor[f] = ("H{}".format(ff) in input_file) or ("_ee_{}_".format(ff) in input_file)
if True not in match_flavor.values():
    print("ERROR: could not infer jet flavor from file name: {}".format(input_file))
    sys.exit(1)

t = uproot.open(input_file)["events"]
n_final = min(n_final, t.num_entries)

## read once (jagged: event -> jet -> constituent), restricted to the event range
arr_jet = {b: t[b].array(library="ak", entry_start=n_start, entry_stop=n_final) for b in branches_jet}
arr_pf = {b: t[b].array(library="ak", entry_start=n_start, entry_stop=n_final) for b in branches_pfcand}

## flatten the event axis -> one entry per jet
jet_flat = {b: ak.to_numpy(ak.flatten(arr_jet[b])).astype(np.float64) for b in branches_jet}
pf_perjet = {b: ak.flatten(arr_pf[b], axis=1) for b in branches_pfcand}
npf = ak.to_numpy(ak.num(pf_perjet[branches_pfcand[0]], axis=1))
njets_tot = int(npf.size)

maxn = 500
out_root = TFile(output_file, "RECREATE")
tr = TTree("tree", "tree with jets")

jet_array = {}
for f in flavors:
    b = "recojet_is{}".format(f.upper())
    jet_array[b] = array("i", [int(match_flavor[f])])
    tr.Branch(b, jet_array[b], "{}/I".format(b))
for b in branches_jet:
    jet_array[b] = array("f", [0])
    tr.Branch(b, jet_array[b], "{}/F".format(b))

jet_npfcand = array("i", [0])
tr.Branch("jet_npfcand", jet_npfcand, "jet_npfcand/I")

pf_buf, pf_np = {}, {}
for b in branches_pfcand:
    pf_buf[b] = array("f", maxn * [0.0])
    tr.Branch(b, pf_buf[b], "{}[jet_npfcand]/F".format(b))
    pf_np[b] = np.frombuffer(pf_buf[b], dtype=np.float32)

## contiguous per-constituent data + per-jet offsets, to fill the fixed-size buffers
pf_offsets = np.zeros(njets_tot + 1, dtype=np.int64)
np.cumsum(npf, out=pf_offsets[1:])
pf_flat = {b: ak.to_numpy(ak.flatten(pf_perjet[b], axis=1)).astype(np.float32) for b in branches_pfcand}

for j in range(njets_tot):
    for b in branches_jet:
        jet_array[b][0] = jet_flat[b][j]
    n = int(min(npf[j], maxn))
    jet_npfcand[0] = n
    o = pf_offsets[j]
    for b in branches_pfcand:
        pf_np[b][:n] = pf_flat[b][o:o + n]
    tr.Fill()

tr.SetDirectory(out_root)
tr.Write()
out_root.Close()
print("wrote {} jets -> {}".format(njets_tot, output_file))
