import sys
import os
import argparse
import multiprocessing as mp
import subprocess
from subprocess import Popen, PIPE
from datetime import date
import time


# ________________________________________________________________________________
def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--indir",
        help="path input directory",
        default="/eos/experiment/fcc/ee/generation/DelphesEvents/pre_fall2022_training/IDEA/",
    )
    parser.add_argument(
        "--outdir",
        help="path output directory",
        default="/eos/experiment/fcc/ee/jet_flavour_tagging/pre_fall2022_training/IDEA/",
    )
    parser.add_argument("--nev", help="number of events", type=int, default=1000000)
    parser.add_argument("--fsplit", help="fraction train/test", type=float, default=0.9)
    parser.add_argument("--dry", help="dry run ", action='store_true')

    args = parser.parse_args()
    inDIR = args.indir
    outDIR = args.outdir

    # create necessary subdirectories
    actualDIR = subprocess.check_output(["bash", "-c", "pwd"], universal_newlines=True)[:-1]
    username = subprocess.check_output(["bash", "-c", "echo $USER"], universal_newlines=True)[:-1]
    today = date.today().strftime("%Y%b%d")
    subdir = username + "_" + today
    subprocess.call(["bash", "-c", "mkdir -p {}".format(subdir)], cwd=outDIR)
    OUTDIR = outDIR + username + "_" + today + "/"
    print(OUTDIR)

    # set total number of events
    N = args.nev
    frac_split = args.fsplit
    N_split = int(frac_split * N)

    print("")
    print("=================================================")
    print("")
    print(" INDIR           = {}".format(inDIR))
    print(" OUTDIR          = {}".format(OUTDIR))
    print(" NEVENTS         = {}".format(N))
    print(" FRAC SPLIT      = {}".format(frac_split))
    print("")

    # compile stage2 c++ code
    cmd_compile = "g++ -o stage2 stage2.cpp `root-config --cflags --libs` -Wall"
    subprocess.check_call(cmd_compile, shell=True, stdout=None, stderr=None)

    # create commands
    #cmdbase_stage1 = "fccanalysis run stage1.py --nevents {}".format(N)
    cmdbase_stage1 = "fccanalysis run stage1.py".format(N)
    opt1_out = " --output {}stage1_ee_ZH_vvCLASS.root ".format(OUTDIR)
    opt1_in = " --files-list {}p8_ee_ZH_Znunu_HCLASS_ecm240/*.root ".format(inDIR)
    wait = " ; sleep 30;"
    cmd_stage1 = cmdbase_stage1 + opt1_out + opt1_in

    cmdbase_stagentuple = "./stage2 DIRstage1_ee_ZH_vvCLASS.root  DIRntuple_MOD_ee_ZH_vvCLASS.root "
    cmd_stage2 = cmdbase_stagentuple.replace("DIR", OUTDIR)

    samples = ["bb", "cc", "ss", "gg", "qq"]
    mods = ["train", "test"]

    # create files storing stdout and stderr
    list_stdout = [open(OUTDIR + "{}_stdout.txt".format(sample), "w") for sample in samples]
    list_stderr = [open(OUTDIR + "{}_stderr.txt".format(sample), "w") for sample in samples]

    ###=== RUN STAGE 1
    for i, sample in enumerate(samples):

        if sample == "qq":
            cmd_stage1_f = (
                cmdbase_stage1
                + opt1_out.replace("CLASS", "qq")
                + " --files-list {}p8_ee_ZH_Znunu_Huu_ecm240/*.root {}p8_ee_ZH_Znunu_Hdd_ecm240/*.root".format(
                    inDIR, inDIR
                )
            )
        else:
            cmd_stage1_f = cmd_stage1.replace("CLASS", sample)

        print(cmd_stage1_f)
        # run stage1
        start1_time = time.time()
        if not args.dry:    
            subprocess.check_call(
                cmd_stage1_f, shell=True, stdout=list_stdout[i], stderr=list_stderr[i]
            )
        end1_time = time.time()
        list_stdout[i].write("Stage1 time: {} \n".format(end1_time - start1_time))

    ###=== RUN STAGE 2
    threads = []
    for i, sample in enumerate(samples):

        cmd_stage2_train = cmd_stage2.replace("CLASS", sample).replace(
            "MOD", mods[0]
        ) + " {} {} ".format(0, N_split)
        cmd_stage2_test = cmd_stage2.replace("CLASS", sample).replace(
            "MOD", mods[1]
        ) + " {} {} ".format(N_split, N)
        print(cmd_stage2_train)
        print(cmd_stage2_test)
         
        if not args.dry:
            thread = mp.Process(
                target=ntuplizer,
                args=(cmd_stage2_train, cmd_stage2_test, list_stdout[i], list_stderr[i]),
            )
            thread.start()
            threads.append(thread)

    for proc in threads:
        proc.join()


    for i in range(len(list_stdout)):
        list_stdout[i].close()
        list_stderr[i].close()


# ________________________________________________________________________________
def ntuplizer(cmd_stage2_train, cmd_stage2_test, f_stdout, f_stderr):

    start2_time = time.time()
    subprocess.check_call(cmd_stage2_train, shell=True, stdout=f_stdout, stderr=f_stderr)
    subprocess.check_call(cmd_stage2_test, shell=True, stdout=f_stdout, stderr=f_stderr)
    end2_time = time.time()
    f_stdout.write("stage2 time (run only): {} \n".format(end2_time - start2_time))


# _______________________________________________________________________________________
if __name__ == "__main__":
    main()

