ACLOCAL_AMFLAGS = -I m4

SUBDIRS = src include wrappers tests bin
DIST_SUBDIRS = $(SUBDIRS) examples doc

dist_noinst_SCRIPTS = mkindex plotpdfs testpdfs testlhapdf
dist_pkgdata_DATA = lhapdf.conf pdfsets.index

pkgconfigdir = $(libdir)/pkgconfig
dist_pkgconfig_DATA = lhapdf.pc

tests:
	(cd tests && $(MAKE))

examples:
	(cd examples && $(MAKE))

if WITH_DOXYGEN
doxy:
	(cd doc && $(MAKE) doxy)
endif

if WITH_PDFLATEX
manual:
	(cd doc && $(MAKE) manual)
endif

## Clean out SVN and hg files
dist-hook:
	rm -rf `find $(distdir) -name ".svn" -o -name ".hg"`

## Remove the unused & misleading share/LHAPDF/sets directory on both install and uninstall!
# TODO: Remove this hook entirely after a couple of versions
install-data-hook:
	test -e $(pkgdatadir)/sets && rmdir $(pkgdatadir)/sets || true
uninstall-hook:
	test -e $(pkgdatadir)/sets && rmdir $(pkgdatadir)/sets || true
