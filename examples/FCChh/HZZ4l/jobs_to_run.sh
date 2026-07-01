#Commands to run to make the inputs for the global fit with excl pT bins

fccanalysis final examples/FCChh/HZZ4l/analysis_final_pTbinned.py 100TeV
python examples/FCChh/HZZ4l/get_eff_unc.py --energy 100TeV --doExclBins

fccanalysis final examples/FCChh/HZZ4l/analysis_final_pTbinned.py 84TeV
python examples/FCChh/HZZ4l/get_eff_unc.py --energy 84TeV --doExclBins

fccanalysis final examples/FCChh/HZZ4l/analysis_final_pTbinned.py 72TeV
python examples/FCChh/HZZ4l/get_eff_unc.py --energy 72TeV --doExclBins

fccanalysis final examples/FCChh/HZZ4l/analysis_final_pTbinned.py 120TeV
python examples/FCChh/HZZ4l/get_eff_unc.py --energy 120TeV --doExclBins