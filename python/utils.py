'''
RDataFrame or other helpers.
'''

import os
import pathlib
import shutil
import logging
import string
import random
import json
import ROOT  # type: ignore


ROOT.gROOT.SetBatch(True)

LOGGER: logging.Logger = logging.getLogger('FCCAnalyses.utils')


# _____________________________________________________________________________
def generate_graph(dframe, args, suffix: str | None = None) -> None:
    '''
    Generate computational graph of the analysis
    '''
    # Check if output file path is provided
    graph_path: pathlib.PurePath = pathlib.PurePath(args.graph_path)
    if args.graph_path == '':
        graph_path = pathlib.PurePath(os.getcwd(), 'fccanalysis_graph.dot')

    # check if file path ends with "correct" extension
    if graph_path.suffix not in ('.dot', '.png'):
        LOGGER.warning('Graph output file extension not recognized!\n'
                       'Using analysis script name...')
        graph_path = pathlib.PurePath(os.getcwd(), 'fccanalysis_graph.dot')

    # Add optional suffix to the output file path
    if suffix is not None:
        graph_path = graph_path.with_name(graph_path.stem +
                                          suffix +
                                          graph_path.suffix)  # extension

    # Announce to which files graph will be saved
    if shutil.which('dot') is None:
        LOGGER.info('Analysis computational graph will be saved into:\n - %s',
                    graph_path.with_suffix('.dot'))
    else:
        LOGGER.info('Analysis computational graph will be saved '
                    'into:\n - %s\n - %s',
                    graph_path.with_suffix('.dot'),
                    graph_path.with_suffix('.png'))

    # Generate graph in .dot format
    ROOT.RDF.SaveGraph(dframe, str(graph_path.with_suffix('.dot')))

    if shutil.which('dot') is None:
        LOGGER.warning('PNG version of the computational graph will not be '
                       'generated.\nGraphviz library not found!')
        return

    # Convert .dot file into .png
    os.system(f'dot -Tpng {graph_path.with_suffix(".dot")} '
              f'-o {graph_path.with_suffix(".png")}')


# _____________________________________________________________________________
def save_benchmark(outfile, benchmark):
    '''
    Save benchmark results to a JSON file.
    '''
    benchmarks = []
    try:
        with open(outfile, 'r', encoding='utf-8') as benchin:
            benchmarks = json.load(benchin)
    except OSError:
        pass
    except json.decoder.JSONDecodeError:
        pass

    benchmarks = [b for b in benchmarks if b['name'] != benchmark['name']]
    benchmarks.append(benchmark)

    with open(outfile, 'w', encoding='utf-8') as benchout:
        json.dump(benchmarks, benchout, indent=2)


# _____________________________________________________________________________
def random_string(length: int = 8):
    '''
    Generate random string of specified length.
    '''
    return ''.join(random.choices(string.ascii_letters + string.digits,
                                  k=length))
