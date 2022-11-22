#__________________________________________________________
def setup(mainparser):
    from config.analysis_builder import setup_analysis

    args, _ = mainparser.parse_known_args()
    if args.command == 'init':
        setup_analysis(package=args.package,
                       name=args.name,
                       author=args.author,
                       description=args.description,
                       standalone=args.standalone,
                       output_dir=args.output_dir)
