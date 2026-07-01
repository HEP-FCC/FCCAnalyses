#Commands to run to make the inputs for the global fit with excl pT bins

fccanalysis final examples/FCChh/Hmumu/analysis_final_pTbinned.py 100TeV
python examples/FCChh/Hmumu/get_eff_unc.py --energy 100TeV --doExclBins

fccanalysis final examples/FCChh/Hmumu/analysis_final_pTbinned.py 84TeV
python examples/FCChh/Hmumu/get_eff_unc.py --energy 84TeV --doExclBins

fccanalysis final examples/FCChh/Hmumu/analysis_final_pTbinned.py 72TeV
python examples/FCChh/Hmumu/get_eff_unc.py --energy 72TeV --doExclBins

fccanalysis final examples/FCChh/Hmumu/analysis_final_pTbinned.py 120TeV
python examples/FCChh/Hmumu/get_eff_unc.py --energy 120TeV --doExclBins