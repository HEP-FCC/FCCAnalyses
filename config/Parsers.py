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
    publicOptions.add_argument('--clean-build',
                               action='store_true',
                               default=False,
                               help='do a clean build')
    publicOptions.add_argument('--build-threads',
                               type=int,
                               default=1,
                               help='bumber of threads when building (equivalen to `make -j`)')

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
    publicOptions = parser.add_argument_group('User options')
    publicOptions.add_argument("pathToAnalysisScript", help="path to analysis script")
    publicOptions.add_argument("--files-list", help="Specify input file to bypass the processList", default=[], nargs='+')
    publicOptions.add_argument("--output", help="Specify output file name to bypass the processList and or outputList, default output.root", type=str, default="output.root")
    publicOptions.add_argument("--nevents", help="Specify max number of events to process", type=int, default=-1)
    publicOptions.add_argument("--test", action='store_true', help="Run over the test file", default=False)
    publicOptions.add_argument('--bench', action='store_true', help='Output benchmark results to a JSON file', default=False)
    publicOptions.add_argument("--ncpus", help="Set number of threads", type=int)
    #publicOptions.add_argument("--final", action='store_true', help="Run final analysis (produces final histograms and trees)", default=False)
    #publicOptions.add_argument("--plots", action='store_true', help="Run analysis plots", default=False)
    publicOptions.add_argument("--preprocess", action='store_true', help="Run preprocessing", default=False)
    publicOptions.add_argument("--validate", action='store_true', help="Validate a given production", default=False)
    publicOptions.add_argument("--rerunfailed", action='store_true', help="Rerun failed jobs", default=False)
    publicOptions.add_argument("--jobdir", help="Specify the batch job directory", type=str, default="output.root")
    publicOptions.add_argument("--eloglevel", help="Specify the RDataFrame ELogLevel", type=str, default="kUnset", choices = ['kUnset','kFatal','kError','kWarning','kInfo','kDebug'])

    internalOptions = parser.add_argument_group('\033[4m\033[1m\033[91m Internal options, NOT FOR USERS\033[0m')
    internalOptions.add_argument("--batch", action='store_true', help="Submit on batch", default=False)

def setup_run_parser_final(parser):
    publicOptions = parser.add_argument_group('User final options')
    publicOptions.add_argument("pathToAnalysisScript", help="path to analysis_final script")
    publicOptions.add_argument("--eloglevel", help="Specify the RDataFrame ELogLevel", type=str, default="kUnset", choices = ['kUnset','kFatal','kError','kWarning','kInfo','kDebug'])

def setup_run_parser_plots(parser):
    publicOptions = parser.add_argument_group('User plots options')
    publicOptions.add_argument("pathToAnalysisScript", help="path to analysis_plots script")
