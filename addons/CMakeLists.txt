add_subdirectory(FastJet)
add_subdirectory(ONNXRuntime)

set(ADDONS_LIBRARIES ${ADDONS_LIBRARIES} PARENT_SCOPE)
message(STATUS "add-ons--------------------------- ${ADDONS_LIBRARIES}")
