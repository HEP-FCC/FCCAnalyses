AM_CPPFLAGS += -I$(top_srcdir)/include
AM_LDFLAGS += -L$(top_builddir)/src -L$(prefix)/lib
LIBS = -lLHAPDF

noinst_PROGRAMS = testpdf testpdfset analyticpdf compatibility testpdfunc hessian2replicas reweight
testpdf_SOURCES = testpdf.cc
testpdfset_SOURCES = testpdfset.cc
analyticpdf_SOURCES = analyticpdf.cc
compatibility_SOURCES = compatibility.cc
testpdfunc_SOURCES = testpdfunc.cc
hessian2replicas_SOURCES = hessian2replicas.cc
reweight_SOURCES = reweight.cc

## Python examples
EXTRA_DIST = pythonexample.py testpdfunc.py

## Fortran example: we don't build, since we didn't test for a compiler, but build like e.g.:
##   gfortran fexample1.f90 -o fexample1 -L/path/to/lhapdf/libdir -lLHAPDF -lstdc++
EXTRA_DIST += fexample1.f90
