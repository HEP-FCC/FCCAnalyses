# FCCAnalyses

Common framework for FCC related analyses. This framework allows one to write
full analysis, taking [EDM4hep](https://github.com/key4hep/EDM4hep) input ROOT
files and producing the plots.

>
> As usual, if you aim at contributing to the repository, please fork it,
> develop your feature/analysis and submit a pull requests.
>
> To have access to the FCC samples, you need to be subscribed to one of the
> following e-groups (with owner approval) `fcc-eos-read-xx` with `xx=ee,hh,eh`.
> For the time being, the configuration files are accessible on `helsens` public
> AFS. This is not optimal and will be changed in the future, thus you are
> also kindly asked to contact `clement.helsens@cern.ch` and request access to
> `/afs/cern.ch/work/h/helsens/public/FCCDicts/`.
>

Detailed code documentation can be found
[here](http://hep-fcc.github.io/FCCAnalyses/doc/latest/index.html).


## Table of contents

* [FCCAnalyses](#fccanalyses)
  * [Table of contents](#table-of-contents)
  * [RootDataFrame based](#rootdataframe-based)
  * [Getting started](#getting-started)
  * [Generalities](#generalities)
  * [Example analysis](#example-analysis)
    * [Pre-selection](#pre-selection)
    * [Final selection](#final-selection)
    * [Plotting](#plotting)


## RootDataFrame based

Using ROOT dataframe allows to use modern, high-level interface and very quick
processing time as it natively supports multithreading. In this README,
everything from reading EDM4hep files on EOS and producing flat n-tuples, to
running a final selection and plotting the results will be explained.

ROOT dataframe documentation is available
[here](https://root.cern/doc/master/classROOT_1_1RDataFrame.html).


## Getting started

In order to use the FCC analysers within ROOT dataframe, a dictionary needs to
be built and put into `LD_LIBRARY_PATH` (this happens in `setup.sh`). The
following needs to be done when running local code and for developers. 

```shell
source ./setup.sh
mkdir build install
cd build
cmake .. -DCMAKE_INSTALL_PREFIX=../install
make install
cd ..
```

>
> Each time changes are made in the C++ code, for example in
> `analyzers/dataframe/` please do not forget to re-compile :)

## Logging in

Personal note : In order to work from personal windows computer :
- Launch Xming
- Launch Putty
- Select CERN session and log into lxplus.

Need to run these commands everytime you log in :
```shell
bash
cd FCCAnalyses
source ./setup.sh
```
## Madgraph installation

Following the recomendations from https://twiki.cern.ch/twiki/bin/view/Main/MadgraphOnLxPlus, Madgraph was installed in the FCCAnalyses directory (only advice was to install it into the workspace). Moreover, we are moving away from Tanishq instructions, since the FCCeePhysicsPerformance git is no longer necessary according to Juliette, hence only FCCAnalyses has been installed properly. Therefore, will need to be careful about copying paths etc.. since Madgraph is installed in FCCAnalyses/

### Launching Madgraph
In order to launch Madgraph : 
- Within workspace directory :
```shell
source ~/.bash_madgraph
cd Madgraph/MG5_aMC_v2_6_4/
./bin/mg5_aMC

```

### Importing models to Madgraph
Useful madgraph models for HNL are available at https://feynrules.irmp.ucl.ac.be/wiki/HeavyN.
In order to import them, go to :  Madgraph/MG5_aMC_v2_6_7/models and run (e.g for SM_HeavyN_CKM_AllMasses_LO) :
```
wget http://feynrules.irmp.ucl.ac.be/raw-attachment/wiki/HeavyN/SM_HeavyN_CKM_AllMasses_LO.tgz
tar -zxvf SM_HeavyN_CKM_AllMasses_LO.tgz
```


## Using a proc card to generate an EDM file
Proc cards are like configuration files for generating Madgraph events. Baseline proc cards are located at :
https://github.com/HEP-FCC/FCCeePhysicsPerformance/tree/master/case-studies/BSM/LLP/DisplacedHNL/HNL_sample_creation
Proc cards can be modified using vim/vi:
```shell
i to insert
:wq to save changes)
```
Note : The provided proc_card seem to contain a command that is either unknown, or has to be added by hand (since it kills the job). Therefore, in order to be able to continue, we have removed the line ```set auto_convert_model T``` (l33).

In order to generate an event with a given proc card do:
```shell
cd Madgraph/MG5_aMC_v2_6_4/
./bin/mg5_aMC path_to_card/proc_cart.dat
```
This then generates .lhe.gz file located at ```HNL_ljj/Events/run_01/unweighted_events.lhe.gz``` which needs to be unzipped :
```shell
gunzip file_name.lhe.gz
```
## From .lhe to .root : final steps to EDM sample.
Once the .lhe file has been unzipped, copy it to the directory containing the Pythia card. We will then need to use Delphes in order to create a .root file to analyze.
```shell
cp file_name.lhe path_to_workspace/FCCeePhysicsPerformance/case-studies/BSM/LLP/DisplacedHNL/HNL_sample_creation/
cd FCCeePhysicsPerformance/case-studies/BSM/LLP/DisplacedHNL/HNL_sample_creation/
```
Must then edit ``` HNL_eenu_pythia.cmnd``` by including the .lhe file (line 14). 
Note: It is possible that the n° of event of the pythia card must match the number of events set in the proc_card.dat file for the events to be generated.
Then run :
```shell
source /cvmfs/fcc.cern.ch/sw/latest/setup.sh
DelphesPythia8_EDM4HEP ../../../../../../FCC-config/FCCee/Delphes/card_IDEA.tcl ../../../../../../FCC-config/FCCee/Delphes/edm4hep_IDEA.tcl HNL_eenu_pythia.cmnd HNL_ejj.root
```
Where HNL_ejj.root is the output file

## Analysis
### Stage 1
In order to run the analysis, we use the new version of the analysis code, located at ```/FCCAnalyses/examples/FCCee/bsm/LLPs/DisplacedHNL```. In order to run the stage 1 analysis code over our EDM sample, we must specify it using :
```shell
cd FCCAnalyses/examples/FCCee/bsm/LLPs/DisplacedHNL
fccanalysis run analysis_stage1.py --output <name_of_desired_output.root> --files-list <name_of_delphes/pythia_root_file.root>
```
Note : you can (must) specify the output directory by directly modifying ```analysis_stage1.py``` (l18)
### Final analysis
The next step is to use ```final_analysis.py```. It must be modified in order to contain the correct inputDir and outputDir. Last test was to remove all processes from process_list and leave only the .root file created during stage1, so it looked like : 
```shell
processList = {
    #run over the full statistics from stage1
    'HNL_ejj_output_test':{},
}
```
Once this is done, run :
```shell
fccanalysis final analysis_final.py
```
The resulting .root files are stored in the output directory which was specified within ```analysis_final.py```

### Plots analysis
The final step is to use the plotting script. Make sure to modify the inputDir to match with the outputDir defined in the previous step. The selections/plots/legend/colors 'keys' have to match the ones contained in the inputDir. Once this is done, run :
```shell
fccanalysis plots analysis_plots.py
```
This will generate plots for each selection. These can then be copied to your local device (from a local terminal) using :
```shell
scp -r dimoulin@lxplus.cern.ch:/afs/cern.ch/user/d/dimoulin/FCCAnalyses/examples/FCCee/bsm/LLPs/DisplacedHNL/plots/ .
```
## Generalities

Analyses in the FCCAnalyses framework usually follow standardized workflow,
which consists of multiple files inside a single directory. Individual files
denote steps in the analysis and have the following meaning:

1. `analysis.py` or `analysis_stage<num>`: In this file(s) the class of type
    `RDFanalysis` is used to define the list of analysers and filters to run on
    (`analysers` function) as well as the output variables (`output` function).
    It also contains the configuration parameters `processList`, `prodTag`,
    `outputDir`, `inputDir`, `nCPUS` and `runBatch`. User can define multiple
    stages of `analysis.py`. The first stage will most likely run on centrally
    produced EDM4hep events, thus the usage of `prodTag`. When running a second
    analysis stage, user points to the directory where the samples are
    located using `inputDir`.

2. `analysis_final.py`: This analysis file contains the final selections and it
    runs over the locally produced n-tuples from the various stages of
    `analysis.py`. It contains a link to the `procDict.json` such that the
    samples can be properly normalised by getting centrally produced cross
    sections. (this might be removed later to include everything in the yaml,
    closer to the sample). It also contains the list of processes (matching the
    standard names), the number of CPUs, the cut list, and the variables (that
    will be both written in a `TTree` and in the form of `TH1` properly
    normalised to an integrated luminosity of 1pb<sup>-1</sup>.

3. `analysis_plots.py`: This analysis file is used to select the final
    selections from running `analysis_final.py` to plot. It usually contains
    information about how to merge processes, write some extra text, normalise
    to a given integrated luminosity etc... For the moment it is possible to
    only plot one signal at the time, but several backgrounds.


## Example analysis

To better explain the FCCAnalyses workflow let's run our example analysis. The
analysis should be located at `examples/FCCee/higgs/mH-recoil/mumu/`.


### Pre-selection

The pre-selection runs over already existing and properly registered FCCSW
EDM4hep events. The dataset names with the corresponding statistics can be found
[here](http://fcc-physics-events.web.cern.ch/fcc-physics-events/Delphesevents_spring2021_IDEA.php)
for the IDEA spring 2021 campaign. The `processList` is a dictionary of
processes, each process having it's own dictionary of parameters. For example
```python
'p8_ee_ZH_ecm240':{'fraction':0.2, 'chunks':2, 'output':'p8_ee_ZH_ecm240_out'}
```
where `p8_ee_ZH_ecm240` should match an existing sample in the database,
`fraction` is the fraction of the sample you want to run on (default is 1),
`chunks` is the number of jobs to run (you will have the corresponding number
of output files) and `output` in case you need to change the name of the output
file (please note that then the sample will not be matched in the database for
`finalSel.py` histograms normalisation). The other parameters are explained in
[the example file](https://github.com/HEP-FCC/FCCAnalyses/tree/master/example/FCCee/higgs/mH-recoil/analysis_stage1.py).

To run the pre-selection stage of the example analysis run:

```shell
fccanalysis run examples/FCCee/higgs/mH-recoil/mumu/analysis_stage1.py
```

This will create the output files in the `ZH_mumu_recoil/stage1` subdirectory
of the output director specified with parameter `outDir` in the file.

You also have the possibility to bypass the samples specified in the
`processList` variable by using command line parameter `--output`, like so:

```shell
fccanalysis run examples/FCCee/higgs/mH-recoil/mumu/analysis_stage1.py \
       --output <myoutput.root> \
       --files-list <file.root or file1.root file2.root or file*.root>
```

The example analysis consists of two pre-selection stages, to run the second one
slightly alter the previous command:

```shell
fccanalysis run examples/FCCee/higgs/mH-recoil/mumu/analysis_stage2.py
```


#### Pre-selection on batch (HTCondor)

It is also possible to run the pre-selection step on the batch. For that the
`runBatch` parameter needs to be set to true. Please make sure you select a
long enough `batchQueue` and that your computing group is properly set
`compGroup` (as you might not have the right to use the default one
`group_u_FCC.local_gen` as it request to be part of the FCC computing e-group
`fcc-experiments-comp`). When running on batch, you should use the `chunk`
parameter for each sample in your `processList` such that you benefit from high
parallelisation.


### Final selection

The final selection runs on the pre-selection files that were produced in the
[Pre-selection](#pre-selection) step. In the configuration file
`analysis_final.py` various cuts are defined to be run on and the final
variables to be stored in both a `TTree` and histograms. This is why the
variables needs extra fields like `title`, number of bins and range for the
histogram creation. In the example analysis it can be run like this:

```shell
fccanalysis final examples/FCCee/higgs/mH-recoil/mumu/analysis_final.py
```

This will create 2 files per selection `SAMPLENAME_SELECTIONNAME.root` for the
`TTree` and `SAMPLENAME_SELECTIONNAME_histo.root` for the histograms.
`SAMPLENAME` and `SELECTIONNAME` correspond to the name of the sample and
selection respectively in the configuration file.


### Plotting

The plotting analysis file `analysis_plots.py` contains not only details for
the rendering of the plots but also ways of combining samples for plotting.
In the example analysis it can be run in the following manner:

```shell
fccanalysis plots examples/FCCee/higgs/mH-recoil/mumu/analysis_plots.py
```

Resulting plots will be located the `outdir` defined in the analysis file.
