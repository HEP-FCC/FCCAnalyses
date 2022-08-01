
if(USE_EXTERNAL_CATCH2)
  find_package(Catch2 REQUIRED)
else()
  message(STATUS "Fetching local copy of Catch2 library for unit-tests...")
  # Build Catch2 with the default flags, to avoid generating warnings when we
  # build it
  set(CXX_FLAGS_CMAKE_USED ${CMAKE_CXX_FLAGS})
  set(CMAKE_CXX_FLAGS ${CXX_FLAGS_CMAKE_DEFAULTS})
  Include(FetchContent)
  FetchContent_Declare(
    Catch2
    GIT_REPOSITORY https://github.com/catchorg/Catch2.git
    GIT_TAG        037ddbc75cc5e58b93cf5a010a94b32333ad824d
    )
  FetchContent_MakeAvailable(Catch2)
  set(CMAKE_MODULE_PATH ${Catch2_SOURCE_DIR}/extras ${CMAKE_MODULE_PATH})
  # Disable clang-tidy on external contents
  set_target_properties(Catch2 PROPERTIES CXX_CLANG_TIDY "")

  # Hack around the fact, that the include directories are not declared as
  # SYSTEM for the targets defined this way. Otherwise warnings can still occur
  # in Catch2 code when templates are evaluated (which happens quite a bit)
  get_target_property(CATCH2_IF_INC_DIRS Catch2 INTERFACE_INCLUDE_DIRECTORIES)
  set_target_properties(Catch2 PROPERTIES INTERFACE_SYSTEM_INCLUDE_DIRECTORIES "${CATCH2_IF_INC_DIRS}")

  # Reset the flags
  set(CMAKE_CXX_FLAGS ${CXX_FLAGS_CMAKE_USED})

endif()


# The unittests are a bit better and they are labelled so we can put together a
# list of labels that we want to ignore
set(filter_tests "")

set(EXTRA_TESTS)
set(EXTRA_INCLUDE_DIRS)
set(EXTRA_LIBRARIES)
if(${WITH_ONNX})
  list(APPEND EXTRA_TESTS onnxtest.cpp)
  list(APPEND EXTRA_INCLUDE_DIRS ${ONNXRUNTIME_INCLUDE_DIRS})
  list(APPEND EXTRA_LIBRARIES ${ONNXRUNTIME_LIBRARIES} nlohmann_json::nlohmann_json)
endif()

add_executable(unittest unittest.cpp myutils.cpp algorithms.cpp ${EXTRA_TESTS})
target_link_libraries(unittest PUBLIC FCCAnalyses gfortran PRIVATE Catch2::Catch2WithMain ${EXTRA_LIBRARIES})
target_include_directories(unittest PUBLIC ${VDT_INCLUDE_DIR} ${EXTRA_INCLUDE_DIRS})
target_compile_definitions(unittest PUBLIC "-DTEST_INPUT_DATA_DIR=${TEST_INPUT_DATA_DIR}")
include(Catch)
catch_discover_tests(unittest
    WORKING_DIRECTORY ${CMAKE_CURRENT_LIST_DIR}
    TEST_PREFIX "UT_" # make it possible to filter easily with -R ^UT
    TEST_SPEC ${filter_tests} # discover only tests that are known to not fail
)
