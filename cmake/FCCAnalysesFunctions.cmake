macro(find_catch_instance)
  if(USE_EXTERNAL_CATCH2)
    find_package(Catch2 REQUIRED)
  else()
    message(STATUS "Fetching local copy of Catch2 library for unit-tests...")
    # Build Catch2 with the default flags, to avoid generating warnings when we
    # build it
    set(CXX_FLAGS_CMAKE_USED ${CMAKE_CXX_FLAGS})
    set(CMAKE_CXX_FLAGS ${CXX_FLAGS_CMAKE_DEFAULTS})
    include(FetchContent)
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
endmacro()

function(add_integration_test _testname)

  add_test(NAME ${_testname}
          COMMAND python config/FCCAnalysisRun.py ${_testname} --test --nevents 100 --bench
          WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
          )
  set_property(TEST ${_testname} APPEND PROPERTY ENVIRONMENT
    LD_LIBRARY_PATH=${CMAKE_BINARY_DIR}/analyzers/dataframe:$ENV{LD_LIBRARY_PATH}
    PYTHONPATH=${CMAKE_SOURCE_DIR}:$ENV{PYTHONPATH}
    ROOT_INCLUDE_PATH=${CMAKE_SOURCE_DIR}/analyzers/dataframe:$ENV{ROOT_INCLUDE_PATH}
    TEST_INPUT_DATA_DIR=${TEST_INPUT_DATA_DIR}
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
    TEST_INPUT_DATA_DIR=${TEST_INPUT_DATA_DIR}
    )
endfunction()
