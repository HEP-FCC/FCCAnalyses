find_package(FastJet REQUIRED)
message(STATUS "includes-------------------------- fastjet: ${FASTJET_INCLUDE_DIRS}")

file(GLOB sources src/*.cc)
file(GLOB headers *.h)

fccanalyses_addon_build(FastJet
                        SOURCES ${sources} ${headers}
                        EXT_HEADERS ${FASTJET_INCLUDE_DIRS}
                        EXT_LIBS ${FASTJET_LIBRARIES}
                                 ROOT::MathCore
                        INSTALL_COMPONENT fastjet)


install(FILES
   ${CMAKE_CURRENT_LIST_DIR}/ExternalRecombiner.h
   ${CMAKE_CURRENT_LIST_DIR}/ValenciaPlugin.h
   ${CMAKE_CURRENT_LIST_DIR}/JetClustering.h
   DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/FastJet
   )
