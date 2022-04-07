FCCAnalyses
=============

This package produces flat ROOT trees using FCCSW EDM root files produced with the [EventProducer](https://github.com/HEP-FCC/EventProducer). As usual, if you aim at contributing to the repository, please fork it, develop and submit pull requests. To have access to the FCC samples, you need to subscribe to one of the following e-group (with owner approval) ```fcc-eos-read-xx``` with ```xx=ee,hh,eh```. For the time being, the configuration files are accessible on ```helsens``` public ```afs```. This is not optimal and will be changed in the future, thus you are also kindly asked to contact ```clement.helsens@cern.ch``` and request access to ```/afs/cern.ch/work/h/helsens/public/FCCDicts/```.

Detailed code documentation [here](http://hep-fcc.github.io/FCCAnalyses/doc/latest/index.html)

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


RootDataFrame based
=============
Using ROOT dataframe allows very quick processing time as it natively supports multithreading. In this implementation, everything from reading EDM4Hep files on eos and producing flat n-tuples, to running a final selection and plotting the results will be explained. ROOT dataframe documentation is available [here](https://root.cern/doc/master/classROOT_1_1RDataFrame.html)

Getting Started
============
In order to use the FCC analysers within ROOT dataframe, a dictionary needs to be built and put into  `LD_LIBRARY_PATH` (this happens in `setup.sh`). The following needs to be done when running local code and for developers.

```
source ./setup.sh
mkdir build install
cd build
cmake .. -DCMAKE_INSTALL_PREFIX=../install
make install
cd ..
```
Each time changes are made in C++ code, for example in ```analyzers/dataframe/``` please do not forget to re-compile.

Generalities
============
The way we suggest to use this analysis framework is to host every analysis in a single directory, for example ```examples/FCCee/higgs/mH-recoil/mumu/```. The workflow and contains the same kind of files.

1. ```analysis.py```: This class of type ```RDFanalysis``` that is used to define the list of analysers and filters to run on (```analysers``` function) as well as the output variables (```output``` function). I also contains the configuration parameters ```processList```, ```prodTag```, ```outputDir```, ```inputDir```, ```nCPUS``` and ```runBatch```. User could define multiple stages of ```analysis.py```. The first stage will most likely run on centrally produced edm4hep events, thus the usage of ```prodTag```. When running a second analysis stage, user should point to the directory where there samples are located using ```inputDir```.

2. ```finalSel.py```: This configuration file contains the final selections and it runs over the locally produced n-tuples from the various stages of ```analysis.py```. It contains a link to the ```procDict.json``` such that the samples can be properly normalised by getting centrally produced cross sections. (this might be removed later to include everything in the yaml, closer to the sample). It also contains the list of processes (matching the standard names), the number of CPU, the cut list, and the variables (that will be both written in a ```TTree``` and in the form of ```TH1``` properly normalised to an integrated luminosity of 1pb-1.
3. ```plots.py```: This configuration files is used to select the final selections from running ```finalSel.py``` to plot. Informations about how to merge processes, write some extra text, normalise to a given integrated luminosity etc... For the moment it is possible to only plot one signal at the time, but several backgrounds.

Pre-selection
============
The pre-selection runs over already existing and properly registered FCCSW EDM4Hep events. The dataset names with the corresponding statistics can be found [here](http://fcc-physics-events.web.cern.ch/fcc-physics-events/Delphesevents_spring2021_IDEA.php) for the IDEA spring 2021 campaign. The ```processList``` is a dictionary of processes, each process having it's own dictionary of parameters. For example ```'p8_ee_ZH_ecm240':{'fraction':0.2, 'chunks':2, 'output':'p8_ee_ZH_ecm240_out'}``` where ```p8_ee_ZH_ecm240``` should match an existing sample in the database, ```fraction``` is the fraction of the sample you want to run on (default is 1), ```chunks``` is the number of jobs to run (you will have the corresponding number of output files) and ```output``` in case you need to change the name of the output file (please note that then the sample will not be matched in the database for ```finalSel.py``` histograms normalisation). The other parameters are explained in [this example](https://github.com/HEP-FCC/FCCAnalyses/tree/master/example/FCCee/higgs/mH-recoil/analysis_stage1.py).
To run the pre-selection of the pre-selection stage just run:

```shell
python config/FCCAnalysisRun.py examples/FCCee/higgs/mH-recoil/mumu/analysis_stage1.py
```

This will output the files in ```ZH_mumu_recoil/stage1``` following the parameter ```outDir``` in the ```analysis_stage1.py``` file.

You also have the possibilty to by-pass the samples in ```processList``` to run over files by running something like:


```shell
python config/FCCAnalysisRun.py examples/FCCee/higgs/mH-recoil/mumu/analysis_stage1.py --output <myoutput.root> --files-list <file.root or file1.root file2.root or file*.root>
```

Pre-selection on batch (HTCondor)
============
It is also possile to run the pre-selection step on batch. For that the ```runBatch``` parameter needs to be set to true. Please make sure you select a long enough ```batchQueue``` and that your computing group is properly set ```compGroup``` (as you might not have the right to use the default one ```group_u_FCC.local_gen``` as it request to be part of the FCC computing e-group ```fcc-experiments-comp```). When running on batch, you should use the ```chunk``` parameter for each samples in your ```processList``` such that you benefit from high paralelisation.


Final selection
============
The final selection runs on the pre-selection files that we produced in the [Pre-selection](#pre-selection) step.
In the configuration file ```finalSel.py``` we define the various cuts to run on and the final variables to be stored in both a ```TTree``` and histograms. This is why the variables needs extra fields like ```title```, number of bins and range for the histogram creation.
In this example it should run like:

```
python examples/FCCee/higgs/mH-recoil/mumu/finalSel.py
```

This will create 2 files per selection ```SAMPLENAME_SELECTIONNAME.root``` for the ```TTree``` and ```SAMPLENAME_SELECTIONNAME_histo.root``` for the histograms. ```SAMPLENAME``` and ```SELECTIONNAME``` corresponds to the name of the sample and selection respectively in the configuration file.

Plotting
============
The plotting configuration file ```plots.py``` contains informations about plotting details for plots rendering but also ways of combining samples for plotting.
In this example just run like:
```
python config/doPlots.py examples/FCCee/higgs/mH-recoil/mumu/plots.py
```

This will produce the plots in the ```outdir``` defined in the configuration file.
