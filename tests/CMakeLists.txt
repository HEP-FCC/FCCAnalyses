
add_subdirectory(unittest)

function(set_test_env _testname)
  set_property(TEST ${_testname} APPEND PROPERTY ENVIRONMENT
    LD_LIBRARY_PATH=${CMAKE_BINARY_DIR}/analyzers/dataframe:$ENV{LD_LIBRARY_PATH}
    PYTHONPATH=${CMAKE_SOURCE_DIR}:$ENV{PYTHONPATH}
    ROOT_INCLUDE_PATH=${CMAKE_SOURCE_DIR}/analyzers/dataframe:$ENV{ROOT_INCLUDE_PATH}
    )
endfunction()

add_test(NAME examples/FCCee/higgs/mH-recoil/mumu
        COMMAND python config/FCCAnalysisRun.py examples/FCCee/higgs/mH-recoil/mumu/analysis_stage1.py --test
        WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
        )
set_test_env(examples/FCCee/higgs/mH-recoil/mumu)

