
find_package(ROOT)
include(${ROOT_USE_FILE})


find_package(fccedm)
find_package(EDM4HEP)
find_package(podio)


set(CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/cmake ${CMAKE_MODULE_PATH})

find_package(FastJet)

include_directories(
        ${CMAKE_SOURCE_DIR}/analyzers/dataframe
        "${FCCEDM_INCLUDE_DIRS}"
	${FASTJET_INCLUDE_DIR}
        )

file(GLOB sources *.cc)
file(GLOB headers *.h)



ROOT_GENERATE_DICTIONARY(G__FCCAnalyses MCParticle.h ReconstructedParticle.h ReconstructedParticle2Track.h ReconstructedParticle2MC.h Algorithm.h JetClustering.h LINKDEF LinkDef.h)

add_library(FCCAnalyses SHARED ${sources} ${headers} G__FCCAnalyses.cxx )
target_link_libraries(FCCAnalyses ${FCCEDM_LIBRARIES} ROOT::Physics EDM4HEP::edm4hep podio::podio ${FASTJET_LIBRARY})

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
