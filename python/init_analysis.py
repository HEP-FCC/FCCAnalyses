'''
Initialize local analysis
'''

import logging
import os
import sys
from subprocess import getoutput


LOGGER = logging.getLogger('FCCAnalyses.init_analysis')


def find_author():
    '''
    Retrieve the author of the package from the git confioguration
    '''
    return getoutput('git config --global --get user.name') + \
        ' <' + getoutput('git config --global --get user.email') + '>'


def replace_all(_input: str, repl: dict) -> str:
    '''
    Replace all elements of repl in the provided string.
    '''
    output = _input
    for a, b in repl.items():
        output = output.replace(a, b)
    return output


def create_file(dest_path: str,
                template_path: str,
                replacements: dict) -> bool:
    '''
    Create file from a template.
    TODO: exceptions
    '''
    with open(template_path, 'r', encoding='utf-8') as template_file:
        template: str = template_file.read()

    with open(dest_path, 'w', encoding='utf-8') as dest_file:
        dest_file.write(replace_all(template, replacements))

    return True


def setup_analysis(package: str,
                   author: str = '',
                   description: str = '',
                   name: str = '',
                   standalone: bool = False,
                   output_dir: str = ''):
    '''
    Generates the analysis package.
    '''
    if not author:
        author = find_author()
    if not description:
        description = '[...]'
    elif '\n' in description:
        raise RuntimeError('Multiline description is not supported. Please '
                           'edit the output analysis header file directly.')
    fccanalyses_path = getoutput('git rev-parse --show-toplevel')
    replacement_dict = {
        '__pkgname__': package,
        '__pkgdesc__': description,
        '__name__': name,
        '__author__': author,
        '__fccpath__': fccanalyses_path
    }

    if not output_dir:
        path = f'{fccanalyses_path}/case-studies/{package}'
    else:
        path = output_dir

    for p in [path, f'{path}/src', f'{path}/include', f'{path}/scripts']:
        try:
            os.mkdir(p)
        except FileExistsError:
            LOGGER.warning('FCCAnalysis package "%s" already exists.', package)
    try:
        tmpl_dir = os.path.join(fccanalyses_path, 'templates')
        create_file(f'{path}/src/classes.h', f'{tmpl_dir}/classes.h',
                    replacement_dict)
        create_file(f'{path}/src/classes_def.xml',
                    f'{tmpl_dir}/classes_def.xml',
                    replacement_dict)
        create_file(f'{path}/src/{name}.cc', f'{tmpl_dir}/Package.cc',
                    replacement_dict)
        create_file(f'{path}/include/{name}.h', f'{tmpl_dir}/Package.h',
                    replacement_dict)
        create_file(f'{path}/scripts/analysis_cfg.py',
                    f'{tmpl_dir}/analysis_cfg.py',
                    replacement_dict)
        if standalone:
            create_file(f'{path}/CMakeLists.txt', f'{tmpl_dir}/CMakeLists.txt',
                        replacement_dict)
    except OSError as error:
        LOGGER.error('FCCAnalysis package "%s" creation error:\n%s',
                     package, error)
        sys.exit(3)


def init_analysis(mainparser):
    '''
    Initialize analysis package
    '''

    args, _ = mainparser.parse_known_args()

    if args.command != 'init':
        LOGGER.error('Wrong sub-command!\nAborting...')

    setup_analysis(package=args.package,
                   name=args.name,
                   author=args.author,
                   description=args.description,
                   standalone=args.standalone,
                   output_dir=args.output_dir)
