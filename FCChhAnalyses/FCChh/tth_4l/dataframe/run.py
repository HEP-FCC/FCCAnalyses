"""
Run the FCChh tth_4l tdataframe analysis on all samples.
"""



import os
import subprocess
import sys

def chunks(l, n):
  """Yield successive n-sized chunks from l."""
  for i in xrange(0, len(l), n):
    yield l[i:i + n]


# expects processname as command line argument, p.ex m
process = sys.argv[1]

filelist = subprocess.check_output(['eos ls /eos/experiment/fcc/hh/generation/DelphesEvents/fcc_v02/' + process + '/events_00*.root', ""], shell=True)

filechunks = [e for e in chunks(filelist.split("\n"),10) if e]

NUM_CPUS = 15 #  "None"  defaults to all available

def worker(f1, f2):

  # bash command to run analysis
  os.system("fcc_ana_tth_4l " + "tree_" + f1[0].split("events_")[1] + " " +  "  ".join("root://eospublic//eos/experiment/fcc/hh/generation/DelphesEvents/fcc_v02/"+ process +"/" + _f for _f in f1))

def run(pool): 
     f2 = None # not used. TODO: Remove
     for f1 in filechunks:
               pool.apply_async(worker, args=(f1,f2))

if __name__ == "__main__":
     import multiprocessing as mp
     pool = mp.Pool(NUM_CPUS)
     run(pool)
     pool.close()
     pool.join()
