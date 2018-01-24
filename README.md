FCChhAnalyses
=============

This package is used inside [heppy](https://github.com/HEP-FCC/heppy) to produce flat ROOT trees using FCCSW EDM root files produced with the [EventProducer](https://github.com/FCC-hh-framework/EventProducer)


Table of contents
=================
  * [FCChhAnalyses](#fcchhanalyses)
  * [Table of contents](#table-of-contents)
  * [Clone and initialisation](#clone-and-initilisation)
 

Clone and initialisation
========================

If you do not attempt to contribute to the heppy repository, simply clone it:
```
git clone git@github.com:HEP-FCC/heppy.git
```

If you aim at contributing to the heppy repository, you need to fork and then clone the forked repository:
```
git clone git@github.com:YOURGITUSERNAME/heppy.git
```

Then go to the ```heppy``` directory ```cd heppy```.

Source the FCCSW software stack
```
source /cvmfs/fcc.cern.ch/sw/0.8.3/init_fcc_stack.sh
```

and source the heppy

```
source ./init.sh
```

If you do not attempt to contribute to the FCChhAnalyses repository, simply clone it:
```
git clone git@github.com:FCC-hh-framework/FCChhAnalyses.git
```

If you aim at contributing to the heppy repository, you need to fork and then clone the forked repository:
```
git clone git@github.com:YOURGITUSERNAME/FCChhAnalyses.git
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
