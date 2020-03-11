FCCAnalyses
=============

This package produce flat ROOT trees using FCCSW EDM root files produced with the [EventProducer](https://github.com/HEP-FCC/EventProducer)


Table of contents
=================
  * [FCCAnalyses](#fcchhanalyses)
  * [Table of contents](#table-of-contents)
  * [RootDataFrame based](#rootdataframe-based)
    * [Requirements](#requirements)
    * [Getting Started](#getting-started)
  * [Heppy based](#heppy-based)
    * [Requirements](#requirements)
    * [Getting Started](#getting-started)


RDF analyzers [WIP]
=============

In order to use ROOT dataframe for the analyses, the dictionary with the analyzers needs to be built and put into  `LD_LIBRARY_PATH` (happens in `setup.sh`)

```
source setup.sh
mkdir build install
cd build
cmake .. -DCMAKE_INSTALL_PREFIX=../install
make install
```

To test:

```
# python
python FCChhAnalyses/FCChh/tth_4l/dataframe/fcchh_ana_tth_4l.py root://eospublic.cern.ch//eos/experiment/fcc/hh/generation/DelphesEvents/fcc_v02/mgp8_pp_tth01j_5f_hllll/events_000000492.root
# C++
./build/FCChhAnalyses/FCChh/tth_4l/dataframe/fcchh_ana_tth_4l tree.root root://eospublic.cern.ch//eos/experiment/fcc/hh/generation/DelphesEvents/fcc_v02/mgp8_pp_tth01j_5f_hllll/events_000000492.root
```

both commands should produce the same output file `tree.root`


Requirements
============

`FCChhAnalyses` depends on the following packages:

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
```

in order to save time I already produced the outputs, they are stored on eos

```
/eos/experiment/fcc/helhc/analyses/Zprime_tt/heppy_outputs/helhc_v01/
```
