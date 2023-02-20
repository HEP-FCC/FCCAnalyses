macro(build_analysis dir)
  file(GLOB headers "${dir}/include/*.h")
  file(GLOB sources "${dir}/src/*.cc")
  file(GLOB classes "${dir}/src/classes.h")
  file(GLOB reflex_sel "${dir}/src/classes_def.xml")
  file(GLOB ci_tests "${dir}/test/*.sh")
  set(lib_name "FCCAnalysis_${dir}")
  #--- generate the ROOT dictionary using a REFLEX selection
  set(CMAKE_ROOTTEST_NOROOTMAP OFF)
  reflex_generate_dictionary(lib${lib_name} ${headers} ${classes}
                             SELECTION ${reflex_sel})
  #--- build the analysis library (linked against FCCAnalyses)
  add_library(${lib_name} SHARED ${sources} ${headers} lib${lib_name}.cxx)
  target_include_directories(${lib_name} PUBLIC ${dir}/include
                                                $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
                                                $<BUILD_INTERFACE:${CMAKE_SOURCE_DIR}/addons>
                                                $<INSTALL_INTERFACE:include>)
  target_link_libraries(${lib_name} PUBLIC FCCAnalyses)
  set_target_properties(${lib_name} PROPERTIES PUBLIC_HEADER "${headers}")
  message(STATUS "analysis-------------------------- ${dir}: ${lib_name}")
  install(TARGETS ${lib_name}
          RUNTIME DESTINATION "${INSTALL_BIN_DIR}" COMPONENT bin
          LIBRARY DESTINATION "${INSTALL_LIB_DIR}" COMPONENT shlib
          PUBLIC_HEADER DESTINATION "${INSTALL_INCLUDE_DIR}/${dir}"
          COMPONENT analyses)
  install(FILES "${CMAKE_CURRENT_BINARY_DIR}/lib${lib_name}.rootmap"
          DESTINATION "${INSTALL_LIB_DIR}"
          COMPONENT analyses)
  if(${ROOT_VERSION} GREATER 6)
    install(FILES "${CMAKE_CURRENT_BINARY_DIR}/lib${lib_name}_rdict.pcm"
            DESTINATION "${INSTALL_LIB_DIR}"
            COMPONENT analyses)
  endif()
  foreach(_test ${ci_tests})
    get_filename_component(test_name ${_test} NAME_WE)
    add_generic_test("${lib_name}_${test_name}" ${_test})
  endforeach()
endmacro()

macro(browse_directory directory)
  #--- recursively browse the directory structure to find a package compatible with an analysis
  get_subdirectories(SUBDIRS ${directory})
  foreach(_dir ${SUBDIRS})
    get_subdirectories(ANALYSIS_DIR_STRUCT ${directory}/${_dir})
    if(("src" IN_LIST ANALYSIS_DIR_STRUCT) AND ("include" IN_LIST ANALYSIS_DIR_STRUCT))
      build_analysis(${_dir})
    else()
      #--- structure was not found; go one level deeper
      browse_directory(${_dir})
    endif()
  endforeach()
endmacro()

#--- start browsing for packages from this directory
browse_directory(${CMAKE_CURRENT_SOURCE_DIR})
