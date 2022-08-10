#!/usr/bin/env python3

def header_tmpl(filename: str):
    return """// -*- C++ -*-
//
/** FCCAnalysis module: @@@ANALYSIS_NAME@@@
 *
 * \\file """ + filename + """
 * \\author @@@AUTHOR_NAME@@@ <@@@AUTHOR_EMAIL@@@>
 *
 * Description:
 *   [...]
 */
"""

source_tmpl = header_tmpl('@@@SCRIPT_NAME@@@.cc') + """
#include "@@@SCRIPT_NAME@@@.h"
#include <iostream>

using namespace std;

namespace @@@ANALYSIS_NAME@@@ {
  void dummy_analysis() { cout << "Dummy analysis initialised." << endl; }

  rv::RVec<float> dummy_collection(const rv::RVec<edm4hep::ReconstructedParticleData>& parts) {
    rv::RVec<float> output;
    for (size_t i = 0; i < parts.size(); ++i)
      output.emplace_back(parts.at(i).momentum.x);
    return output;
  }
}  // namespace @@@ANALYSIS_NAME@@@"""

header_tmpl = header_tmpl('@@@SCRIPT_NAME@@@.h') + """
#ifndef @@@ANALYSIS_NAME@@@_@@@SCRIPT_NAME@@@_h
#define @@@ANALYSIS_NAME@@@_@@@SCRIPT_NAME@@@_h

#include "ROOT/RVec.hxx"
#include "edm4hep/ReconstructedParticle.h"

namespace @@@ANALYSIS_NAME@@@ {
  namespace rv = ROOT::VecOps;

  void dummy_analysis();
  rv::RVec<float> dummy_collection(const rv::RVec<edm4hep::ReconstructedParticleData>&);
}  // namespace @@@ANALYSIS_NAME@@@

#endif"""

class_tmpl = """namespace @@@ANALYSIS_NAME@@@ {
  struct dictionary {};
} // namespace @@@ANALYSIS_NAME@@@"""

xml_tmpl = """<lcgdict>
  <class name="@@@ANALYSIS_NAME@@@::dictionary"/>
</lcgdict>"""

cmake_tmpl = """cmake_minimum_required(VERSION 3.16.9)
project(@@@ANALYSIS_NAME@@@ CXX)
find_package(ROOT COMPONENTS ROOTVecOps ROOTDataFrame REQUIRED)
find_package(EDM4HEP REQUIRED)
#--- Set a better default for installation directory---------------------------
if(CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT)
  set(CMAKE_INSTALL_PREFIX "${CMAKE_CURRENT_LIST_DIR}/install" CACHE PATH "default install path" FORCE)
endif()
#--- Use GNU-style hierarchy for installing build products
include(GNUInstallDirs)
#--- Offer the user the choice of overriding the installation directories
set(FCCANALYSES_DIR "@@@FCCANALYSES_PATH@@@" CACHE PATH
    "Installation directory for FCCAnalyses framework")
set(INSTALL_LIB_DIR lib CACHE PATH "Installation directory for libraries")
set(INSTALL_BIN_DIR bin CACHE PATH "Installation directory for executables")
set(INSTALL_INCLUDE_DIR include CACHE PATH
    "Installation directory for header files")
#--- Find all paths to '@@@ANALYSIS_NAME@@@' library pieces
file(GLOB headers "include/*.h")
file(GLOB sources "src/*.cc")
file(GLOB classes "src/classes.h")
file(GLOB reflex_sel "src/classes.xml")
#--- generate the ROOT dictionary using a REFLEX selection
set(CMAKE_ROOTTEST_NOROOTMAP OFF)
REFLEX_GENERATE_DICTIONARY(lib@@@ANALYSIS_NAME@@@ ${headers} ${classes}
                           SELECTION ${reflex_sel})
#--- build the analysis library (linked against FCCAnalyses)
add_library(@@@ANALYSIS_NAME@@@ SHARED ${sources} ${headers} lib@@@ANALYSIS_NAME@@@.cxx)
target_include_directories(@@@ANALYSIS_NAME@@@ PUBLIC
                           ${FCCANALYSES_DIR} ${FCCANALYSES_DIR}/addons
                           include $<INSTALL_INTERFACE:include>)
target_link_directories(@@@ANALYSIS_NAME@@@ PUBLIC
                        ${FCCANALYSES_DIR} ${FCCANALYSES_DIR}/install/lib)
target_link_libraries(@@@ANALYSIS_NAME@@@ PUBLIC
                      FCCAnalyses
                      EDM4HEP::edm4hep
                      EDM4HEP::edm4hepDict
                      ROOT::ROOTVecOps)
set_target_properties(@@@ANALYSIS_NAME@@@ PROPERTIES PUBLIC_HEADER "${headers}")
install(TARGETS @@@ANALYSIS_NAME@@@
        EXPORT @@@ANALYSIS_NAME@@@Targets
        RUNTIME DESTINATION "${INSTALL_BIN_DIR}" COMPONENT bin
        LIBRARY DESTINATION "${INSTALL_LIB_DIR}" COMPONENT shlib
        PUBLIC_HEADER DESTINATION "${INSTALL_INCLUDE_DIR}/@@@ANALYSIS_NAME@@@"
        COMPONENT analyses)
install(FILES "${CMAKE_CURRENT_BINARY_DIR}/lib@@@ANALYSIS_NAME@@@.rootmap"
        DESTINATION "${INSTALL_LIB_DIR}"
        COMPONENT analyses)
if(${ROOT_VERSION} GREATER 6)
  install(FILES "${CMAKE_CURRENT_BINARY_DIR}/lib@@@ANALYSIS_NAME@@@_rdict.pcm"
          DESTINATION "${INSTALL_LIB_DIR}"
          COMPONENT analyses)
endif()
message(STATUS "Built standalone analyser package: @@@ANALYSIS_NAME@@@")
"""

