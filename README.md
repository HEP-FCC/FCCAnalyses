FCCAnalyses
=============

This package produce flat ROOT trees using FCCSW EDM root files produced with the [EventProducer](https://github.com/HEP-FCC/EventProducer). As usual, if you aim at contributing to the repository, please fork it, develop and submit pull requests. To have access to the FCC samples, you need to subscribe to one of the following e-group (with owner approval) ```fcc-eos-read-xx``` with ```xx=ee,hh,eh```. For the time being, the configuration files are accessible on ```helsens``` public ```afs```. This is not optimal and will be changed in the future, thus you are also kindly asked to contact ```clement.helsens@cern.ch``` and request access to ```/afs/cern.ch/work/h/helsens/public/FCCDicts/```.


Table of contents
=================
  * [FCCAnalyses](#fccanalyses)
  * [Table of contents](#table-of-contents)
  * [RootDataFrame based](#rootdataframe-based)
    * [Getting Started](#getting-started)
    * [Generalities](#generalities)
    * [Pre selection](#pre-selection)
    * [Final selection](#final-selection)
    * [Plotting](#plotting)
  * [Heppy based (no long term support)](#heppy-based-no-long-term-support)
    * [Requirements](#requirements)
    * [Getting Started](#getting-started)


RootDataFrame based
=============
Using ROOT dataframe allows a much quicker processing time. In this implementation, everything from reading FCCSW EDM files on eos and producing flat n-tuples, to running a final selection and plotting the results will be explained.

Getting Started
============
In order to use ROOT dataframe for the analyses, the dictionary with the analyzers needs to be built and put into  `LD_LIBRARY_PATH` (this happens in `setup.sh`)

First check if FCCSW is setup. If the command ```which fccrun``` returns something like: ```/cvmfs/sw.hsf.org/spackages/linux-centos7-broadwell/gcc-8.3.0/fccsw-develop-q57ahua7lm65fvxnzekozih4mgvzptlx/scripts/fccrun``` then you are good to go, if not please run:

```
source /cvmfs/fcc.cern.ch/sw/latest/setup.sh
```

```
source setup.sh
mkdir build install
cd build
cmake .. -DCMAKE_INSTALL_PREFIX=../install
make install
```
Each time changes are made in ```analyzers/dataframe/``` please re-compile!

Generalities
============
Each analysis is hosted in a single directory, for example ```FCCeeAnalyses/ZH_Zmumu/dataframe/``` and contains the same kind of files, please use the same naming convention for all analysis. 

1. ```analysis.py```: This class that is used to define the list of analysers and filters to run on as well as the output variables. 
2. ```preSel.py```: This configuration file is used to define how to run the ```analysis.py```. It contains the list of samples, the number of CPUs, the fraction of the original sample to process and the base directory for the yaml files (that contains the informations about the samples). This will run the ```analysis.py``` with a common code ```bin/runDataFrame.py``` (this last file is common to all analyses and should not be touched). 
3. ```finalSel.py```: This configuration file contains the final selections and it runs over the locally produced flat ntuples from the ```preSel.py```. It contains a link to the ```procDict.json``` for getting cross section etc...(this might be removed later to include everything in the yaml, closer to the sample), the list of processes, the number of CPU, the cut list, and the variables (that will be both written in a ```TTree``` and in the form of ```TH1``` properly normalised to an integrated luminosity of 1pb-1. 
4. ```plots.py```: This configuration files is used to select the final selections from running ```finalSel.py``` to plot. Informations about how to merge processes, write some extra text, normalise to a given integrated luminosity etc... For the moment it is possible to only plot one signal at the time, but several backgrounds. 

Pre-selection
============
The pre-selection runs over already existing and properly registered FCCSW EDM events. The dataset names with the corresponding statistics can be found [here](http://fcc-physics-events.web.cern.ch/fcc-physics-events/Delphesevents_fccee_v01.php). One important parameter is the fraction of the total dataset to run. It can be found in the ```preSel.py``` file by setting a value between ]0,1]. For example ```fraction=0.1``` will run over 10% of the statistics. Reading the files on ```eos```, and with 15 CPUs we observe processing speeds between 3000 and 10000 events per seconds depending on the number of files. Only run full statistics after having done all the proper testing and analysis design as it can take some time (that of course depends on the sample total statistics). To run the pre-selection of the ```ZH_Zmumu``` analysis, just run:
```
python FCCeeAnalyses/ZH_Zmumu/dataframe/preSel.py
```
This will output 3 files in ```FCCee/ZH_Zmumu/``` following the parameter ```outdir``` in the ```preSel.py``` configuration file.


Final selection
============
The final selection runs on the pre-selection files that we produced in the [Pre-selection](#pre-selection) step. 
In the configuration file ```finalSel.py``` we define the various cuts to run on and the final variables to be stored in both a ```TTree``` and histograms. This is why the variables needs extra fields like ```title```, number of bins and range for the histogram creation.
In this example it should run like: 

```
python FCCeeAnalyses/ZH_Zmumu/dataframe/finalSel.py
```

This will create 2 files per selection ```SAMPLENAME_SELECTIONNAME.root``` for the ```TTree``` and ```SAMPLENAME_SELECTIONNAME_histo.root``` for the histograms. ```SAMPLENAME``` and ```SELECTIONNAME``` corresponds to the name of the sample and selection respectively in the configuration file.

Plotting
============
The plotting configuration file ```plots.py``` contains informations about plotting details for plots rendering but also ways of combining samples for plotting. 
In this example just run like: 
```
python bin/doPlots.py FCCeeAnalyses/ZH_Zmumu/dataframe/plots.py
```

This will produce the plots in the ```outdir``` defined in the configuration file.



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
