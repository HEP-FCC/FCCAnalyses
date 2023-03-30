cmake_minimum_required(VERSION 3.16.9)


project(FCCAnalyses CXX)

#--- RPATH settings -----------------------------------------------------------

set(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE CACHE BOOL "RPATH USE LINK PATH")

#--- enable unit testing capabilities -----------------------------------------
include(CTest)


#--- options ------------------------------------------------------------------


set(WITH_ACTS OFF CACHE STRING "Build analyzers that need Acts")
set_property(CACHE WITH_ACTS PROPERTY STRINGS AUTO ON OFF)

set(WITH_DD4HEP AUTO CACHE STRING "Build analyzers that need DD4hep")
set_property(CACHE WITH_DD4HEP PROPERTY STRINGS AUTO ON OFF)

set(WITH_ONNX AUTO CACHE STRING "Build analyzers that need ONNXRuntime")
set_property(CACHE WITH_ONNX PROPERTY STRINGS AUTO ON OFF)

option(FCCANALYSES_CASESTUDIES "Build the case studies" OFF)

option(USE_EXTERNAL_CATCH2 "Link against an external Catch2 v3 static library, otherwise build it locally" ON)

option(FCCANALYSES_DOCUMENTATION "Whether or not to create doxygen doc target." ON)

#--- Set a better default for installation directory---------------------------
if(CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT)
  set(CMAKE_INSTALL_PREFIX "${CMAKE_CURRENT_LIST_DIR}/install" CACHE PATH "default install path" FORCE)
endif()

# Use GNU-style hierarchy for installing build products
include(GNUInstallDirs)

# Offer the user the choice of overriding the installation directories
set(INSTALL_LIB_DIR lib CACHE PATH "Installation directory for libraries")
set(INSTALL_BIN_DIR bin CACHE PATH "Installation directory for executables")
set(INSTALL_INCLUDE_DIR include CACHE PATH
  "Installation directory for header files")


#--- Declare C++ Standard -----------------------------------------------------

set(CMAKE_CXX_STANDARD 17 CACHE STRING "")
if(NOT CMAKE_CXX_STANDARD MATCHES "17")
  message(FATAL_ERROR "Unsupported C++ standard: ${CMAKE_CXX_STANDARD}")
endif()
message (STATUS "C++ standard: ${CMAKE_CXX_STANDARD}")

#--- Dependencies -------------------------------------------------------------

find_package(ROOT COMPONENTS ROOTVecOps ROOTDataFrame REQUIRED)
find_package(EDM4HEP REQUIRED)
find_package(podio)

# need to use our own FindFastJet.cmake
set(CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/cmake ${CMAKE_MODULE_PATH})
find_package(FastJet)

find_package( Delphes REQUIRED )


if(WITH_ACTS)
  find_package( Acts COMPONENTS Core )
  if(Acts_FOUND)

  elseif(WITH_ACTS STREQUAL AUTO)
    message(WARNING "Acts not found. Skipping Acts-dependent analyzers.")
    set(WITH_ACTS OFF)
  else()
    message(FATAL_ERROR "Failed to locate Acts!")
  endif()
endif()


if(WITH_DD4HEP)
  find_package(DD4hep)
  if(DD4hep_FOUND)

  elseif(WITH_DD4HEP STREQUAL AUTO)
    message(WARNING "DD4hep not found. Skipping DD4hep-dependent analyzers.")
    set(WITH_DD4HEP OFF)
  else()
    message(FATAL_ERROR "Failed to locate DD4hep!")
  endif()
endif()


if(WITH_ONNX AND BUILD_TESTING) # currently these files are only needed by ONNX-parts
# Grab the test files into a cached directory
  if(NOT DEFINED CACHE{TEST_INPUT_DATA_DIR})
    message(STATUS "Getting test input files")
    execute_process(COMMAND bash ${CMAKE_CURRENT_LIST_DIR}/tests/get_test_inputs.sh
                    OUTPUT_VARIABLE test_input_data_dir
                    RESULT_VARIABLE test_inputs_available)
    if(NOT "${test_inputs_available}" STREQUAL "0")
      message(WARNING "Failed to retrieve input test files. Some tests will need to be skipped.")
      unset(TEST_INPUT_DATA_DIR CACHE)
    else()
      message(STATUS "Test input files stored in ${test_input_data_dir}")
      set(TEST_INPUT_DATA_DIR ${test_input_data_dir} CACHE INTERNAL "directory for input test files")
      mark_as_advanced(TEST_INPUT_DATA_DIR)
    endif()
  endif()
endif()

#--- add CMake infrastructure --------------------------------------------------
include(cmake/FCCAnalysesCreateConfig.cmake)
include(cmake/FCCAnalysesFunctions.cmake)

file(COPY bin/fccanalysis
  DESTINATION ${CMAKE_BINARY_DIR}
  FILE_PERMISSIONS OWNER_READ OWNER_WRITE OWNER_EXECUTE GROUP_READ
  GROUP_EXECUTE WORLD_READ WORLD_EXECUTE)
install(PROGRAMS bin/fccanalysis DESTINATION bin)


file(GLOB _run_python_files config/*.py)
install(FILES ${_run_python_files} DESTINATION ${CMAKE_INSTALL_PREFIX}/python/config)
install(FILES config/doPlots.py PERMISSIONS OWNER_EXECUTE OWNER_WRITE OWNER_READ DESTINATION ${CMAKE_INSTALL_PREFIX}/python/config)


#--- Descend into subdirectories ----------------------------------------------

set(ADDONS_LIBRARIES CACHE STRING "List of external libraries the RDF utilities will be linked against")
add_subdirectory(addons)
add_subdirectory(analyzers/dataframe)

add_subdirectory(case-studies)
if(FCCANALYSES_CASESTUDIES)
  add_subdirectory(analyzers/dataframe/case-studies FCCANALYSES_CASESTUDIES)
endif()


if(FCCANALYSES_DOCUMENTATION)
  include(cmake/FCCANALYSESDoxygen.cmake)
endif()

if(BUILD_TESTING)
  add_subdirectory(tests)
endif()
