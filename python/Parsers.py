import argparse

def setup_init_parser(parser):
    publicOptions = parser.add_argument_group('User options')
    publicOptions.add_argument('package', help='name of the analysis package to be built')
    publicOptions.add_argument('--name', help='name of the main analysis utility', default='DummyAnalysis')
    publicOptions.add_argument('--author', help="author's \"name <email@address>\" (will use git-config if not specified)")
    publicOptions.add_argument('--description', help='analysis package description')
    publicOptions.add_argument('--standalone', action='store_true', help="also add CMake directive to build standalone package", default=False)
    publicOptions.add_argument('--output-dir', help='output directory where the analysis package will be written')

def setup_build_parser(parser):
    publicOptions = parser.add_argument_group('User build options')
    publicOptions.add_argument('-c', '--clean-build',
                               action='store_true',
                               default=False,
                               help='do a clean build')
    publicOptions.add_argument(
        '-j', '--build-threads',
        type=int,
        default=1,
        help='number of threads when building (equivalent to `make -j`)'
    )


def setup_test_parser(parser):
    '''
    Adds test options
    '''
    test_args = parser.add_argument_group('Test options')
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
    publicOptions = parser.add_argument_group('User pin options')
    publicOptions.add_argument('-c', '--clear',
                               action='store_true',
                               default=False,
                               help='clear analysis pin')
    publicOptions.add_argument('-f', '--force',
                               action='store_true',
                               default=False,
                               help='force recreate analysis pin')
    publicOptions.add_argument('-s', '--show',
                               action='store_true',
                               default=False,
                               help='show pinned stack')


def setup_run_parser(parser):
    '''
    Define command line arguments for the run subcommand.
    '''
    parser.add_argument('anafile_path',
                        help='path to analysis file')
    parser.add_argument('--files-list', default=[], nargs='+',
                        help='specify input file to bypass the processList')
    parser.add_argument('--output', type=str, default='output.root',
                        help='specify output file name to bypass the processList and or outputList')
    parser.add_argument('--nevents', type=int, default=-1,
                        help='specify max number of events to process')
    parser.add_argument('--test', action='store_true', default=False,
                        help='run over the test file')
    parser.add_argument('--bench', action='store_true', default=False,
                        help='output benchmark results to a JSON file')
    parser.add_argument('--ncpus', type=int, default=-1,
                        help='set number of threads')
    parser.add_argument('--final', action='store_true', default=False,
                        help='run final analysis (produces final histograms and trees)')
    parser.add_argument('--plots', action='store_true', default=False,
                        help='run analysis plots')
    parser.add_argument('--preprocess', action='store_true', default=False,
                        help='run preprocessing')
    parser.add_argument('--validate', action='store_true', default=False,
                        help='validate a given production')
    parser.add_argument('--rerunfailed', action='store_true', default=False,
                        help='rerun failed jobs')
    parser.add_argument('--jobdir', type=str, default='output.root',
                        help='specify the batch job directory')

    # Internal argument, not to be used by the users
    parser.add_argument('--batch', action='store_true', default=False,
                        help=argparse.SUPPRESS)


def setup_run_parser_final(parser):
    '''
    Define command line arguments for the final subcommand.
    '''
    parser.add_argument('anafile_path',
                        help='path to analysis_final script')


def setup_run_parser_plots(parser):
    '''
    Define command line arguments for the plots subcommand.
    '''
    parser.add_argument('anafile_path', help="path to analysis_plots script")
