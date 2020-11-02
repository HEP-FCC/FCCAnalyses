
cmake_minimum_required(VERSION 2.8)




project(FCCAnalyses CXX)

find_package(ROOT COMPONENTS ROOTDataFrame)
include(${ROOT_USE_FILE})

find_package(fccedm)
find_package(EDM4HEP)


# Define basic build settings
# Use GNU-style hierarchy for installing build products
include(GNUInstallDirs)



# Offer the user the choice of overriding the installation directories
set(INSTALL_LIB_DIR lib CACHE PATH "Installation directory for libraries")
set(INSTALL_BIN_DIR bin CACHE PATH "Installation directory for executables")
set(INSTALL_INCLUDE_DIR include CACHE PATH
  "Installation directory for header files")

option(INSTALL_PYTHON "Flag for CMake to attempt to run python setup.py install" OFF)

if(INSTALL_PYTHON)
find_program(PYTHON "python")
if (PYTHON)
    set(SETUP_PY    "${CMAKE_CURRENT_SOURCE_DIR}/setup.py")
    set(OUTPUT      "${CMAKE_CURRENT_BINARY_DIR}")


    add_custom_command(OUTPUT ${OUTPUT}/timestamp
                       COMMAND ${PYTHON} ${SETUP_PY} build
                       COMMAND ${CMAKE_COMMAND} -E touch ${OUTPUT}/timestamp
                        )

    add_custom_target(target ALL DEPENDS ${OUTPUT}/timestamp)

    install(CODE "execute_process(COMMAND ${PYTHON} ${SETUP_PY} install --prefix ${CMAKE_INSTALL_PREFIX})")
endif()
endif()

add_subdirectory(analyzers/dataframe)

#add_subdirectory(FCChhAnalyses/FCChh/tth_4l/dataframe)
#add_subdirectory(FCCeeAnalyses/Z_Zqq/dataframe)
