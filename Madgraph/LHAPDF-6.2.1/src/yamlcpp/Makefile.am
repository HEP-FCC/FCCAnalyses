## How to make our mangled yaml-cpp from the yaml-cpp-0.3.0.tar.gz tarball
# tar xf yaml-cpp-0.3.0.tar.gz
# for i in `find yaml-cpp -type f -name "*.h" -o -name "*.cpp"`; do \
#   sed -e 's/namespace YAML/namespace LHAPDF_YAML/' -e 's/YAML::/LHAPDF_YAML::/g' -i; done
# mv yaml-cpp{,.bak} && cp yaml-cpp.bak/include/yaml-cpp . -r && cp yaml-cpp.bak/src/*.{h,cpp} .

EXTRA_DIST = yaml-cpp
noinst_LTLIBRARIES = liblhapdf-yaml-cpp.la
liblhapdf_yaml_cpp_la_CPPFLAGS = $(AM_CPPFLAGS) -I$(srcdir)
liblhapdf_yaml_cpp_la_SOURCES = \
  aliasmanager.cpp    emitterutils.cpp   ostream.cpp     simplekey.cpp \
  binary.cpp          exp.cpp            parser.cpp      singledocparser.cpp \
  conversion.cpp      iterator.cpp       regex.cpp       stream.cpp \
  directives.cpp      nodebuilder.cpp    scanner.cpp     tag.cpp \
  emitfromevents.cpp  node.cpp           scanscalar.cpp \
  emitter.cpp         nodeownership.cpp  scantag.cpp \
  emitterstate.cpp    null.cpp           scantoken.cpp
dist_noinst_HEADERS = \
  collectionstack.h  iterpriv.h       regeximpl.h        streamcharsource.h \
  directives.h       nodebuilder.h    scanner.h          stream.h \
  emitterstate.h     nodeownership.h  scanscalar.h       stringsource.h \
  emitterutils.h     ptr_stack.h      scantag.h          tag.h \
  exp.h              ptr_vector.h     setting.h          token.h \
  indentation.h      regex.h          singledocparser.h
