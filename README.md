# FCCAnalyses

Common framework for FCC related analyses. This framework allows one to write
full analysis, taking [EDM4hep](https://github.com/key4hep/EDM4hep) input ROOT
files and producing the plots.


## Quick Start

Running analysis script can be done using `fccanalysis` command which is
shipped in Key4hep stack:

```sh
source /cvmfs/sw.hsf.org/key4hep/setup.sh
fccanalysis run analysis_script.py
```


## Pre-generated Samples

### Access

To have read access to the FCC pre-generated samples, one needs to be subscribed to
the following e-group (with owner approval): `fcc-eos-access`.


### Winter 2023 and Spring 2021 Pre-generated Samples

In order to run over pre-generated samples from `winter2023` or `spring2021`
campaigns one needs to compile `pre-edm4hep1` branch of the FCCAnalyses in the
`2024-03-10` release:

   ```sh
   source /cvmfs/sw.hsf.org/key4hep/setup.sh -r 2024-03-10
   git clone --branch pre-edm4hep1 git@github.com:HEP-FCC/FCCAnalyses.git
   cd FCCAnalyses
   source ./setup.sh
   fccanalysis build -j 8
   ```


### Sample Metadata

All sample information, including Key4hep stack used for the campaign, is
collected at the
[FCC Physics Events](https://fcc-physics-events.web.cern.ch/)
website.


## Documentation

Detailed documentation can be found at the
[FCCAnalyses](https://hep-fcc.github.io/FCCAnalyses/) webpage.


## Contributing

As usual, if you aim at contributing to the repository, please fork it, develop
your feature/analysis and submit a pull requests.


### Code Formating

The preferred style of the C++ code in the
[FCCAnalyses](https://hep-fcc.github.io/FCCAnalyses/) is LLVM, which is checked
by a CI job.

To apply formatting to a file:
```
clang-format -i -style=file /path/to/file.cpp
```
