'''
RDataFrame helpers.
'''

import os
import pathlib
import shutil
import logging
import ROOT  # type: ignore


ROOT.gROOT.SetBatch(True)

LOGGER: logging.Logger = logging.getLogger('FCCAnalyses.frame')


# _____________________________________________________________________________
def generate_graph(dframe, args, suffix: str | None = None) -> None:
    '''
    Generate computational graph of the analysis
    '''
    # Check if output file path is provided
    graph_path: pathlib.PurePath = pathlib.PurePath(args.graph_path)
    if args.graph_path == '':
        graph_path = pathlib.PurePath(args.anascript_path).with_suffix('.dot')

    # check if file path ends with "correct" extension
    if graph_path.suffix not in ('.dot', '.png'):
        LOGGER.warning('Graph output file extension not recognized!\n'
                       'Using analysis script name...')
        graph_path = pathlib.PurePath(args.anascript_path).with_suffix('.dot')

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
        LOGGER.info('Analysis computational graph will be saved into:\n - %s\n - %s',
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
