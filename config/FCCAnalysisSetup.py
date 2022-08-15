#__________________________________________________________
def setup(mainparser):
    from config.analysis_builder import setup_analysis

    args, _ = mainparser.parse_known_args()
    if args.command == 'init':
        setup_analysis(name=args.name,
                       script=args.script,
                       author=args.author,
                       description=args.description,
                       standalone=args.standalone,
                       output_dir=args.output_dir)
