#!/usr/bin/env python3

def find_author():
    from subprocess import getoutput
    return (getoutput('git config --global --get user.name'),
            getoutput('git config --global --get user.email'))

def replace_all(input: str, repl) -> str:
    output = input
    for a, b in repl.items():
        output = output.replace(a, b)
    return output

def setup_analysis(name: str, author: str='', description: str='', script: str='', standalone: bool=False, output_dir: str=''):
    if not author:
        author_name, author_email = find_author()
    else:
        author_list = author.split()
        if len(author) == 1:
            author_name = author
        else:
            author_name, author_email = author_list
            author_email = author_email.replace('<', '').replace('>', '')
    if not description:
        description = '[...]'
    #FIXME handle multiline descriptions
    from subprocess import getoutput
    fccanalyses_dir = getoutput('git rev-parse --show-toplevel')
    replacement_dict = {
        '__ANALYSIS_NAME__': name,
        '__ANALYSIS_DESCRIPTION__': description,
        '__SCRIPT_NAME__': script,
        '__AUTHOR_NAME__': author_name,
        '__AUTHOR_EMAIL__': author_email,
        '__FCCANALYSES_PATH__': fccanalyses_dir
    }

    import os
    if not output_dir:
        path = f'{fccanalyses_dir}/case-studies/{name}'
    else:
        path = output_dir
    for p in [path, f'{path}/src', f'{path}/include', f'{path}/scripts']:
        try:
            os.mkdir(p)
        except FileExistsError:
            print(f'Warning: FCCAnalysis space "{name}" already exists.')
            pass
    try:
        tmpl_dir = os.path.join(os.getenv('LOCAL_DIR', '.'), 'config/templates')
        with open(f'{path}/src/classes.h', 'w') as f:
            f.write(replace_all(open(f'{tmpl_dir}/classes.h', 'r').read(), replacement_dict))
        with open(f'{path}/src/classes_def.xml', 'w') as f:
            f.write(replace_all(open(f'{tmpl_dir}/classes_def.xml', 'r').read(), replacement_dict))
        with open(f'{path}/src/{script}.cc', 'w') as f:
            f.write(replace_all(open(f'{tmpl_dir}/Analysis.cc', 'r').read(), replacement_dict))
        with open(f'{path}/include/{script}.h', 'w') as f:
            f.write(replace_all(open(f'{tmpl_dir}/Analysis.h', 'r').read(), replacement_dict))
        with open(f'{path}/scripts/analysis_cfg.py', 'w') as f:
            f.write(replace_all(open(f'{tmpl_dir}/analysis_cfg.py', 'r').read(), replacement_dict))
        if standalone:
            with open(f'{path}/CMakeLists.txt', 'w') as f:
                f.write(replace_all(open(f'{tmpl_dir}/CMakeLists.txt', 'r').read(), replacement_dict))
    except OSError as error:
        print(f'FCCAnalysis space "{name}" creation error:')
        print(error)
