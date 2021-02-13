
find_package(ROOT REQUIRED COMPONENTS ROOTDataFrame ROOTVecOps)
include(${ROOT_USE_FILE})
#include("${ROOT_DIR}/modules/RootNewMacros.cmake")


find_package(fccedm)
find_package(EDM4HEP)
find_package(podio)


set(CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/cmake ${CMAKE_MODULE_PATH})

find_package(FastJet)



get_target_property(EDM4HEP_INCLUDE_DIRS EDM4HEP::edm4hep INTERFACE_INCLUDE_DIRECTORIES)

include_directories(${EDM4HEP_INCLUDE_DIRS} ${podio_INCLUDE_DIR} ${FASTJET_INCLUDE_DIR} ${FCCEDM_INCLUDE_DIRS})

ROOT_GENERATE_DICTIONARY(G__FCCAnalyses MCParticle.h
					ReconstructedParticle.h
					ReconstructedParticle2Track.h
					ReconstructedParticle2MC.h
					Algorithm.h
					JetClustering.h
					Vertexing.h
					LINKDEF LinkDef.h)


file(GLOB sources *.cc)
file(GLOB headers *.h)
add_library(FCCAnalyses SHARED ${sources} ${headers} G__FCCAnalyses.cxx )
target_include_directories(FCCAnalyses  PUBLIC
        ${CMAKE_SOURCE_DIR}/analyzers/dataframe
        "${FCCEDM_INCLUDE_DIRS}"
	      ${FASTJET_INCLUDE_DIR}

)
target_link_libraries(FCCAnalyses ${FCCEDM_LIBRARIES} ROOT::Physics ROOT::MathCore ROOT::ROOTVecOps ROOT::ROOTDataFrame EDM4HEP::edm4hep EDM4HEP::edm4hepDict podio::podio ${FASTJET_LIBRARY})

set_target_properties(FCCAnalyses PROPERTIES
  PUBLIC_HEADER "${headers}")

install(TARGETS FCCAnalyses
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
