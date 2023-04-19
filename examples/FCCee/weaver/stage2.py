import sys
from array import array
from ROOT import TFile, TTree
from examples.FCCee.weaver.config import variables_pfcand, variables_jet, flavors

debug = False

if len(sys.argv) < 2:
    print(" Usage: stage2.py input_file output_file n_start n_events")
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]
n_start = int(sys.argv[3])
n_final = int(sys.argv[4])
n_events = n_final - n_start

# Opening the input file containing the tree (output of stage1.py)
infile = TFile.Open(input_file, "READ")

ev = infile.Get("events")
numberOfEntries = ev.GetEntries()

## basic checks
if n_final > n_start + numberOfEntries:
    print("ERROR: requesting too many events. This file only has {}".format(numberOfEntries))
    sys.exit()

branches_pfcand = list(variables_pfcand.keys())
branches_jet = list(variables_jet.keys())

if len(branches_jet) == 0:
    print("ERROR: branches_jet is empty ...")
    sys.exit()

if len(branches_pfcand) == 0:
    print("ERROR: branches_pfcand is empty ...")
    sys.exit()

# print("")
# print("-> number of events: {}".format(numberOfEntries))
# print("-> requested to run over [{},{}] event range".format(n_start, n_final))

# branches_pfcand = [branches_pfcand[0]]
# branches_jet = [branches_jet[-1]]

## define variables for output tree
maxn = 500

match_flavor = dict()
for f in flavors:
    match_flavor[f] = False
    if "H{}{}".format(f, f) in input_file:
        match_flavor[f] = True

if True in match_flavor.values():
    f0 = list(match_flavor.keys())[list(match_flavor.values()).index(True)]
    # print("producing  '{}-flavor' jets ...".format(f0, f0))
else:
    print("ERROR: could not infer jet flavor from file name")
    str_err = "ERROR: please provide input file containing: "
    for f in flavors:
        str_err += "H{}{} ".format(f, f)

## output jet-wise tree
out_root = TFile(output_file, "RECREATE")
t = TTree("tree", "tree with jets")

jet_array = dict()
for f in flavors:
    b = "recojet_is{}".format(f.upper())
    jet_array[b] = array("i", [0])
    t.Branch(b, jet_array[b], "{}/I".format(b))
for b in branches_jet:
    jet_array[b] = array("f", [0])
    t.Branch(b, jet_array[b], "{}/F".format(b))

## need this branch to define pfcand branches
jet_npfcand = array("i", [0])
t.Branch("jet_npfcand", jet_npfcand, "jet_npfcand/I")

pfcand_array = dict()
for b in branches_pfcand:
    pfcand_array[b] = array("f", maxn * [0])
    t.Branch(b, pfcand_array[b], "{}[jet_npfcand]/F".format(b))

if debug:
    for key, item in jet_array.items():
        print(key)
    for key, item in pfcand_array.items():
        print(key)

# Loop over all events
for entry in range(n_start, n_final):
    # Load selected branches with data from specified event

    # if (entry+1)%100 == 0:
    # if (entry + 1) % 1000 == 0:
    #    print(" ... processed {} events ...".format(entry + 1))

    ev.GetEntry(entry)

    njets = len(getattr(ev, branches_jet[0]))

    ## loop over jets
    for j in range(njets):

        ## fill jet-based quantities
        for f in flavors:
            name = "recojet_is{}".format(f.upper())
            jet_array[name][0] = int(match_flavor[f])
            if debug:
                print("   jet:", j, name, jet_array[name][0])

        for name in branches_jet:
            jet_array[name][0] = getattr(ev, name)[j]
            if debug:
                print("   jet:", j, name, getattr(ev, name)[j])

        ## loop over constituents
        jet_npfcand[0] = len(getattr(ev, branches_pfcand[0])[j])
        for k in range(jet_npfcand[0]):
            for name in branches_pfcand:
                pfcand_array[name][k] = getattr(ev, name)[j][k]
                if debug:
                    print("       const:", k, name, getattr(ev, name)[j][k])

        ## fill tree at every jet
        t.Fill()

# write tree
t.SetDirectory(out_root)
t.Write()
