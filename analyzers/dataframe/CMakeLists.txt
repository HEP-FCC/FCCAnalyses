
find_package(ROOT REQUIRED COMPONENTS ROOTDataFrame ROOTVecOps)
include(${ROOT_USE_FILE})
#include("${ROOT_DIR}/modules/RootNewMacros.cmake")

find_package(Vdt)

set(CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/cmake ${CMAKE_MODULE_PATH})

get_target_property(EDM4HEP_INCLUDE_DIRS EDM4HEP::edm4hep INTERFACE_INCLUDE_DIRECTORIES)

include_directories(${EDM4HEP_INCLUDE_DIRS}
                    ${podio_INCLUDE_DIR}
                    ${FASTJET_INCLUDE_DIR}
                    ${acts_INCLUDE_DIR}
                    ${AWKWARD_INCLUDE}
                    ${VDT_INCLUDE_DIR}
                    )

message(STATUS "includes-------------------------- dataframe awkward:     ${AWKWARD_INCLUDE}")
message(STATUS "includes-------------------------- dataframe edm4hep:     ${EDM4HEP_INCLUDE_DIRS}")
message(STATUS "includes-------------------------- dataframe podio  :     ${podio_INCLUDE_DIR}")
message(STATUS "includes-------------------------- dataframe fastjet:     ${FASTJET_INCLUDE_DIRS}")

set(EXTRA_INCLUDE_DIRS)
set(EXTRA_LIBRARIES)

if(WITH_ONNX STREQUAL AUTO OR WITH_ONNX)
  find_package(ONNXRuntime QUIET)
  find_package(nlohmann_json QUIET)
  if(ONNXRuntime_FOUND AND nlohmann_json_FOUND)
    message(STATUS "includes-------------------------- dataframe onnxruntime: ${ONNXRUNTIME_INCLUDE_DIRS}")
    message(STATUS "includes-------------------------- dataframe nlohmann_json")
    list(APPEND EXTRA_INCLUDE_DIRS ${ONNXRUNTIME_INCLUDE_DIRS})
    list(APPEND EXTRA_LIBRARIES ${ONNXRUNTIME_LIBRARIES} nlohmann_json::nlohmann_json)
    include_directories(${ONNXRUNTIME_INCLUDE_DIRS})
  elseif(WITH_ONNX STREQUAL AUTO)
    message(WARNING "ONNXRuntime and/or nlohmann's JSON libraries not found.")
  else()
    message(FATAL_ERROR "Failed to locate ONNXRuntime and/or nlohmann's JSON library!")
  endif()
endif()


file(GLOB sources src/*.cc)
file(GLOB headers RELATIVE ${CMAKE_CURRENT_LIST_DIR} FCCAnalyses/*.h)

message(STATUS "includes headers ${headers}")
message(STATUS "includes sources ${sources}")

list(FILTER headers EXCLUDE REGEX "LinkDef.h")
if(NOT ${WITH_DD4HEP})
  list(FILTER headers EXCLUDE REGEX "CaloNtupleizer.h")
  list(FILTER sources EXCLUDE REGEX "CaloNtupleizer.cc")
endif()
if(NOT ${WITH_ONNX})
  list(FILTER headers EXCLUDE REGEX "JetFlavourUtils.h")
  list(FILTER sources EXCLUDE REGEX "JetFlavourUtils.cc")
  list(FILTER headers EXCLUDE REGEX "ONNXRuntime.h")
  list(FILTER sources EXCLUDE REGEX "ONNXRuntime.cc")
  list(FILTER headers EXCLUDE REGEX "WeaverInterface.h")
  list(FILTER sources EXCLUDE REGEX "WeaverInterface.cc")
endif()


message(STATUS "CMAKE_CURRENT_SOURCE_DIR  ${CMAKE_CURRENT_SOURCE_DIR}")
message(STATUS "CMAKE_INSTALL_INCLUDEDIR  ${CMAKE_INSTALL_INCLUDEDIR}")

add_library(FCCAnalyses SHARED  ${sources} ${headers} )
target_include_directories(FCCAnalyses  PUBLIC
                           $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
                           $<INSTALL_INTERFACE:include>
                           ${FASTJET_INCLUDE_DIR}
                           ${acts_INCLUDE_DIR}
                           ${AWKWARD_INCLUDE}
                           ${EXTRA_INCLUDE_DIRS}
                           )

target_link_libraries(FCCAnalyses
                      ROOT::Physics
                      ROOT::MathCore
                      ROOT::ROOTVecOps
                      ROOT::ROOTDataFrame
                      EDM4HEP::edm4hep
                      EDM4HEP::edm4hepDict
                      podio::podio
                      ${FASTJET_LIBRARY}
                      ${FASTJET_LIBRARY_DIRS}/libfastjetplugins.so
                      ${acts_LIBRARY}
                      ActsCore
                      #${AWKWARD_LIBRARIES}
                      ${LIBAWKWARD}
                      ${CPU-KERNELS}
                      ${LIBDL}
                      ${EXTRA_LIBRARIES}
                      gfortran # todo: why necessary?
                      )

if(${WITH_DD4HEP})
  find_package(DD4hep)
  target_link_libraries(FCCAnalyses DD4hep::DDCore)
endif()

set_target_properties(FCCAnalyses PROPERTIES
  PUBLIC_HEADER "${headers}")

ROOT_GENERATE_DICTIONARY(G__FCCAnalyses
                         ${headers}
                         MODULE FCCAnalyses
                         LINKDEF FCCAnalyses/LinkDef.h
                         )

install(TARGETS FCCAnalyses
    EXPORT FCCAnalysesTargets
    RUNTIME DESTINATION "${INSTALL_BIN_DIR}" COMPONENT bin
    LIBRARY DESTINATION "${INSTALL_LIB_DIR}" COMPONENT shlib
    PUBLIC_HEADER DESTINATION "${INSTALL_INCLUDE_DIR}/FCCAnalyses"
    COMPONENT dev
    )

install(FILES
  "${PROJECT_BINARY_DIR}/analyzers/dataframe/libFCCAnalyses.rootmap"
    DESTINATION "${INSTALL_LIB_DIR}" COMPONENT dev)

if (${ROOT_VERSION} GREATER 6)
    install(FILES
          "${PROJECT_BINARY_DIR}/analyzers/dataframe/libFCCAnalyses_rdict.pcm"
                DESTINATION "${INSTALL_LIB_DIR}" COMPONENT dev)
    endif()
