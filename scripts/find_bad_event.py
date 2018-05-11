import ROOT, os, sys
from ROOT import TFile

####################
# excute example
####################
# command :
# python find_bad_event.py path_to_output_of_your_batch_jobs_containing_Chunks
#
# read the list of corrupted tree.root files in ./diagnostic.txt
# it has been found that Chunk are OK but hadd is making the issue

useChunk=False

####################
# make trees list
####################
path = sys.argv[1] 
the_file = ""
Trees = []
for subdir, dirs, files in os.walk(path) :
  for file in files :
    if file.find("tree.root") >= 0 :
      the_file = os.path.join(subdir, file)
      if useChunk==False and the_file.find("Chunk") >= 0 : continue
      Trees.append(the_file)

####################
# check the trees
####################
out_file = open("diagnostic.txt","w")
for tree in Trees :
  print "check tree "+str(Trees.index(tree)+1)+"/"+str(len(Trees))
  rf = TFile(tree)
  t = rf.Get("events")
  numberOfEntries = t.GetEntries()
  bad_status = False
  show_every=5
  count=1
  for entry in xrange(numberOfEntries) :
      ratio=100.*float(entry)/float(numberOfEntries)
      if ratio>show_every*count :
        print "Done "+str(int(ratio))+"% ("+str(entry)+"/"+str(numberOfEntries)+")"
        count+=1
      bad_event_status = t.GetEntry(entry)
      if bad_event_status == -1 :
        bad_status = True
        break
  txt_OK="OK"
  if bad_status == True : txt_OK="bad"
  out_file.write(txt_OK+" "+tree+" ("+str(numberOfEntries)+" entries)\n")
out_file.close()

