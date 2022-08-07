find_catch_instance()

# The unittests are a bit better and they are labelled so we can put together a
# list of labels that we want to ignore
set(filter_tests "")

add_executable(unittest unittest.cpp myutils.cpp algorithms.cpp)
target_link_libraries(unittest PUBLIC FCCAnalyses gfortran PRIVATE Catch2::Catch2WithMain)
target_include_directories(unittest PUBLIC ${VDT_INCLUDE_DIR})
target_compile_definitions(unittest PUBLIC "-DTEST_INPUT_DATA_DIR=${TEST_INPUT_DATA_DIR}")
include(Catch)
catch_discover_tests(unittest
    WORKING_DIRECTORY ${CMAKE_CURRENT_LIST_DIR}
    TEST_PREFIX "UT_" # make it possible to filter easily with -R ^UT
    TEST_SPEC ${filter_tests} # discover only tests that are known to not fail
)
