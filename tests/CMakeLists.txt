
add_subdirectory(unittest)

add_subdirectory(benchmark)

function(add_integration_test _testname)

  add_test(NAME ${_testname} 
          COMMAND python config/FCCAnalysisRun.py ${_testname} --test --nevents 100 --bench
          WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
          )
  set_property(TEST ${_testname} APPEND PROPERTY ENVIRONMENT
    LD_LIBRARY_PATH=${CMAKE_BINARY_DIR}/analyzers/dataframe:$ENV{LD_LIBRARY_PATH}
    PYTHONPATH=${CMAKE_SOURCE_DIR}:$ENV{PYTHONPATH}
    ROOT_INCLUDE_PATH=${CMAKE_SOURCE_DIR}/analyzers/dataframe:$ENV{ROOT_INCLUDE_PATH}
    )
endfunction()

function(add_integration_test_2 _testname)

  add_test(NAME fccanalysisrun_${_testname} 
          # todo: figure out how to make ctest pick fccanalysis up from PATH
          COMMAND ${CMAKE_SOURCE_DIR}/bin/fccanalysis run ${_testname} --test --nevents 100 --bench
          WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
          )
  set_property(TEST fccanalysisrun_${_testname} APPEND PROPERTY ENVIRONMENT
    LD_LIBRARY_PATH=${CMAKE_BINARY_DIR}/analyzers/dataframe:$ENV{LD_LIBRARY_PATH}
    PYTHONPATH=${CMAKE_SOURCE_DIR}:$ENV{PYTHONPATH}
    PATH=${CMAKE_SOURCE_DIR}/bin:$CMAKE_BINARY_DIR:$ENV{PATH}
    ROOT_INCLUDE_PATH=${CMAKE_SOURCE_DIR}/analyzers/dataframe:$ENV{ROOT_INCLUDE_PATH}
    )
endfunction()


add_integration_test_2("examples/FCCee/higgs/mH-recoil/mumu/analysis_stage1.py")

add_integration_test("examples/FCCee/higgs/mH-recoil/mumu/analysis_stage1.py")
add_integration_test("examples/FCCee/flavour/Bc2TauNu/analysis_B2TauNu_truth.py")

