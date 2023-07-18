'''
The module runs tests of FCCAnalyses
'''

import os
import sys
import subprocess


def run_subprocess(command, run_dir):
    '''
    Run subprocess in specified directory.
    Check only the return value, otherwise keep the subprocess connected to
    stdin/stout/stderr.
    '''
    try:
        with subprocess.Popen(command, cwd=run_dir) as proc:
            status = proc.wait()

            if status != 0:
                print('----> Error: One of the tests failed!')
                sys.exit(int(status))

    except FileNotFoundError:
        print('----> \"ctest\" not found!')
        sys.exit(3)
    except KeyboardInterrupt:
        print('----> Aborting...')
        sys.exit(0)


def test_fccanalyses(mainparser):
    '''
    Test FCCAnalyses framework
    '''

    if 'LOCAL_DIR' not in os.environ:
        print('----> Error: FCCAnalyses environment not set up correctly!')
        print('      Aborting...')
        sys.exit(3)

    local_dir = os.environ.get('LOCAL_DIR')

    args, _ = mainparser.parse_known_args()

    ctest_command = ['ctest', '--output-on-failure']

    if args.tests_regex:
        ctest_command.append('-R')
        ctest_command.append(args.tests_regex)

    if args.exclude_regex:
        ctest_command.append('-E')
        ctest_command.append(args.exclude_regex)

    run_subprocess(ctest_command, local_dir + '/build')

    print(args)
