'''
The module takes care of building FCCAnalyses
'''

import os
import sys
import subprocess
import pathlib
import shutil
import logging


LOGGER = logging.getLogger('FCCAnalyses.build')


def run_subprocess(command: str, run_dir: str) -> None:
    '''
    Run sub-process in specified directory.
    Check only the return value, otherwise keep the sub-process connected to
    stdin/stout/stderr.
    '''
    try:
        with subprocess.Popen(command, cwd=run_dir) as proc:
            status: int = proc.wait()

            if status != 0:
                LOGGER.error('Error encountered!\n'
                             'In case `fccanalysis` command is broken, you '
                             'can try recovering with:\n'
                             '  hash -d fccanalysis\n'
                             'Aborting...')
                sys.exit(3)

    except KeyboardInterrupt:
        LOGGER.error('Aborting...')
        sys.exit(0)


def build_analysis(mainparser) -> None:
    '''
    Main build steering function
    '''
    args = mainparser.parse_args()

    if 'FCCANA_LOCAL_DIR' not in os.environ:
        LOGGER.error('Local FCCAnalyses environment not set up correctly!\n'
                     'Building of the FCCAnalyses is available only '
                     'for the local copy of the FCCAnalyses.\n'
                     'Aborting...')
        sys.exit(3)

    local_dir = os.environ.get('FCCANA_LOCAL_DIR')
    build_path = pathlib.Path(local_dir + '/build')
    install_path = pathlib.Path(local_dir + '/install')
    cmake_args: list[str] = ['-DCMAKE_INSTALL_PREFIX=../install',
                             '-DCMAKE_EXPORT_COMPILE_COMMANDS=ON']

    LOGGER.info('Building analysis located in:\n%s', local_dir)

    if args.acts_on:
        LOGGER.info('Building also ACTS based analyzers...')
        cmake_args += ['-DWITH_ACTS=ON']

    if args.no_source:
        cmake_args += ['-DWITH_PODIO_DATASOURCE=OFF']

    if args.clean_build:
        LOGGER.info('Clearing build and install directories...')
        if build_path.is_dir():
            shutil.rmtree(build_path)
        if install_path.is_dir():
            shutil.rmtree(install_path)

    if not build_path.is_dir():
        LOGGER.info('Creating build directory...')
        os.makedirs(build_path)

        run_subprocess(['cmake'] + cmake_args + ['..'],
                       local_dir + '/build')

    if not install_path.is_dir():
        LOGGER.info('Creating install directory...')
        os.makedirs(install_path)

    run_subprocess(['make', f'-j{args.build_threads}', 'install'],
                   local_dir + '/build')

    build_stack_path = pathlib.Path(local_dir + '/.fccana/stack_build')
    stack_path = os.environ.get('KEY4HEP_STACK')

    LOGGER.debug('Saving information about the Key4hep stack used in the '
                 'build:\n  - %s', stack_path)

    os.makedirs(os.path.dirname(build_stack_path), exist_ok=True)

    with open(build_stack_path, 'w', encoding='utf-8') as buildstackfile:
        buildstackfile.write(stack_path + '\n')
