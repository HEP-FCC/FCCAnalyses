# FCCAnalyses

[![DOI](https://zenodo.org/badge/177151745.svg)](https://zenodo.org/doi/10.5281/zenodo.4767810)

![test](https://github.com/HEP-FCC/FCCAnalyses/actions/workflows/test.yml/badge.svg)
![docs](https://github.com/HEP-FCC/FCCAnalyses/actions/workflows/docs.yml/badge.svg)

Common framework for FCC related analyses. This framework allows one to write
full analysis, taking [EDM4hep](https://github.com/key4hep/EDM4hep) input ROOT
files and producing the plots.


## Quick start

In order to run over pre-generated samples from `winter2023` or `spring2021`
campaigns one needs to compile `pre-edm4hep1` branch of the FCCAnalyses in the
`2024-03-10` release (hard coded into the `setup.sh` script)

```sh
git clone --branch pre-edm4hep1 git@github.com:HEP-FCC/FCCAnalyses.git
cd FCCAnalyses
source ./setup.sh
fccanalysis build -j 8
```

To have access to the FCC pre-generated samples, one needs to be subscribed
the `fcc-eos-access` e-group (with owner approval).

Detailed documentation can be found at the [FCCAnalyses](https://hep-fcc.github.io/FCCAnalyses/) webpage.

All sample information, including Key4hep stack used for the campaign, is collected at the [FCC Physics Events](http://fcc-physics-events.web.cern.ch/fcc-physics-events/) website.


## Contributing

As usual, if you aim at contributing to the repository, please fork it, develop your feature/analysis and submit a pull requests.

### Code formating

The preferred style of the C++ code in the FCCAnalyses is LLVM which is checked
by CI job.

To apply formatting to a given file:
```
clang-format -i -style=file /path/to/file.cpp
```
