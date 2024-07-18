find_package(TBB REQUIRED COMPONENTS tbb)
find_package(ROOT REQUIRED COMPONENTS TMVA TMVAUtils ROOTVecOps)

file(GLOB sources src/*.cc)
file(GLOB headers *.h)

fccanalyses_addon_build(TMVAHelper
                        SOURCES ${headers} ${sources}
                        EXT_LIBS ROOT::ROOTVecOps ROOT::TMVA ROOT::TMVAUtils
                                 TBB::tbb
                        INSTALL_COMPONENT tmvahelper
)

add_custom_command(
  TARGET TMVAHelper
  POST_BUILD
  COMMAND ${CMAKE_COMMAND} -E copy ${CMAKE_CURRENT_SOURCE_DIR}/python/*
                                   ${CMAKE_CURRENT_BINARY_DIR}
)

install(FILES
   ${CMAKE_CURRENT_LIST_DIR}/TMVAHelper.h
   DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/TMVAHelper
)

file(GLOB _addon_python_files python/*.py)
install(FILES ${_addon_python_files}
        DESTINATION ${CMAKE_INSTALL_PREFIX}/python/addons/TMVAHelper
)
