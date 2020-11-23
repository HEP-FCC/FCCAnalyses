FCCAnalyses
=============

This package produce flat ROOT trees using FCCSW EDM root files produced with the [EventProducer](https://github.com/HEP-FCC/EventProducer). As usual, if you aim at contributing to the repository, please fork it, develop and submit pull requests. To have access to the FCC samples, you need to subscribe to one of the following e-group (with owner approval) ```fcc-eos-read-xx``` with ```xx=ee,hh,eh```. For the time being, the configuration files are accessible on ```helsens``` public ```afs```. This is not optimal and will be changed in the future, thus you are also kindly asked to contact ```clement.helsens@cern.ch``` and request access to ```/afs/cern.ch/work/h/helsens/public/FCCDicts/```.


Table of contents
=================
  * [FCCAnalyses](#fccanalyses)
  * [Table of contents](#table-of-contents)
  * [Heppy based (no long term support)](#heppy-based-no-long-term-support)
    * [Requirements](#requirements)
    * [Getting Started](#getting-started)

Heppy based (no long term support)
============

Requirements
============

`FCCAnalyses` depends on the following packages:

- [`heppy`](https://github.com/cbernet/heppy)
- [`ROOT`](https://github.com/root-project/root)


Getting Started
===============

Above-mentioned packages are provided through CVMFS in the stack of FCC external software dependencies, which can be sourced as follows:

```
source /cvmfs/fcc.cern.ch/sw/views/releases/externals/latest/setup.sh
```

Otherwise, both packages can be easily installed using `conda` and `pip`:

```
# Install ROOT
conda install -c conda-forge root

# Install heppy
pip install heppyfwk
```

See the official documentation for further information about [conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html) and [pip](https://pip.pypa.io/en/stable/installing/)

Once `root` and `heppy` are present on our system, either through CVMFS or a manual installation, `FCChhAnalyses` can be installed with the following command:

```
python setup.py install --user
```

Now you are ready to run an existing analysis or make your own one.

```
heppy_loop.py Outputs/HELHC FCChhAnalyses/HELHC/Zprime_tt/analysis.py
```

but better to run on Batch
```
heppy_batch.py -o FCChhAnalyses/HELHC/Outputs FCChhAnalyses/HELHC/Zprime_tt/analysis.py -b 'bsub -q 8nh < batchScript.sh'
heppy_batch.py -o FCChhAnalyses/HELHC/Outputs FCChhAnalyses/HELHC/Zprime_tt/analysis.py -b 'run_condor.sh --bulk tttt_condor -f workday'
-> the --bulk option is necessary to submit all the CHunks into 1 CONDOR job
-> if do not use --bulk, there will have 1 job per Chunk
```

The job retry, is as follow :
heppy_check.py Outdir/*Chunk* -b 'run_condor.sh -f workday'
-> it will submit each failed Chunks into a single CONDOR job
```

The queue names of CONDOR :
 20 mins -> espresso
 1h -> microcentury
 2h -> longlunch
 8h -> workday
 1d -> tomorrow
 3d -> testmatch
 1w -> nextweek

```

in order to save time I already produced the outputs, they are stored on eos

```
/eos/experiment/fcc/helhc/analyses/Zprime_tt/heppy_outputs/helhc_v01/
```
