find_package(ROOT COMPONENTS HistPainter REQUIRED)
find_package(Python REQUIRED COMPONENTS Development)
find_package(pybind11 REQUIRED)
message(STATUS "includes-------------------------- pybind11: ${pybind11_INCLUDE_DIRS}")

file(GLOB sources src/*.cc)
file(GLOB headers *.h)

include_directories(${CMAKE_CURRENT_SOURCE_DIR})

set(dict_includes -I${CMAKE_CURRENT_SOURCE_DIR})
foreach(_include_dir ${pybind11_INCLUDE_DIRS})
  list(APPEND dict_includes -I${_include_dir})
endforeach()
reflex_build_dictionary(MultiPlotter src/classes.h src/classes_def.xml
  LIBRARIES ROOT::Core pybind11::pybind11
  OPTIONS ${ROOTCLING_OPTIONS} ${dict_includes})
list(APPEND sources MultiPlotterDict.cxx)

fccanalyses_addon_build(MultiPlotter
                        SOURCES ${sources} ${headers}
                        #EXT_HEADERS ${FASTJET_INCLUDE_DIRS}
                        EXT_LIBS ROOT::HistPainter pybind11::pybind11 Python::Python
                        INSTALL_COMPONENT multiplotter)

add_custom_command(TARGET MultiPlotter POST_BUILD
                   COMMAND ${CMAKE_COMMAND} -E copy
                   ${CMAKE_CURRENT_SOURCE_DIR}/python/*
                   ${CMAKE_CURRENT_BINARY_DIR}
)

install(DIRECTORY MultiPlotter/
        DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/MultiPlotter
        FILES_MATCHING PATTERN "*.h")

file(GLOB _addon_python_files python/*.py)
install(FILES ${_addon_python_files} DESTINATION ${CMAKE_INSTALL_PREFIX}/python/addons/MultiPlotter)

install(TARGETS MultiPlotterDict
        LIBRARY DESTINATION "${CMAKE_INSTALL_LIBDIR}"
        RUNTIME DESTINATION "${CMAKE_INSTALL_BINDIR}")
install(FILES "${PROJECT_BINARY_DIR}/addons/MultiPlotter/MultiPlotterDict.rootmap"
        DESTINATION "${CMAKE_INSTALL_LIBDIR}" COMPONENT dev)

if (${ROOT_VERSION} GREATER 6)
    install(FILES "${PROJECT_BINARY_DIR}/addons/MultiPlotter/MultiPlotter_rdict.pcm"
            DESTINATION "${CMAKE_INSTALL_LIBDIR}" COMPONENT dev)
endif()
