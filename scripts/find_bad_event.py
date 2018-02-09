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
      Trees.append(the_file)

####################
# check the trees
####################
out_file = open("diagnostic.txt","w")
out_file.write("The tree list with event issue found :\n")
for tree in Trees :
  print "check tree "+str(Trees.index(tree)+1)+"/"+str(len(Trees))
  rf = TFile(tree)
  t = rf.Get("events")
  numberOfEntries = t.GetEntries()
  bad_status = False
  for entry in xrange(numberOfEntries) :
      bad_event_status = t.GetEntry(entry)
      if bad_event_status == -1 :
        bad_status = True
        break
  if bad_status == True : out_file.write(tree+"\n")
out_file.close()

