import os
import sys
import subprocess
import pathlib
import shutil


def build_analysis(mainparser):
    args, _ = mainparser.parse_known_args()

    if 'LOCAL_DIR' not in os.environ:
        print('----> FCCAnalyses environment not set up correctly!')
        print('      Aborting...')
        sys.exit(3)

    local_dir = os.environ.get('LOCAL_DIR')
    build_path = pathlib.Path(local_dir + '/build')
    install_path = pathlib.Path(local_dir + '/install')

    print('----> Building analysis located in:')
    print('      ' + local_dir)

    if args.clean_build:
        print('----> Clearing build and install directories...')
        if build_path.is_dir():
            shutil.rmtree(build_path)
        if install_path.is_dir():
            shutil.rmtree(install_path)

    if not build_path.is_dir():
        print('----> Creating build directory...')
        os.makedirs(build_path)

        with subprocess.Popen(['cmake', '-DCMAKE_INSTALL_PREFIX=../install', '..'],
                              cwd=local_dir+'/build',
                              stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT,
                              bufsize=1,
                              universal_newlines=True) as proc:
            for line in proc.stdout:
                print(line, end='')

    if not install_path.is_dir():
        print('----> Creating install directory...')
        os.makedirs(install_path)

    with subprocess.Popen(['make', '-j'+str(args.build_threads), 'install'],
                          cwd=local_dir+'/build',
                          stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT,
                          bufsize=1,
                          universal_newlines=True) as proc:
        for line in proc.stdout:
            print(line, end='')
