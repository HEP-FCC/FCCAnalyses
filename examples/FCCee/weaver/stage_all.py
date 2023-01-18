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
    parser.add_argument("--ncpus", help="number of cpus", type=int, default=8)
    parser.add_argument("--sample", help="sample", default="p8_ee_ZH_Znunu")
    parser.add_argument("--dry", help="dry run ", action="store_true")

    ## qq is merge of uu/dd
    flavors = ["bb", "cc", "ss", "gg", "qq"]

    ## sample (CLASS)

    # sample = "wzp6_ee_nunuH"

    args = parser.parse_args()
    inDIR = args.indir
    outDIR = args.outdir
    sample = args.sample

    # create necessary subdirectories
    actualDIR = subprocess.check_output(["bash", "-c", "pwd"], universal_newlines=True)[:-1]
    username = subprocess.check_output(["bash", "-c", "echo $USER"], universal_newlines=True)[:-1]
    today = date.today().strftime("%Y%b%d")
    subdir = username + "_" + today
    subprocess.call(["bash", "-c", "mkdir -p {}".format(outDIR)])
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
    print(" NCPUS           = {}".format(args.ncpus))
    print("")

    # create commands
    # cmdbase_stage1 = "fccanalysis run stage1.py --nevents {}".format(N)
    cmdbase_stage1 = "fccanalysis run examples/FCCee/weaver/stage1.py --ncpus {}".format(args.ncpus)
    opt1_out = " --output {}stage1_{}_HDUMMYCLASS.root ".format(OUTDIR, sample)
    opt1_in = " --files-list {}{}_HDUMMYCLASS_ecm240/*.root ".format(inDIR, sample)
    wait = " ; sleep 30;"
    cmd_stage1 = cmdbase_stage1 + opt1_out + opt1_in

    cmdbase_stagentuple = "python examples/FCCee/weaver/stage2.py DIRstage1_{}_HDUMMYCLASS.root DIRntuple_MOD_{}_HDUMMYCLASS.root ".format(
        sample, sample
    )
    cmd_stage2 = cmdbase_stagentuple.replace("DIR", OUTDIR)

    mods = ["train", "test"]

    # create files storing stdout and stderr
    list_stdout = [open(OUTDIR + "{}_stdout.txt".format(flavor), "w") for flavor in flavors]
    list_stderr = [open(OUTDIR + "{}_stderr.txt".format(flavor), "w") for flavor in flavors]

    ###=== RUN STAGE 1

    for i, flavor in enumerate(flavors):

        if flavor == "qq":
            cmd_stage1_f = (
                cmdbase_stage1
                + opt1_out.replace("DUMMYCLASS", "qq")
                + " --files-list {}{}_Huu_ecm240/*.root {}{}_Hdd_ecm240/*.root".format(
                    inDIR, sample, inDIR, sample
                )
            )
        else:
            cmd_stage1_f = cmd_stage1.replace("DUMMYCLASS", flavor)

        print(cmd_stage1_f)
        # run stage1
        start1_time = time.time()
        if not args.dry:
            # subprocess.check_call(
            #    cmd_stage1_f, shell=True, stdout=list_stdout[i], stderr=list_stderr[i]
            # )
            os.system(cmd_stage1_f)

        end1_time = time.time()
        list_stdout[i].write("Stage1 time: {} \n".format(end1_time - start1_time))
    
    ###=== RUN STAGE 2

    threads = []
    for i, flavor in enumerate(flavors):

        cmd_stage2_train = cmd_stage2.replace("DUMMYCLASS", flavor).replace(
            "MOD", mods[0]
        ) + " {} {} ".format(0, N_split)
        cmd_stage2_test = cmd_stage2.replace("DUMMYCLASS", flavor).replace(
            "MOD", mods[1]
        ) + " {} {} ".format(N_split, N)
        print(cmd_stage2_train)
        print(cmd_stage2_test)

        if not args.dry:
            thread = mp.Process(
                target=ntuplizer,
                args=(
                    cmd_stage2_train,
                    cmd_stage2_test,
                    list_stdout[i],
                    list_stderr[i],
                ),
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
