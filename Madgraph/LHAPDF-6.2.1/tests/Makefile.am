check_PROGRAMS = testalphas testgrid testindex testinfo testpaths testperf testsetperf testnsetperf

AM_CPPFLAGS += -I$(top_srcdir)/include $(BOOST_CPPFLAGS)
AM_LDFLAGS += -L$(top_builddir)/src
LIBS = -lLHAPDF

testalphas_SOURCES = testalphas.cc
testgrid_SOURCES = testgrid.cc
testindex_SOURCES = testindex.cc
testinfo_SOURCES = testinfo.cc
testpaths_SOURCES = testpaths.cc
testperf_SOURCES = testperf.cc
testsetperf_SOURCES = testsetperf.cc
testnsetperf_SOURCES = testnsetperf.cc

TESTS = testpaths

#testalphas testgrid testindex
installcheck-local: check
	$(bindir)/lhapdf install CT10nlo
	$(bindir)/lhapdf list
	./testalphas
	./testgrid
	./testindex

uninstall-local:
	rm -rf $(pkgdatadir)/CT10nlo

CLEANFILES = alphas_ct10nlo.dat alphas_ipol.dat pdf.dat alphas_ana.dat alphas_ode.dat
