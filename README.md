# FCCAnalyses

Common framework for FCC related analyses. This framework allows one to write
full analysis, taking [EDM4hep](https://github.com/key4hep/EDM4hep) input ROOT
files and producing the plots.


## Quick start

Running analysis script can be done using `fccanalysis` command which is shipped in Key4hep stack:

```shell
source /cvmfs/sw.hsf.org/key4hep/setup.sh
fccanalysis run analysis_script.py
```

To have access to the FCC pre-generated samples, one needs to be subscribed to one of the following e-groups (with owner approval)
`fcc-eos-read-xx` with `xx = ee,hh,eh`.

Detailed documentation can be found at the [FCCAnalyses](https://hep-fcc.github.io/FCCAnalyses/) webpage.

## Pre-generated Samples

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
