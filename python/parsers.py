'''
Parsers for the fccanalysis sub-commands
'''

import argparse


def setup_init_parser(parser):
    '''
    Arguments for the init sub-command
    '''
    init_args = parser.add_argument_group('Init arguments')

    init_args.add_argument('package',
                           help='name of the analysis package to be built')
    init_args.add_argument('--name',
                           default='DummyAnalysis',
                           help='name of the main analysis utility')
    init_args.add_argument(
        '--author',
        help="author's \"name <email@address>\" (will use git-config if not "
             "specified)")
    init_args.add_argument('--description',
                           help='analysis package description')
    init_args.add_argument(
        '--standalone',
        action='store_true',
        default=False,
        help='also add CMake directive to build standalone package')
    init_args.add_argument(
        '--output-dir',
        help='output directory where the analysis package will be written')


def setup_build_parser(parser):
    '''
    Arguments for the build sub-command
    '''
    build_args = parser.add_argument_group('Build arguments')
    build_args.add_argument('-c', '--clean-build',
                            action='store_true',
                            default=False,
                            help='do a clean build')
    build_args.add_argument(
        '-j', '--build-threads',
        type=int,
        default=1,
        help='number of threads when building (equivalent to `make -j`)'
    )
    build_args.add_argument('--acts-on',
                            action='store_true',
                            default=False,
                            help='enable ACTS based analyzers')


def setup_test_parser(parser):
    '''
    Arguments for the test sub-command
    '''
    test_args = parser.add_argument_group('Test arguments')
    test_args.add_argument(
        '-R', '--tests-regex',
        type=str,
        help='Run tests matching regular expression (e.g. run only unit tests '
             'with "^UT")'
    )
    test_args.add_argument(
        '-E', '--exclude-regex',
        type=str,
        help='Exclude tests matching regular expression'
    )
    test_args.add_argument(
        '-j', '--parallel',
        type=int,
        default=-1,
        help='number of tests running in parallel (equivalent to `ctest -j`)'
    )


def setup_pin_parser(parser):
    '''
    Arguments for the pin sub-command
    '''
    pin_args = parser.add_argument_group('Pin arguments')
    pin_args.add_argument('-c', '--clear',
                          action='store_true',
                          default=False,
                          help='clear analysis pin')
    pin_args.add_argument('-f', '--force',
                          action='store_true',
                          default=False,
                          help='force recreate analysis pin')
    pin_args.add_argument('-s', '--show',
                          action='store_true',
                          default=False,
                          help='show pinned stack')


def setup_run_parser(parser):
    '''
    Define command line arguments for the run sub-command.
    '''
    parser.add_argument('anascript_path',
                        help='path to analysis script')
    parser.add_argument('--files-list', default=[], nargs='+',
                        help='specify input file(s) to bypass the processList')
    parser.add_argument(
        '--output',
        type=str,
        default='output.root',
        help='specify output file name to bypass the processList and or '
             'outputList')
    parser.add_argument('--nevents', type=int, default=-1,
                        help='specify max number of events to process')
    parser.add_argument('--test', action='store_true', default=False,
                        help='run over the test input file')
    parser.add_argument('--bench', action='store_true', default=False,
                        help='output benchmark results to a JSON file')
    parser.add_argument('-j', '--ncpus', type=int, default=-1,
                        help='set number of threads')
    parser.add_argument('-g', '--graph', action='store_true', default=False,
                        help='generate computational graph of the analysis')
    parser.add_argument('--graph-path', type=str, default='',
                        help='analysis graph save path, should end with '
                        '\'.dot\' or \'.png\'')

    # Internal argument, not to be used by the users
    parser.add_argument('--batch', action='store_true', default=False,
                        help=argparse.SUPPRESS)


def setup_run_parser_final(parser):
    '''
    Define command line arguments for the final sub-command.
    '''
    parser.add_argument('anascript_path',
                        help='path to analysis_final script')
    parser.add_argument('-g', '--graph', action='store_true', default=False,
                        help='generate computational graph of the analysis')
    parser.add_argument('--graph-path', type=str, default='',
                        help='analysis graph save path, should end with '
                        '\'.dot\' or \'.png\'')


def setup_run_parser_plots(parser):
    '''
    Define command line arguments for the plots sub-command.
    '''
    parser.add_argument('script_path', help="path to the plots script")
    parser.add_argument('--legend-text-size', type=float, default=None,
                        help='text size for the legend elements')
    parser.add_argument('--legend-x-min', type=float, default=None,
                        help='minimal x position of the legend')
    parser.add_argument('--legend-x-max', type=float, default=None,
                        help='maximal x position of the legend')
    parser.add_argument('--legend-y-min', type=float, default=None,
                        help='minimal y position of the legend')
    parser.add_argument('--legend-y-max', type=float, default=None,
                        help='maximal y position of the legend')



def setup_run_parser_combine(parser):
    '''
    Define command line arguments for the combine sub-command.
    '''
    parser.add_argument('script_path', help="path to the combine script")


# _____________________________________________________________________________
def setup_subparsers(subparsers):
    '''
    Sets all sub-parsers for all sub-commands
    '''

    # Create sub-parsers
    parser_init = subparsers.add_parser(
        'init',
        help="generate a RDataFrame based FCC analysis")
    parser_build = subparsers.add_parser(
        'build',
        help='build and install local analysis')
    parser_test = subparsers.add_parser(
        'test',
        help='test whole or a part of the analysis framework')
    parser_pin = subparsers.add_parser(
        'pin',
        help='pin fccanalyses to the current version of Key4hep stack')
    parser_run = subparsers.add_parser(
        'run',
        help="run a RDataFrame based FCC analysis")
    parser_run_final = subparsers.add_parser(
        'final',
        help="run a RDataFrame based FCC analysis final configuration")
    parser_run_plots = subparsers.add_parser(
        'plots',
        help="run a RDataFrame based FCC analysis plot configuration")
    parser_run_combine = subparsers.add_parser(
        'combine',
        help="prepare combine cards to run basic template fits")

    # Register sub-parsers
    setup_init_parser(parser_init)
    setup_build_parser(parser_build)
    setup_test_parser(parser_test)
    setup_pin_parser(parser_pin)
    setup_run_parser(parser_run)
    setup_run_parser_final(parser_run_final)
    setup_run_parser_plots(parser_run_plots)
    setup_run_parser_combine(parser_run_combine)
