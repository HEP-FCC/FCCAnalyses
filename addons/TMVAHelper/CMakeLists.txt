

find_package(TBB REQUIRED tbb)
find_package(ROOT)
find_package(ROOT COMPONENTS ROOTVecOps)
find_package(ROOT COMPONENTS TMVA)


message(STATUS "includes-------------------------- TEST: ${TBB_INCLUDE_DIRS}")

file(GLOB sources src/*.cc)
file(GLOB headers *.h)


fccanalyses_addon_build(TMVAHelper
                        SOURCES ${headers} ${sources}
#                        EXT_LIBS ROOT::ROOTVecOps ROOT::TMVA TBB::tbb
                        INSTALL_COMPONENT tmvahelper)

add_custom_command(TARGET TMVAHelper POST_BUILD
                   COMMAND ${CMAKE_COMMAND} -E copy
                   ${CMAKE_CURRENT_SOURCE_DIR}/python/*
                   ${CMAKE_CURRENT_BINARY_DIR}
)

target_link_libraries(TMVAHelper PRIVATE TBB::tbb)
target_link_libraries(TMVAHelper PRIVATE ROOT::ROOTVecOps)
target_link_libraries(TMVAHelper PRIVATE ROOT::TMVA)
target_compile_features(TMVAHelper PRIVATE cxx_std_11)

install(FILES
   ${CMAKE_CURRENT_LIST_DIR}/TMVAHelper.h
   DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/TMVAHelper
   )

file(GLOB _addon_python_files python/*.py)
install(FILES ${_addon_python_files} DESTINATION ${CMAKE_INSTALL_PREFIX}/python/addons/TMVAHelper)