def find_author():
    from subprocess import getoutput
    return (getoutput('git config --global --get user.name'),
            getoutput('git config --global --get user.email'))

def replace_all(input: str, repl) -> str:
    output = input
    for a, b in repl.items():
        output = output.replace(a, b)
    return output

def setup_analysis(name: str, author: str='', script: str='', standalone: bool=False, output_dir: str=''):
    if not author:
        author_name, author_email = find_author()
    else:
        author_list = author.split()
        if len(author) == 1:
            author_name = author
        else:
            author_name, author_email = author_list
            author_email = author_email.replace('<', '').replace('>', '')
    from subprocess import getoutput
    fccanalyses_dir = getoutput('git rev-parse --show-toplevel')
    replacement_dict = {
        '@@@ANALYSIS_NAME@@@': name,
        '@@@SCRIPT_NAME@@@': script,
        '@@@AUTHOR_NAME@@@': author_name,
        '@@@AUTHOR_EMAIL@@@': author_email,
        '@@@FCCANALYSES_PATH@@@': fccanalyses_dir
    }

    from os import mkdir
    if not output_dir:
        path = fccanalyses_dir + '/analyses/' + name
    else:
        path = output_dir
    for p in [path, path + '/src', path + '/include']:
        try:
            mkdir(p)
        except FileExistsError:
            print('Warning: FCCAnalysis space "' + name + ' already exists.')
            pass
    try:
        with open(path + '/src/' + script + '.cc', 'w') as f:
            f.write(replace_all(source_tmpl, replacement_dict))
        with open(path + '/src/classes.h', 'w') as f:
            f.write(replace_all(class_tmpl, replacement_dict))
        with open(path + '/src/classes.xml', 'w') as f:
            f.write(replace_all(xml_tmpl, replacement_dict))
        with open(path + '/include/' + script + '.h', 'w') as f:
            f.write(replace_all(header_tmpl, replacement_dict))
        if standalone:
            with open(path + '/CMakeLists.txt', 'w') as f:
                f.write(replace_all(cmake_tmpl, replacement_dict))
    except OSError as error:
        print('FCCAnalysis space "' + name + '" creation error:')
        print(error)

