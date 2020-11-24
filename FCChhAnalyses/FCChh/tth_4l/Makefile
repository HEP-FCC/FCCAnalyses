

# build the reproducer of the heppy analysis with TDataFrame
# todo: cleaner directory structure, cmake, etc

all: tdataframe_analysis

tdataframe_analysis:  fcc_ana_tth_4l.cxx
	g++ -g -o fcc_ana_tth_4l fcc_ana_tth_4l.cxx `root-config --cflags --glibs` -lROOTVecOps -lROOTDataFrame   

tdataframe_analysis_mt:  fcc_ana_tth_4l.cxx
	g++ -g -o fcc_ana_tth_4l fcc_ana_tth_4l.cxx `root-config --cflags --glibs` -lROOTVecOps -lROOTDataFrame   -DENABLEIMPLICITMT

# run the analysis

run:
	./fcc_ana_tth_4l tree.root root://eospublic.cern.ch//eos/experiment/fcc/hh/generation/DelphesEvents/fcc_v02/mgp8_pp_tth01j_5f_hllll/events_000000830.root

# todo: comparison with expected output  (/afs/cern.ch/work/v/vavolkl/public/heppy_analysis_samples/localtest/mgp8_pp_tth01j_5f_hllll_1/heppy.FCChhAnalyses.FCChh.tth_4l.TreeProducer.TreeProducer_1/tree.root)
