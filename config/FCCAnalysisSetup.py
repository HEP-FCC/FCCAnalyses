#__________________________________________________________
def setup(mainparser):
    from config.analysis_builder import setup_analysis

    args, _ = mainparser.parse_known_args()
    if args.command == 'setup':
        setup_analysis(name=args.name,
                       script=args.script,
                       author=args.author,
                       standalone=args.standalone)
