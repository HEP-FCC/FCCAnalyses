# - Use CMake's module to help generating relocatable config files
include(CMakePackageConfigHelpers)


# - Install time config and target files
configure_package_config_file(${CMAKE_CURRENT_LIST_DIR}/FCCAnalysesConfig.cmake.in
  "${PROJECT_BINARY_DIR}/FCCAnalysesConfig.cmake"
  INSTALL_DESTINATION "${CMAKE_INSTALL_LIBDIR}/cmake/FCCAnalyses"
  PATH_VARS
    CMAKE_INSTALL_BINDIR
    CMAKE_INSTALL_INCLUDEDIR
    CMAKE_INSTALL_LIBDIR
  )

# - install and export
install(FILES
  "${PROJECT_BINARY_DIR}/FCCAnalysesConfig.cmake"
  DESTINATION "${CMAKE_INSTALL_LIBDIR}/cmake/FCCAnalyses"
  )
install(EXPORT FCCAnalysesTargets
  NAMESPACE FCCAnalyses::
  DESTINATION "${CMAKE_INSTALL_LIBDIR}/cmake/FCCAnalyses"
  )

