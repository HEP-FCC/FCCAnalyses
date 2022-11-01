SUBDIRS = yamlcpp

lib_LTLIBRARIES = libLHAPDF.la
noinst_LTLIBRARIES = libLHAPDFInfo.la libLHAPDFPaths.la

AM_CPPFLAGS += -I$(top_srcdir)/include -I$(prefix)/include
AM_LDFLAGS += -L$(top_builddir)/src -L$(prefix)/lib -avoid-version

libLHAPDF_la_SOURCES = \
  PDF.cc PDFSet.cc GridPDF.cc PDFInfo.cc \
  Interpolator.cc BilinearInterpolator.cc BicubicInterpolator.cc \
  LogBilinearInterpolator.cc LogBicubicInterpolator.cc \
  ErrExtrapolator.cc NearestPointExtrapolator.cc  ContinuationExtrapolator.cc \
  AlphaS.cc AlphaS_Analytic.cc AlphaS_ODE.cc AlphaS_Ipol.cc \
  Config.cc Factories.cc PDFIndex.cc Utils.cc

libLHAPDFInfo_la_SOURCES = Info.cc
libLHAPDFInfo_la_CPPFLAGS = -I$(srcdir)/yamlcpp -DYAMLCPP_API=3 -DYAML_NAMESPACE=LHAPDF_YAML $(AM_CPPFLAGS)
libLHAPDFInfo_la_LIBADD = $(builddir)/yamlcpp/liblhapdf-yaml-cpp.la

libLHAPDFPaths_la_SOURCES = Paths.cc
libLHAPDFPaths_la_CPPFLAGS = $(AM_CPPFLAGS) -DLHAPDF_INSTALL_PREFIX=\"$(prefix)\" -DLHAPDF_DATA_PREFIX=\"$(datadir)\"

libLHAPDF_la_LIBADD = libLHAPDFInfo.la libLHAPDFPaths.la

if ENABLE_LHAGLUE
  noinst_LTLIBRARIES += libLHAPDFGlue.la
  libLHAPDFGlue_la_SOURCES = LHAGlue.cc
  libLHAPDFGlue_la_CPPFLAGS = $(AM_CPPFLAGS) -DENABLE_LHAGLUE_CXX
  libLHAPDF_la_LIBADD += libLHAPDFGlue.la
endif
