
add_executable(fcchh_ana_tth_4l fcchh_ana_tth_4l.cxx)
target_link_libraries(fcchh_ana_tth_4l ${FCCEDM_LIBRARIES} ROOT::ROOTDataFrame ROOT::Physics FCCAnalyses)
target_include_directories(fcchh_ana_tth_4l PUBLIC ${FCCEDM_INCLUDE_DIRS} ${ROOT_INCLUDE_DIRS} ${CMAKE_SOURCE_DIR}/analyzers/dataframe)
