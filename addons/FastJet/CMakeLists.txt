find_package(FastJet REQUIRED)
message(STATUS "includes-------------------------- fastjet: ${FASTJET_INCLUDE_DIRS}")

file(GLOB sources src/*.cc)
file(GLOB headers *.h)

add_library(FastJet SHARED ${sources} ${headers})
target_link_libraries(FastJet PUBLIC ${FASTJET_LIBRARY} ${FASTJET_LIBRARY_DIRS}/libfastjetplugins.so)
target_include_directories(FastJet PUBLIC $<BUILD_INTERFACE:${CMAKE_SOURCE_DIR}/addons> ${FASTJET_INCLUDE_DIRS})
list(APPEND ADDONS_LIBRARIES FastJet)
set(ADDONS_LIBRARIES ${ADDONS_LIBRARIES} PARENT_SCOPE)
install(TARGETS FastJet
  EXPORT FCCAnalysesTargets
  RUNTIME DESTINATION "${INSTALL_BIN_DIR}" COMPONENT bin
  LIBRARY DESTINATION "${INSTALL_LIB_DIR}" COMPONENT shlib
  PUBLIC_HEADER DESTINATION "${INSTALL_INCLUDE_DIR}/FastJet"
  COMPONENT onnxruntime)
