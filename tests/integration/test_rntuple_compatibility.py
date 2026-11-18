"""Exercise input event counting and output formats with matched EDM4hep files."""

import argparse
import pathlib
import subprocess
import sys
import tempfile

import numpy as np
import ROOT
from sample import get_event_entries


COLUMNS = ('n_reconstructed', 'n_muons', 'muon_momentum',
           'n_jets', 'jet_momentum')
ANALYSIS = pathlib.Path(__file__).with_name('rntuple_compatibility_analysis.py')


def check_events(path, expected_format):
    with ROOT.TFile.Open(str(path)) as root_file:
        key = root_file.GetKey('events')
        assert key, f'{path}: missing events'
        actual_format = 'rntuple' if 'RNTuple' in key.GetClassName() else 'ttree'
        assert actual_format == expected_format, (path, actual_format, expected_format)
        events = root_file.Get('events')
        entries = (ROOT.RNTupleReader.Open(events).GetNEntries()
                   if actual_format == 'rntuple' else events.GetEntries())
        assert entries == 1000, (path, entries)
        assert get_event_entries(root_file) == entries, path


def read_output(path, expected_format):
    check_events(path, expected_format)
    return ROOT.RDataFrame('events', str(path)).AsNumpy(list(COLUMNS))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ttree', required=True)
    parser.add_argument('--rntuple', required=True)
    parser.add_argument('--fccanalysis', required=True)
    args = parser.parse_args()

    if (not hasattr(ROOT, 'RNTupleReader') or
            not hasattr(ROOT.RDF, 'ESnapshotOutputFormat')):
        print('Skipping: ROOT lacks the RNTuple reader or snapshot output format')
        return 77

    check_events(args.ttree, 'ttree')
    check_events(args.rntuple, 'rntuple')

    with tempfile.TemporaryDirectory(prefix='fcc-rntuple-test-') as tmp:
        outputs = []
        for input_format, input_path in (('ttree', args.ttree),
                                         ('rntuple', args.rntuple)):
            output = pathlib.Path(tmp) / f'{input_format}.root'
            command = [args.fccanalysis, 'run', str(ANALYSIS), '-i', input_path,
                       '-o', str(output), '-j', '1', '--no-progress-bar']
            subprocess.run(command, check=True)
            outputs.append(read_output(output, input_format))

        reference = outputs[0]
        for values in outputs[1:]:
            for column in COLUMNS:
                for expected, actual in zip(reference[column], values[column]):
                    np.testing.assert_array_equal(actual, expected, err_msg=column)

    return 0


if __name__ == '__main__':
    sys.exit(main())
