cmake_minimum_required(VERSION 3.16.9)
project(__pkgname__ CXX)
set(lib_name "FCCAnalysis___pkgname__")
find_package(ROOT COMPONENTS ROOTVecOps ROOTDataFrame REQUIRED)
find_package(EDM4HEP REQUIRED)
#--- Set a better default for installation directory---------------------------
if(CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT)
  set(CMAKE_INSTALL_PREFIX "__fccpath__/install" CACHE PATH "default install path" FORCE)
endif()
#--- Offer the user the choice of overriding the installation directories
set(FCCANALYSES_DIR "__fccpath__" CACHE PATH
    "Installation directory for FCCAnalyses framework")
#--- Find all paths to '__pkgname__' library pieces
file(GLOB headers "include/*.h")
file(GLOB sources "src/*.cc")
file(GLOB classes "src/classes.h")
file(GLOB reflex_sel "src/classes_def.xml")
#--- generate the ROOT dictionary using a REFLEX selection
set(CMAKE_ROOTTEST_NOROOTMAP OFF)
reflex_generate_dictionary(lib${lib_name} ${headers} ${classes}
                           SELECTION ${reflex_sel})
#--- build the analysis library (linked against FCCAnalyses)
add_library(${lib_name} SHARED ${sources} ${headers} lib${lib_name}.cxx)
target_include_directories(${lib_name} PUBLIC include
                                              ${FCCANALYSES_DIR}
                                              ${FCCANALYSES_DIR}/addons
                                              ${FCCANALYSES_DIR}/analyzers/dataframe
                                              $<INSTALL_INTERFACE:include>)
target_link_directories(${lib_name} PUBLIC ${FCCANALYSES_DIR}
                                           ${FCCANALYSES_DIR}/install/lib)
target_link_libraries(${lib_name} PUBLIC FCCAnalyses
                                         EDM4HEP::edm4hep EDM4HEP::edm4hepDict
                                         ROOT::ROOTVecOps)
set_target_properties(${lib_name} PROPERTIES PUBLIC_HEADER "${headers}")
install(TARGETS ${lib_name}
        RUNTIME DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" COMPONENT bin
        LIBRARY DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" COMPONENT shlib
        PUBLIC_HEADER DESTINATION "${CMAKE_INSTALL_PREFIX}/include/__pkgname__"
        COMPONENT analyses)
install(FILES "${CMAKE_CURRENT_BINARY_DIR}/lib${lib_name}.rootmap"
        DESTINATION "${CMAKE_INSTALL_PREFIX}/lib"
        COMPONENT analyses)
if(${ROOT_VERSION} GREATER 6)
  install(FILES "${CMAKE_CURRENT_BINARY_DIR}/lib${lib_name}_rdict.pcm"
          DESTINATION "${CMAKE_INSTALL_PREFIX}/lib"
          COMPONENT analyses)
endif()
message(STATUS "Built standalone analyser package: __pkgname__")
