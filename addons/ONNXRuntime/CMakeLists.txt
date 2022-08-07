
if(WITH_ONNX STREQUAL OFF)
  return()
endif()
find_package(ONNXRuntime)
find_package(nlohmann_json)
find_package(ROOT COMPONENTS ROOTVecOps)
if(ONNXRuntime_FOUND AND nlohmann_json_FOUND)
  message(STATUS "includes-------------------------- onnxruntime: ${ONNXRUNTIME_INCLUDE_DIRS}")
elseif(WITH_ONNX STREQUAL AUTO)
  message(WARNING "ONNXRuntime and/or nlohmann's JSON libraries not found. Skipping ONNX-dependent analyzers.")
  set(WITH_ONNX OFF)
else()
  message(FATAL_ERROR "Failed to locate ONNXRuntime and/or nlohmann's JSON library!")
endif()

file(GLOB sources src/*.cc)
file(GLOB headers *.h)

add_library(ONNXRuntime SHARED ${sources} ${headers})
target_link_libraries(ONNXRuntime PUBLIC ROOT::ROOTVecOps ${ONNXRUNTIME_LIBRARIES} nlohmann_json::nlohmann_json)
target_include_directories(ONNXRuntime PUBLIC $<BUILD_INTERFACE:${CMAKE_SOURCE_DIR}/addons> ${ONNXRUNTIME_INCLUDE_DIRS})
list(APPEND ADDONS_LIBRARIES ONNXRuntime)
set(ADDONS_LIBRARIES ${ADDONS_LIBRARIES} PARENT_SCOPE)
install(TARGETS ONNXRuntime
  EXPORT FCCAnalysesTargets
  RUNTIME DESTINATION "${INSTALL_BIN_DIR}" COMPONENT bin
  LIBRARY DESTINATION "${INSTALL_LIB_DIR}" COMPONENT shlib
  PUBLIC_HEADER DESTINATION "${INSTALL_INCLUDE_DIR}/ONNXRuntime"
  COMPONENT onnxruntime)

# add all unit tests
if(FALSE)
add_executable(unittest test/onnxtest.cpp)
target_link_libraries(unittest PUBLIC FCCAnalyses gfortran PRIVATE Catch2::Catch2WithMain ${ONNXRUNTIME_LIBRARIES} nlohmann_json::nlohmann_json)
target_include_directories(unittest PUBLIC ${VDT_INCLUDE_DIR} ${ONNXRUNTIME_INCLUDE_DIRS})
target_compile_definitions(unittest PUBLIC "-DTEST_INPUT_DATA_DIR=${TEST_INPUT_DATA_DIR}")
include(Catch)
catch_discover_tests(unittest
    WORKING_DIRECTORY ${CMAKE_CURRENT_LIST_DIR}
    TEST_PREFIX "UT_" # make it possible to filter easily with -R ^UT
    TEST_SPEC ${filter_tests} # discover only tests that are known to not fail
)

# add all integration tests
add_integration_test("examples/FCCee/test/weaver_inference.py")
endif()
