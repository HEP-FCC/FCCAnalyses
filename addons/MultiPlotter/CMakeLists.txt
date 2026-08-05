find_package(ROOT COMPONENTS HistPainter REQUIRED)
message(STATUS "includes-------------------------- fastjet: ${FASTJET_INCLUDE_DIRS}")

file(GLOB sources src/*.cc)
file(GLOB headers *.h)

fccanalyses_addon_build(MultiPlotter
                        SOURCES ${sources} ${headers}
                        EXT_HEADERS ${FASTJET_INCLUDE_DIRS}
                        EXT_LIBS ROOT::HistPainter
                        INSTALL_COMPONENT multiplotter)

add_custom_command(TARGET MultiPlotter POST_BUILD
                   COMMAND ${CMAKE_COMMAND} -E copy
                   ${CMAKE_CURRENT_SOURCE_DIR}/python/*
                   ${CMAKE_CURRENT_BINARY_DIR}
)


install(FILES
   #${CMAKE_CURRENT_LIST_DIR}/ExternalRecombiner.h
   DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/MultiPlotter
   )

file(GLOB _addon_python_files python/*.py)
install(FILES ${_addon_python_files} DESTINATION ${CMAKE_INSTALL_PREFIX}/python/addons/MultiPlotter)
