add_subdirectory(unittest)

add_subdirectory(benchmark)

add_integration_test("examples/FCCee/higgs/mH-recoil/mumu/analysis_stage1.py")
add_integration_test("examples/FCCee/flavour/Bc2TauNu/analysis_B2TauNu_truth.py")
add_integration_test("examples/FCCee/test/jet_constituents.py")
add_integration_test("examples/FCCee/vertex_lcfiplus/analysis_V0.py")

if(WITH_SOURCE)
  add_integration_test("examples/data_source/histmaker_source.py")
  add_integration_test("examples/data_source/stages_source.py")
  add_integration_test("examples/data_source/analysis_stage1.py")
  add_standalone_test("examples/data_source/standalone.py")
endif()

add_standalone_test("examples/FCCee/fullSim/caloNtupleizer/analysis.py")

# C++ Analyses

# podio::DataSource
add_executable(test_data_source ${CMAKE_SOURCE_DIR}/tests/data_source/test_source.cxx)
target_include_directories(test_data_source PRIVATE ${CMAKE_SOURCE_DIR}/include)
target_link_libraries(test_data_source podio::podioDataSource
                                       EDM4HEP::edm4hep
)

add_executable(test_source_associations
               ${CMAKE_SOURCE_DIR}/tests/data_source/test_source_associations.cxx)
target_include_directories(test_source_associations PRIVATE
                           ${CMAKE_SOURCE_DIR}/include)
target_link_libraries(test_source_associations podio::podioDataSource
                                               EDM4HEP::edm4hep
                                               FCCAnalyses
)

# Low level access
add_executable(test_low_level ${CMAKE_SOURCE_DIR}/tests/data_source/test_low_level.cxx)
target_link_libraries(test_low_level ROOT::ROOTDataFrame
                                     podio::podioDataSource
                                     EDM4HEP::edm4hep
                                     EDM4HEP::edm4hepDict
)

add_executable(test_low_level_associations
               ${CMAKE_SOURCE_DIR}/tests/data_source/test_low_level_associations.cxx)
target_link_libraries(test_low_level_associations ROOT::ROOTDataFrame
                                                  podio::podioDataSource
                                                  EDM4HEP::edm4hep
                                                  EDM4HEP::edm4hepDict
                                                  FCCAnalyses
)

# TODO: make this test run in the spack build environment
#add_generic_test(build_new_case_study "tests/build_new_case_study.sh")
