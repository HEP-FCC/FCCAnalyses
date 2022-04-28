
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

add_executable(unittest unittest.cpp)
target_link_libraries(unittest PUBLIC FCCAnalyses gfortran PRIVATE Catch2::Catch2WithMain)
target_include_directories(unittest PUBLIC ${VDT_INCLUDE_DIR})
  include(Catch)
  catch_discover_tests(unittest
      WORKING_DIRECTORY ${CMAKE_CURRENT_LIST_DIR}
      TEST_PREFIX "UT_" # make it possible to filter easily with -R ^UT
      TEST_SPEC ${filter_tests} # discover only tests that are known to not fail
  )

add_executable(unittest_myutils myutils.cpp)
target_link_libraries(unittest_myutils PUBLIC FCCAnalyses gfortran PRIVATE Catch2::Catch2WithMain)
target_include_directories(unittest_myutils PUBLIC ${VDT_INCLUDE_DIR})
  include(Catch)
  catch_discover_tests(unittest_myutils
      WORKING_DIRECTORY ${CMAKE_CURRENT_LIST_DIR}
      TEST_PREFIX "UT_" # make it possible to filter easily with -R ^UT
      TEST_SPEC ${filter_tests} # discover only tests that are known to not fail
  )

add_executable(unittest_algorithms algorithms.cpp)
target_link_libraries(unittest_algorithms PUBLIC FCCAnalyses gfortran PRIVATE Catch2::Catch2WithMain)
target_include_directories(unittest_algorithms PUBLIC ${VDT_INCLUDE_DIR})
  include(Catch)
  catch_discover_tests(unittest_algorithms
      WORKING_DIRECTORY ${CMAKE_CURRENT_LIST_DIR}
      TEST_PREFIX "UT_" # make it possible to filter easily with -R ^UT
      TEST_SPEC ${filter_tests} # discover only tests that are known to not fail
  )
