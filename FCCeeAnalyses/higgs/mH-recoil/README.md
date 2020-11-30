## The Higgs boson mass from the recoil mass

### Contributors
- Clement Helsens: Developer, Sample production, Preliminary FCCAnalyses design, Preliminary recoil fit analysis

### Preliminary analyses
Using the corresponding ```FCCAnalyses``` [ZH_Zmumu](https://github.com/HEP-FCC/FCCAnalyses/tree/master/FCCeeAnalyses/Higgs/mH-recoil/mumu) and [ZH_Zee](https://github.com/HEP-FCC/FCCAnalyses/tree/master/FCCeeAnalyses/Higgs/mH-recoil/ee) and using the input files in ```edm4hep``` of this [sample production](http://fcc-physics-events.web.cern.ch/fcc-physics-events/Delphesevents_fccee_tmp.php), produced ```FlatNtuples``` and ```histograms``` used to fit the recoil: ```/eos/experiment/fcc/ee/analyses/case-studies/higgs/mH-recoil/FlatNtuples/```.

![](images/leptonic_recoil_m_ZH_sel1_stack_lin.png?raw=true)


arguments and examples to run the fitting macro could be seen by running
```python
python utils/massFit.py
usage:   python massFit.py BASEDIR HISTONAME SELECTION BINLOW=120 BINHIGH=140
example: python massFit.py /eos/experiment/fcc/ee/analyses/case-studies/higgs/mH-recoil/FlatNtuples/ZH_Zee/ leptonic_recoil_m_zoom3 sel1
example: python massFit.py /eos/experiment/fcc/ee/analyses/case-studies/higgs/mH-recoil/FlatNtuples/ZH_Zmumu/ leptonic_recoil_m_zoom4 sel0 122 128
```


As an example the fit result of running the following command 
```python
python case-studies/higgs/mH-recoil/massFit.py /eos/experiment/fcc/ee/analyses/case-studies/higgs/mH-recoil/FlatNtuples/ZH_Zee/ leptonic_recoil_m_zoom4 sel1 123 127:
```

is shown below (to be re-done with including beam energy spread)

```bash
  EXT PARAMETER                                INTERNAL      INTERNAL  
  NO.   NAME      VALUE            ERROR       STEP SIZE       VALUE   
   1  alpha       -8.67272e-01   4.57686e-02   3.90224e-02   7.11703e-01
   2  cbmean       1.25094e+02   6.79656e-03   3.51532e-03   1.87562e-02
   3  cbsigma      2.81768e-01   6.89490e-03   5.74469e-02  -6.08122e-02
   4  lam         -3.43241e-06   1.01039e-02   3.40174e-01   1.56709e+00
   5  n            1.27209e+00   1.72834e-01   2.30740e-02  -1.34474e+00
   6  nbkg         7.59189e+03   2.15350e+02   1.34305e-03  -1.51568e+00
   7  nsig         9.05996e+03   2.19379e+02   1.28389e-03  -1.51059e+00
```

![](images/fitResult.png?raw=true)



