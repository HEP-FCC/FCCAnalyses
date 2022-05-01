
add_subdirectory(unittest)

add_test(NAME examples/FCCee/higgs/mH-recoil/mumu
        COMMAND python config/FCCAnalysisRun.py examples/FCCee/higgs/mH-recoil/mumu/analysis_stage1.py --test
        WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
)
