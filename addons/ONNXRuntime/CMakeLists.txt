if(WITH_ONNX STREQUAL OFF)
  return()
endif()

find_package(ONNXRuntime QUIET)
find_package(nlohmann_json QUIET)
find_package(ROOT COMPONENTS ROOTVecOps QUIET)
if(ONNXRuntime_FOUND AND nlohmann_json_FOUND)
  message(STATUS "includes-------------------------- onnxruntime: ${ONNXRUNTIME_INCLUDE_DIRS}")
elseif(WITH_ONNX STREQUAL AUTO)
  message(WARNING "ONNXRuntime and/or nlohmann's JSON libraries not found. Skipping ONNX-dependent analyzers.")
  set(WITH_ONNX OFF)
  return()
else()
  message(FATAL_ERROR "Failed to locate ONNXRuntime and/or nlohmann's JSON library!")
endif()

file(GLOB sources src/*.cc)
file(GLOB headers *.h)

fccanalyses_addon_build(ONNXRuntime
                        SOURCES ${sources} ${headers}
                        EXT_HEADERS ${ONNXRUNTIME_INCLUDE_DIRS}
                        EXT_LIBS ROOT::ROOTVecOps ${ONNXRUNTIME_LIBRARIES} nlohmann_json::nlohmann_json
                        INSTALL_COMPONENT onnxruntime)

if(BUILD_TESTING)
  find_catch_instance()
  if(Catch2_FOUND)
    # add all unit tests
    add_executable(onnxruntime-unittest test/onnxtest.cpp)
    target_link_libraries(onnxruntime-unittest PUBLIC FCCAnalyses gfortran PRIVATE Catch2::Catch2WithMain ONNXRuntime)
    target_include_directories(onnxruntime-unittest PUBLIC ${VDT_INCLUDE_DIR} ${ONNXRUNTIME_INCLUDE_DIRS})
    target_compile_definitions(onnxruntime-unittest PUBLIC "-DTEST_INPUT_DATA_DIR=${TEST_INPUT_DATA_DIR}")
    include(Catch)
    catch_discover_tests(onnxruntime-unittest
      WORKING_DIRECTORY ${CMAKE_CURRENT_LIST_DIR}
      TEST_PREFIX "UT_" # make it possible to filter easily with -R ^UT
      TEST_SPEC ${filter_tests} # discover only tests that are known to not fail
    )
  endif()
  # add all integration tests
  add_integration_test("examples/FCCee/weaver/analysis_inference.py")
endif()
