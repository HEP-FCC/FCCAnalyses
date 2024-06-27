if(WITH_ONNX STREQUAL OFF)
  return()
endif()

find_package(nlohmann_json QUIET)
find_package(ROOT COMPONENTS ROOTVecOps QUIET)
get_target_property(ONNXRUNTIME_INCLUDE_DIRS onnxruntime::onnxruntime INTERFACE_INCLUDE_DIRECTORIES)
if(nlohmann_json_FOUND)
  message(STATUS "includes-------------------------- onnxruntime: ${ONNXRUNTIME_INCLUDE_DIRS}")
elseif(WITH_ONNX STREQUAL AUTO)
  message(WARNING "nlohmann's JSON libraries not found. Skipping ONNX-dependent analyzers.")
  set(WITH_ONNX OFF)
  return()
else()
  message(FATAL_ERROR "nlohmann's JSON library!")
endif()

file(GLOB sources src/*.cc)
file(GLOB headers *.h)

fccanalyses_addon_build(ONNXRuntime
                        SOURCES ${sources} ${headers}
                        EXT_HEADERS ${ONNXRUNTIME_INCLUDE_DIRS}
                        EXT_LIBS ROOT::ROOTVecOps nlohmann_json::nlohmann_json onnxruntime::onnxruntime
                        INSTALL_COMPONENT onnxruntime)

add_custom_command(TARGET ONNXRuntime POST_BUILD
                   COMMAND ${CMAKE_COMMAND} -E copy
                   ${CMAKE_CURRENT_SOURCE_DIR}/python/*
                   ${CMAKE_CURRENT_BINARY_DIR}
)

if(BUILD_TESTING)
  find_catch_instance()
  if(Catch2_FOUND)
    # add all unit tests
    add_executable(onnxruntime-unittest test/onnxtest.cpp)
    target_link_libraries(onnxruntime-unittest PUBLIC FCCAnalyses gfortran PRIVATE Catch2::Catch2WithMain ONNXRuntime)
    target_include_directories(onnxruntime-unittest PUBLIC ${VDT_INCLUDE_DIR})
    target_compile_definitions(onnxruntime-unittest PUBLIC "-DTEST_INPUT_DATA_DIR=${TEST_INPUT_DATA_DIR}")
    include(Catch)
    catch_discover_tests(onnxruntime-unittest
      WORKING_DIRECTORY ${CMAKE_CURRENT_LIST_DIR}
      TEST_PREFIX "UT_" # make it possible to filter easily with -R ^UT
      TEST_SPEC ${filter_tests} # discover only tests that are known to not fail
    )
  endif()
  # add all integration tests
  # add_integration_test("examples/FCCee/weaver/analysis_inference.py")
endif()

file(GLOB _addon_python_files python/*.py)
install(FILES ${_addon_python_files} DESTINATION ${CMAKE_INSTALL_PREFIX}/python/addons/ONNXRuntime)
