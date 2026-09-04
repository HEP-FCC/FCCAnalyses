find_package(FastJet REQUIRED)
message(STATUS "includes-------------------------- fastjet: ${FASTJET_INCLUDE_DIRS}")

file(GLOB sources src/*.cc)
file(GLOB headers *.h)

fccanalyses_addon_build(FastJet
                        SOURCES ${sources} ${headers}
                        EXT_HEADERS ${FASTJET_INCLUDE_DIRS}
                        EXT_LIBS ${FASTJET_LIBRARIES}
                                 ROOT::MathCore
                                 ROOT::ROOTVecOps
                        INSTALL_COMPONENT fastjet)

# Prefer FastJet's RPATH over LD_LIBRARY_PATH, so it doesn't pick up a
# different FastJet build (e.g. Delphes' bundled copy) found earlier on
# the search path.
target_link_options(FastJet PRIVATE -Wl,--disable-new-dtags)

add_custom_command(TARGET FastJet POST_BUILD
                   COMMAND ${CMAKE_COMMAND} -E copy
                   ${CMAKE_CURRENT_SOURCE_DIR}/python/*
                   ${CMAKE_CURRENT_BINARY_DIR}
)


install(FILES
   ${CMAKE_CURRENT_LIST_DIR}/ExternalRecombiner.h
   ${CMAKE_CURRENT_LIST_DIR}/ValenciaPlugin.h
   ${CMAKE_CURRENT_LIST_DIR}/JetClustering.h
   DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/FastJet
   )

file(GLOB _addon_python_files python/*.py)
install(FILES ${_addon_python_files} DESTINATION ${CMAKE_INSTALL_PREFIX}/python/addons/FastJet)
