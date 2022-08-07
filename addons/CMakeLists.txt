set(addons_sources CACHE STRING "List of sources for addons")
set(addons_headers CACHE STRING "List of headers for addons")
set(addons_libs CACHE STRING "List of libraries used for addons")

add_subdirectory(ONNXRuntime)

add_library(FCCAnalysesAddOns SHARED ${addons_sources} ${addons_headers})
target_include_directories(FCCAnalysesAddOns PUBLIC ${addons_headers})
target_link_libraries(FCCAnalysesAddOns PUBLIC ${addons_libs})
