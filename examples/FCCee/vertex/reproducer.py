import ROOT
ROOT.gSystem.Load("libFCCAnalyses")
ROOT.gInterpreter.ProcessLine("#include \"VertexingACTS.h\"")

tf = ROOT.TFile("/eos/experiment/fcc/ee/generation/DelphesEvents/fcc_tmp/p8_ee_Zuds_ecm91/events_199980034.root")
tt = tf.Get("events")

print (ROOT.VertexingACTS.initialize)
count=0
for event in tt:
    
    print (type(event.EFlowTrack_1))
    count +=1
    ROOT.VertexingACTS.initialize(event.EFlowTrack_1)
    if count>10: break
