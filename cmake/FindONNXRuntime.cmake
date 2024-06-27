find_path(ONNXRUNTIME_INCLUDE_DIR
          NAMES onnxruntime_cxx_api.h
          PATH_SUFFIXES onnxruntime/core/session
          HINTS $ENV{ONNXRUNTIME_ROOT_DIR}/include ${ONNXRUNTIME_ROOT_DIR}/include)

find_library(ONNXRUNTIME_LIBRARY NAMES onnxruntime
             HINTS $ENV{ONNXRUNTIME_ROOT_DIR}/lib ${ONNXRUNTIME_ROOT_DIR}/lib)

include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(ONNXRuntime DEFAULT_MSG ONNXRUNTIME_INCLUDE_DIR ONNXRUNTIME_LIBRARY)

mark_as_advanced(ONNXRUNTIME_FOUND ONNXRUNTIME_INCLUDE_DIR ONNXRUNTIME_LIBRARY)

set(ONNXRUNTIME_INCLUDE_DIRS ${ONNXRUNTIME_INCLUDE_DIR})
set(ONNXRUNTIME_LIBRARIES ${ONNXRUNTIME_LIBRARY})

# Rig an onnxruntime::onnxruntime target that works similar (enough) to the one
# that can be directly found via find_package(onnxruntime) for newer versions of
# onnxruntime
add_library(onnxruntime::onnxruntime INTERFACE IMPORTED GLOBAL)
set_target_properties(onnxruntime::onnxruntime
  PROPERTIES
  INTERFACE_INCLUDE_DIRECTORIES "${ONNXRUNTIME_INCLUDE_DIRS}"
  INTERFACE_LINK_LIBRARIES "${ONNXRUNTIME_LIBRARIES}"
)
