
cmake_minimum_required(VERSION 2.8)


project(FCCAnalyses)

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
