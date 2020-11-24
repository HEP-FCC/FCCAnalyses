add_executable(analysis analysis.cc)
target_link_libraries(analysis ${FCCEDM_LIBRARIES} EDM4HEP::edm4hep ROOT::ROOTDataFrame ROOT::Physics FCCAnalyses)
target_include_directories(analysis PUBLIC ${FCCEDM_INCLUDE_DIRS} ${ROOT_INCLUDE_DIRS} ${CMAKE_SOURCE_DIR}/analyzers/dataframe)
