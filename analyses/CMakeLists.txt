get_subdirectories(SUBDIRS ${CMAKE_CURRENT_SOURCE_DIR})
foreach(_dir ${SUBDIRS})
  get_subdirectories(ANALYSIS_DIR_STRUCT ${CMAKE_CURRENT_SOURCE_DIR}/${_dir})
  if("src" IN_LIST ANALYSIS_DIR_STRUCT)
    file(GLOB sources "${_dir}/src/*.cc")
    add_library(${_dir} SHARED ${sources})
    target_link_libraries(${_dir} PUBLIC FCCAnalyses)
    target_include_directories(${_dir} PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})
    #if("include" IN_LIST ANALYSIS_DIR_STRUCT)
    #  target_include_directories(${_dir} PUBLIC "${_dir}/include")
    #endif()
    install(TARGETS ${_dir}
            EXPORT FCCAnalysesTargets
            RUNTIME DESTINATION "${INSTALL_BIN_DIR}" COMPONENT bin
            LIBRARY DESTINATION "${INSTALL_LIB_DIR}" COMPONENT shlib
            PUBLIC_HEADER DESTINATION "${INSTALL_INCLUDE_DIR}/${_dir}"
            COMPONENT ${ARG_INSTALL_COMPONENT})
    message(STATUS "analysis-------------------------- ${_dir}")
  endif()
endforeach()
