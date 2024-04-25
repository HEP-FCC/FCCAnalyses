add_subdirectory(FastJet)
add_subdirectory(ONNXRuntime)
add_subdirectory(TMVAHelper)

set(ADDONS_LIBRARIES ${ADDONS_LIBRARIES} PARENT_SCOPE)
message(STATUS "add-ons--------------------------- ${ADDONS_LIBRARIES}")
