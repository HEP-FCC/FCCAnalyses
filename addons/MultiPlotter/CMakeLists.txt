find_package(ROOT COMPONENTS HistPainter REQUIRED)
find_package(pybind11 REQUIRED)
message(STATUS "includes-------------------------- pybind11: ${pybind11_INCLUDE_DIRS}")

file(GLOB sources src/*.cc)
file(GLOB headers *.h)

include_directories(${CMAKE_CURRENT_SOURCE_DIR})

reflex_build_dictionary(MultiPlotter src/classes.h src/classes_def.xml
  LIBRARIES ROOT::Core pybind11::pybind11
  OPTIONS ${ROOTCLING_OPTIONS} -I$<TARGET_PROPERTY:pybind11::headers,INTERFACE_INCLUDE_DIRECTORIES> -I${CMAKE_CURRENT_SOURCE_DIR})
list(APPEND sources MultiPlotterDict.cxx)

fccanalyses_addon_build(MultiPlotter
                        SOURCES ${sources} ${headers}
                        #EXT_HEADERS ${FASTJET_INCLUDE_DIRS}
                        EXT_LIBS ROOT::HistPainter pybind11::pybind11
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

install(TARGETS MultiPlotterDict LIBRARY DESTINATION ${CMAKE_INSTALL_PREFIX}/lib RUNTIME DESTINATION ${CMAKE_INSTALL_PREFIX}/bin)
install(FILES
  "${PROJECT_BINARY_DIR}/addons/MultiPlotter/MultiPlotterDict.rootmap"
    DESTINATION "${INSTALL_LIB_DIR}" COMPONENT dev)

if (${ROOT_VERSION} GREATER 6)
    install(FILES
          "${PROJECT_BINARY_DIR}/addons/MultiPlotter/MultiPlotter_rdict.pcm"
                DESTINATION "${INSTALL_LIB_DIR}" COMPONENT dev)
endif()
