#!/usr/bin/env python3

def find_author():
    from subprocess import getoutput
    return getoutput('git config --global --get user.name') + ' <' + getoutput('git config --global --get user.email') + '>'

def replace_all(input: str, repl) -> str:
    output = input
    for a, b in repl.items():
        output = output.replace(a, b)
    return output

def setup_analysis(package: str, author: str='', description: str='', name: str='', standalone: bool=False, output_dir: str=''):
    if not author:
        author = find_author()
    if not description:
        description = '[...]'
    #FIXME handle multiline descriptions
    from subprocess import getoutput
    fccanalyses_dir = getoutput('git rev-parse --show-toplevel')
    replacement_dict = {
        '__pkgname__': package,
        '__pkgdesc__': description,
        '__name__': name,
        '__author__': author,
        '__fccpath__': fccanalyses_dir
    }

    if not output_dir:
        path = f'{fccanalyses_dir}/case-studies/{package}'
    else:
        path = output_dir

    import os
    for p in [path, f'{path}/src', f'{path}/include', f'{path}/scripts']:
        try:
            os.mkdir(p)
        except FileExistsError:
            print(f'Warning: FCCAnalysis package "{package}" already exists.')
            pass
    try:
        tmpl_dir = os.path.join(fccanalyses_dir, 'config/templates')
        with open(f'{path}/src/classes.h', 'w') as f:
            f.write(replace_all(open(f'{tmpl_dir}/classes.h', 'r').read(), replacement_dict))
        with open(f'{path}/src/classes_def.xml', 'w') as f:
            f.write(replace_all(open(f'{tmpl_dir}/classes_def.xml', 'r').read(), replacement_dict))
        with open(f'{path}/src/{name}.cc', 'w') as f:
            f.write(replace_all(open(f'{tmpl_dir}/Analysis.cc', 'r').read(), replacement_dict))
        with open(f'{path}/include/{name}.h', 'w') as f:
            f.write(replace_all(open(f'{tmpl_dir}/Analysis.h', 'r').read(), replacement_dict))
        with open(f'{path}/scripts/analysis_cfg.py', 'w') as f:
            f.write(replace_all(open(f'{tmpl_dir}/analysis_cfg.py', 'r').read(), replacement_dict))
        if standalone:
            with open(f'{path}/CMakeLists.txt', 'w') as f:
                f.write(replace_all(open(f'{tmpl_dir}/CMakeLists.txt', 'r').read(), replacement_dict))
    except OSError as error:
        print(f'FCCAnalysis package "{package}" creation error:')
        print(error)
