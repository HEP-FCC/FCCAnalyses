#!/usr/bin/env python3

def header_boilerplate(filename: str):
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

source_tmpl = header_boilerplate('@@@SCRIPT_NAME@@@.cc') + """
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

header_tmpl = header_boilerplate('@@@SCRIPT_NAME@@@.h') + """
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

class_tmpl = """
namespace @@@ANALYSIS_NAME@@@ {
  struct dictionary {};
} // namespace @@@ANALYSIS_NAME@@@"""

xml_tmpl = """<lcgdict>
  <class name="@@@ANALYSIS_NAME@@@::dictionary"/>
</lcgdict>"""

cmake_tmpl = """cmake_minimum_required(VERSION 3.16.9)
project(@@@ANALYSIS_NAME@@@ CXX)
set(lib_name "FCCAnalysis_@@@ANALYSIS_NAME@@@")
find_package(ROOT COMPONENTS ROOTVecOps ROOTDataFrame REQUIRED)
find_package(EDM4HEP REQUIRED)
#--- Set a better default for installation directory---------------------------
if(CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT)
  set(CMAKE_INSTALL_PREFIX "@@@FCCANALYSES_PATH@@@/install" CACHE PATH "default install path" FORCE)
endif()
#--- Offer the user the choice of overriding the installation directories
set(FCCANALYSES_DIR "@@@FCCANALYSES_PATH@@@" CACHE PATH
    "Installation directory for FCCAnalyses framework")
#--- Find all paths to '@@@ANALYSIS_NAME@@@' library pieces
file(GLOB headers "include/*.h")
file(GLOB sources "src/*.cc")
file(GLOB classes "src/classes.h")
file(GLOB reflex_sel "src/classes_def.xml")
#--- generate the ROOT dictionary using a REFLEX selection
set(CMAKE_ROOTTEST_NOROOTMAP OFF)
reflex_generate_dictionary(lib${lib_name} ${headers} ${classes}
                           SELECTION ${reflex_sel})
#--- build the analysis library (linked against FCCAnalyses)
add_library(${lib_name} SHARED ${sources} ${headers} lib${lib_name}.cxx)
target_include_directories(${lib_name} PUBLIC include
                                              ${FCCANALYSES_DIR}
                                              ${FCCANALYSES_DIR}/addons
                                              $<INSTALL_INTERFACE:include>)
target_link_directories(${lib_name} PUBLIC ${FCCANALYSES_DIR}
                                           ${FCCANALYSES_DIR}/install/lib)
target_link_libraries(${lib_name} PUBLIC FCCAnalyses
                                         EDM4HEP::edm4hep EDM4HEP::edm4hepDict
                                         ROOT::ROOTVecOps)
set_target_properties(${lib_name} PROPERTIES PUBLIC_HEADER "${headers}")
install(TARGETS ${lib_name}
        RUNTIME DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" COMPONENT bin
        LIBRARY DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" COMPONENT shlib
        PUBLIC_HEADER DESTINATION "${CMAKE_INSTALL_PREFIX}/include/@@@ANALYSIS_NAME@@@"
        COMPONENT analyses)
install(FILES "${CMAKE_CURRENT_BINARY_DIR}/lib${lib_name}.rootmap"
        DESTINATION "${CMAKE_INSTALL_PREFIX}/lib"
        COMPONENT analyses)
if(${ROOT_VERSION} GREATER 6)
  install(FILES "${CMAKE_CURRENT_BINARY_DIR}/lib${lib_name}_rdict.pcm"
          DESTINATION "${CMAKE_INSTALL_PREFIX}/lib"
          COMPONENT analyses)
endif()
message(STATUS "Built standalone analyser package: @@@ANALYSIS_NAME@@@")
"""

config_tmpl = """#Optional: List of analysis packages to load in runtime
analysesList = ['@@@ANALYSIS_NAME@@@']

#Mandatory: List of processes
processList = {
    'p8_noBES_ee_H_Hbb_ecm125':{'fraction':0.01, 'chunks':1, 'output':'test_out'}
}

#Mandatory: Production tag when running over EDM4Hep centrally produced events, this points to the yaml files for getting sample statistics
prodTag     = "FCCee/spring2021/IDEA/"

#Optional: output directory, default is local running directory
outputDir   = "."

#Optional
nCPUS       = 8
runBatch    = False
#batchQueue = "longlunch"
#compGroup = "group_u_FCC.local_gen"

#Optional test file
testFile ="root://eospublic.cern.ch//eos/experiment/fcc/ee/generation/DelphesEvents/spring2021/IDEA/p8_ee_ZH_ecm240/events_101027117.root"

#Mandatory: RDFanalysis class where the use defines the operations on the TTree
class RDFanalysis():
    #__________________________________________________________
    #Mandatory: analysers function to define the analysers to process, please make sure you return the last dataframe, in this example it is df2
    def analysers(df):
        df2 = (df
               .Define("dummy_collection", "@@@ANALYSIS_NAME@@@::dummy_collection(ReconstructedParticles)")
              )
        return df2

    #__________________________________________________________
    #Mandatory: output function, please make sure you return the branchlist as a python list
    def output():
        branchList = ['dummy_collection']
        return branchList"""

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
        path = f'{fccanalyses_dir}/case-studies/{name}'
    else:
        path = output_dir
    for p in [path, f'{path}/src', f'{path}/include', f'{path}/scripts']:
        try:
            mkdir(p)
        except FileExistsError:
            print(f'Warning: FCCAnalysis space "{name}" already exists.')
            pass
    try:
        with open(f'{path}/src/{script}.cc', 'w') as f:
            f.write(replace_all(source_tmpl, replacement_dict))
        with open(f'{path}/src/classes.h', 'w') as f:
            f.write(replace_all(class_tmpl, replacement_dict))
        with open(f'{path}/src/classes_def.xml', 'w') as f:
            f.write(replace_all(xml_tmpl, replacement_dict))
        with open(f'{path}/include/{script}.h', 'w') as f:
            f.write(replace_all(header_tmpl, replacement_dict))
        with open(f'{path}/scripts/analysis_cfg.py', 'w') as f:
            f.write(replace_all(config_tmpl, replacement_dict))
        if standalone:
            with open(f'{path}/CMakeLists.txt', 'w') as f:
                f.write(replace_all(cmake_tmpl, replacement_dict))
    except OSError as error:
        print(f'FCCAnalysis space "{name}" creation error:')
        print(error)

