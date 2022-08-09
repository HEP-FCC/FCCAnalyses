macro(browse_directory directory)
  get_subdirectories(SUBDIRS ${directory})
  foreach(_dir ${SUBDIRS})
    get_subdirectories(ANALYSIS_DIR_STRUCT ${directory}/${_dir})
    if(("src" IN_LIST ANALYSIS_DIR_STRUCT) AND ("include" IN_LIST ANALYSIS_DIR_STRUCT))
      file(GLOB sources "${_dir}/src/*.cc")
      file(GLOB headers RELATIVE ${CMAKE_CURRENT_LIST_DIR} "${_dir}/include/*.h")
      list(FILTER headers EXCLUDE REGEX "LinkDef.h")
      file(GLOB linkdef "${_dir}/include/LinkDef.h")
      add_library(${_dir} SHARED ${sources} ${headers})
      target_include_directories(${_dir} PUBLIC $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
                                                $<BUILD_INTERFACE:${CMAKE_SOURCE_DIR}/addons>
                                                $<INSTALL_INTERFACE:include>)
      target_link_libraries(${_dir} PUBLIC FCCAnalyses)
      set_target_properties(${_dir} PROPERTIES PUBLIC_HEADER "${headers}")
      if(linkdef)
        ROOT_GENERATE_DICTIONARY(G__${_dir} ${headers}
                                 MODULE ${_dir}
                                 LINKDEF ${linkdef})
      endif()
      install(TARGETS ${_dir}
              EXPORT ${_dir}Targets
              RUNTIME DESTINATION "${INSTALL_BIN_DIR}" COMPONENT bin
              LIBRARY DESTINATION "${INSTALL_LIB_DIR}" COMPONENT shlib
              PUBLIC_HEADER DESTINATION "${INSTALL_INCLUDE_DIR}/${_dir}"
              COMPONENT analyses)
      if(linkdef)
        install(FILES "${CMAKE_CURRENT_BINARY_DIR}/lib${_dir}.rootmap"
                DESTINATION "${INSTALL_LIB_DIR}"
                COMPONENT analyses)
        if(${ROOT_VERSION} GREATER 6)
          install(FILES "${CMAKE_CURRENT_BINARY_DIR}/lib${_dir}_rdict.pcm"
                  DESTINATION "${INSTALL_LIB_DIR}"
                  COMPONENT analyses)
        endif()
      endif()
      message(STATUS "analysis-------------------------- ${_dir}")
    else()
      browse_directory(${_dir})
    endif()
  endforeach()
endmacro()

browse_directory(${CMAKE_CURRENT_SOURCE_DIR})
