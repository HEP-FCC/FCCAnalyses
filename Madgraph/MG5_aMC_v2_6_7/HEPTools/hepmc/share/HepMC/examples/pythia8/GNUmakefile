################################################################################
# Makefile for building a HepMC PYTHIA8 example
#
# Lynn Garren garren@fnal.gov
#
# main31 and main32 have been copied from PYTHIA 8.157
# you must source either config.csh or config.sh first
#
# ./main31.exe
# ./main32.exe main32.cmnd hepmcout32.dat
#
################################################################################ Define directory paths 
#    You may have to change PYTHIA8_HOME and/or other variables
#
  HepMCdir      = /afs/cern.ch/user/d/dimoulin/FCCAnalyses/Madgraph/MG5_aMC_v2_6_7/HEPTools/hepmc
  HEPMCLOCATION = $(HepMCdir)
  HepMClib      = -L$(HEPMCLOCATION)/lib -Wl,-rpath -Wl,$(HEPMCLOCATION)/lib \
                  -lHepMC
  Pythia_LIB	= -L$(PYTHIA8_HOME)/lib -Wl,-rpath -Wl,$(PYTHIA8_HOME)/lib \
                  -lpythia8 -llhapdfdummy -lhepmcinterface

################################################################################ Compiler options
#
  CXX           = /cvmfs/sft.cern.ch/lcg/releases/gcc/7.3.0-90605/x86_64-slc6-gcc62-opt/bin/g++
  INCLUDES 	= -I$(HEPMCLOCATION)/include -I$(PYTHIA8_HOME)/include
  CXXFLAGS      =  -ansi -pedantic -Wall -g -O2 -Wshadow -fbounds-check $(INCLUDES)
ifeq "$(CXX)" "g++"
   FLAGS 	= $(DFLG) -fno-second-underscore $(INCDIR)
else
  FLAGS 	= $(DFLG) $(INCDIR)
endif

  LINK_LIBS     =  

UNAME = $(shell uname)
ifneq "$(UNAME)" "Darwin"
  LINK_LIBS     += -Wl,-rpath -Wl,$(HepMCdir)/lib
endif

  HDRS          = $(HepMCdir)/include/HepMC/*.h *.h
  EXAMPLES	=  main31.exe main32.exe

###############################################################################
#
.SUFFIXES:      .o .cc .exe

all:	$(EXAMPLES)

main31.exe: main31.o
	$(CXX) $(CXXFLAGS) -o $@ main31.o \
	$(Pythia_LIB) \
	$(HepMClib)

main32.exe: main32.o
	$(CXX) $(CXXFLAGS) -o $@ main32.o \
	$(Pythia_LIB) \
	$(HepMClib)

###############################################################################
#
.cc.o:         $(HDRS) $<
	$(CXX) $(CXXFLAGS) -c $< -o $@

###############################################################################
# gmake clean       removes all garbage from HepMC directories.
# gmake distclean       removes all compiled libraries, executables, +garbage
#
clean:
	rm -f *.o

distclean: 
	$(MAKE) clean --no-print-directory
	rm -f $(EXAMPLES)
	rm -f *.dat
