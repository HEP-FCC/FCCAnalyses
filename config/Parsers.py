def setup_run_parser(parser):
    publicOptions = parser.add_argument_group('User options')
    publicOptions.add_argument("pathToAnalysisScript", help="path to analysis script")
    publicOptions.add_argument("--files-list", help="Specify input file to bypass the processList", default=[], nargs='+')
    publicOptions.add_argument("--output", help="Specify output file name to bypass the processList and or outputList, default output.root", type=str, default="output.root")
    publicOptions.add_argument("--nevents", help="Specify max number of events to process", type=int, default=-1)
    publicOptions.add_argument("--test", action='store_true', help="Run over the test file", default=False)
    publicOptions.add_argument('--bench', action='store_true', help='Output benchmark results to a JSON file', default=False)
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
