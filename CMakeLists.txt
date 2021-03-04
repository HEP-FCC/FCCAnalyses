cmake_minimum_required(VERSION 3.1...3.16)
#cmake_minimum_required(VERSION 2.8)




project(FCCAnalyses CXX)

#needed for ACTS
cmake_policy(SET CMP0057 NEW)

find_package(ROOT COMPONENTS ROOTDataFrame)
include(${ROOT_USE_FILE})

find_package(EDM4HEP)
find_package(podio)


# Define basic build settings
# Use GNU-style hierarchy for installing build products
include(GNUInstallDirs)

	

set(CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/cmake ${CMAKE_MODULE_PATH})
find_package(FastJet)
find_package( Acts COMPONENTS Core )

# Offer the user the choice of overriding the installation directories
set(INSTALL_LIB_DIR lib CACHE PATH "Installation directory for libraries")
set(INSTALL_BIN_DIR bin CACHE PATH "Installation directory for executables")
set(INSTALL_INCLUDE_DIR include CACHE PATH
  "Installation directory for header files")


file(GLOB _run_python_files config/*.py)
install(FILES ${_run_python_files} DESTINATION ${CMAKE_INSTALL_PREFIX}/python/config)
install(FILES config/doPlots.py PERMISSIONS OWNER_EXECUTE OWNER_WRITE OWNER_READ DESTINATION ${CMAKE_INSTALL_PREFIX}/python/config)

#install(DIRECTORY FCCeeAnalyses DESTINATION ${CMAKE_INSTALL_PREFIX}/python)
#install(DIRECTORY FCChhAnalyses DESTINATION ${CMAKE_INSTALL_PREFIX}/python)

add_subdirectory(analyzers/dataframe)


option(FCCANALYSES_DOCUMENTATION "Whether or not to create doxygen doc target." ON)

if(FCCANALYSES_DOCUMENTATION)
  include(cmake/FCCANALYSESDoxygen.cmake)
endif()

execute_process(COMMAND python -m awkward.config --incdir OUTPUT_VARIABLE AWKWARD_INCLUDE OUTPUT_STRIP_TRAILING_WHITESPACE)
execute_process(COMMAND python -m awkward.config --libdir OUTPUT_VARIABLE AWKWARD_LIBRARIES OUTPUT_STRIP_TRAILING_WHITESPACE)

include_directories(BEFORE "${AWKWARD_INCLUDE}")

find_library(CPU-KERNELS awkward-cpu-kernels REQUIRED HINTS ${AWKWARD_LIBRARIES})
find_library(LIBAWKWARD awkward REQUIRED HINTS ${AWKWARD_LIBRARIES})
find_library(LIBDL dl REQUIRED)

message(STATUS "Libraries: ${CPU-KERNELS} ${LIBAWKWARD} ${LIBDL}")
message(STATUS "includes---------------------: ${AWKWARD_INCLUDE}")
