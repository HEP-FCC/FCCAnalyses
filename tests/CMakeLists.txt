
add_subdirectory(unittest)

function(add_integration_test _testname)

  add_test(NAME ${_testname} 
          COMMAND python config/FCCAnalysisRun.py ${_testname} --test
          WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
          )
  set_property(TEST ${_testname} APPEND PROPERTY ENVIRONMENT
    LD_LIBRARY_PATH=${CMAKE_BINARY_DIR}/analyzers/dataframe:$ENV{LD_LIBRARY_PATH}
    PYTHONPATH=${CMAKE_SOURCE_DIR}:$ENV{PYTHONPATH}
    ROOT_INCLUDE_PATH=${CMAKE_SOURCE_DIR}/analyzers/dataframe:$ENV{ROOT_INCLUDE_PATH}
    )
endfunction()

add_integration_test("examples/FCCee/higgs/mH-recoil/mumu/analysis_stage1.py")
add_integration_test("examples/FCCee/flavour/Bc2TauNu/analysis_B2TauNu_truth.py")
