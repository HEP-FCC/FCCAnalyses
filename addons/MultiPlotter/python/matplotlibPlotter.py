'''matplotlib-based plotting utility, with a ROOT-like drawing style'''

import itertools
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import to_rgba
from matplotlib.legend import Legend
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.transforms import Bbox, BboxTransformTo

import ROOT
from ROOT import mplt

ROOT_STYLE = {
    'font.family': 'sans-serif',
    'font.sans-serif': ['Nimbus Sans', 'Helvetica', 'Arial', 'DejaVu Sans'],
    'font.size': 15,
    'mathtext.default': 'regular',
    'axes.linewidth': 1.,
    'axes.labelsize': 15,
    'xaxis.labellocation': 'right',
    'yaxis.labellocation': 'top',
    'xtick.direction': 'in',
    'ytick.direction': 'in',
    'xtick.top': True,
    'ytick.right': True,
    'xtick.minor.visible': True,
    'ytick.minor.visible': True,
    'xtick.major.size': 10,
    'ytick.major.size': 10,
    'xtick.minor.size': 5,
    'ytick.minor.size': 5,
    'legend.frameon': False,
    'legend.handlelength': 1.6,
    'hatch.linewidth': 0.6,
}
SYST_COLOURS = ['#cc0000', '#3399ff', '#009900', '#cc00cc',
                '#ff6600', '#009999', '#9966ff', '#ff3399']
SIGNAL_LINESTYLES = ['--', ':', '-.', (0, (5, 1)), (0, (3, 1, 1, 1))]
GREY = '#999999'


def _tex(text):
    text = str(text)
    if not any(token in text for token in ('#', '^', '_{')):
        return text
    return '$' + text.replace('#', '\\').replace(' ', '\\ ') + '$'


def _visible(hist):
    return hist.GetXaxis().GetFirst(), hist.GetXaxis().GetLast()


def _arrays(hist):
    first, last = _visible(hist)
    edges = np.array([hist.GetBinLowEdge(i) for i in range(first, last + 2)])
    values = np.array([hist.GetBinContent(i) for i in range(first, last + 1)])
    errors = np.array([hist.GetBinError(i) for i in range(first, last + 1)])
    return edges, values, errors


def _colour(index):
    colour = ROOT.gROOT.GetColor(index)
    return str(colour.AsHexString()) if colour else 'black'


def _band(axis, edges, low, high, **kwargs):
    return axis.fill_between(edges, np.append(low, low[-1]),
                             np.append(high, high[-1]), step='post',
                             linewidth=0, **kwargs)


def _ratio(numerator, denominator):
    return np.divide(numerator, denominator,
                     out=np.zeros_like(numerator, dtype=float),
                     where=denominator > 0)


def _systematics(samples, first, last):
    '''Signed (up, down) shifts for each source, and total (up, down)'''
    num_bins = last - first + 1
    sources = {}
    for sample in samples:
        for item in sample.systematics:
            shifts = np.zeros((last + 1, 2))  # indexed by bin number
            for bin_number, shift in enumerate(item.second):
                if bin_number <= last:
                    shifts[bin_number] = shift.first, shift.second
            source = sources.setdefault(str(item.first),
                                        np.zeros((num_bins, 2)))
            source += shifts[first:]
    total = np.zeros((num_bins, 2))
    for source in sources.values():
        total[:, 0] += np.maximum(source.max(axis=1), 0.)**2
        total[:, 1] += np.maximum((-source).max(axis=1), 0.)**2
    return sources, np.sqrt(total)


class matplotlibPlotter(mplt.MultiPlotter):
    def __init__(self, experiment_name, extra_labels):
        super().__init__(experiment_name, extra_labels)
        self._experiment_name = str(experiment_name)
        self._extra_labels = [str(label) for label in extra_labels]
        self._text_boxes = []

    def addTextBox(self, x1, y1, lines):
        self._text_boxes.append((x1, y1, [str(line) for line in lines]))
        super().addTextBox(x1, y1, lines)

    def plot(self, output_file, output_dir, options=None):
        options = options or {}
        samples = {kind: [(sample, _arrays(sample.histogram))
                          for sample in self.samples(kind)
                          if sample.histogram]
                   for kind in (mplt.Sample.Type.background,
                                mplt.Sample.Type.signal)}
        drawn = sum(samples.values(), [])
        if not drawn:
            raise RuntimeError('Failed to initialise a reference histogram '
                               f'for plot with name \'{output_file}\'.')
        self._name = str(output_file)
        self._edges = drawn[0][1][0]
        self._xlabel = _tex(drawn[0][0].histogram.GetXaxis().GetTitle())
        self._ylabel = _tex(drawn[0][0].histogram.GetYaxis().GetTitle())
        self._backgrounds = samples[mplt.Sample.Type.background]
        self._signals = samples[mplt.Sample.Type.signal]
        self._data = [(sample, _arrays(sample.histogram))
                      for sample in self.samples(mplt.Sample.Type.data)
                      if sample.histogram]

        num_bins = len(self._edges) - 1
        self._sources, self._total_syst = {}, np.zeros((num_bins, 2))
        if options.get('plot-syst-unc', True):
            self._sources, self._total_syst = _systematics(
                [sample for sample, _ in self._backgrounds],
                *_visible(drawn[0][0].histogram))
        breakdown = (bool(self._sources) or bool(self._data)) and \
            options.get('syst-breakdown', True)

        stackings = options.get('stack-sig', ['nostack'])
        y_scalings = options.get('y-axis-scale-types', ['lin'])
        with plt.rc_context(ROOT_STYLE):
            for stacking, x_scaling, y_scaling in itertools.product(
                    stackings, options.get('x-axis-scale-types', ['lin']),
                    y_scalings):
                figure = self._draw(options, breakdown, x_scaling == 'log',
                                    y_scaling == 'log', stacking == 'stack')
                name = str(output_file)
                if len(stackings) > 1:
                    name += '_' + stacking
                if len(y_scalings) > 1:
                    name += '_' + y_scaling
                for fmt in options.get('output-file-types', ['pdf']):
                    figure.savefig(
                        os.path.join(str(output_dir), f'{name}.{fmt}'),
                        transparent=options.get('transparent', False))
                plt.close(figure)

    def _draw(self, options, breakdown, logx, logy, stack_signals):
        figure = plt.figure(figsize=(options.get('width', 800) / 100.,
                                     options.get('height', 800) / 100.))
        grid = figure.add_gridspec(
            2 if breakdown else 1, 1, hspace=0.05,
            height_ratios=(7, 3) if breakdown else (1,),
            left=options.get('margin_left', 0.14),
            right=1. - options.get('margin_right', 0.08),
            top=1. - options.get('margin_top', 0.1),
            bottom=options.get('margin_bottom', 0.1))
        main = figure.add_subplot(grid[0])
        edges = self._edges
        handles, labels, signal_handles = [], [], []
        minimum, maximum, min_positive = 0., 0., np.inf

        nominal = np.zeros(len(edges) - 1)
        variance = np.zeros(len(edges) - 1)
        for sample, (_, values, errors) in self._backgrounds:
            colour = _colour(sample.colour)
            main.stairs(nominal + values, edges, baseline=nominal, fill=True,
                        facecolor=to_rgba(colour, 0.5), zorder=1)
            nominal = nominal + values
            variance += errors**2
            main.stairs(nominal, edges, color=colour, linewidth=2, zorder=2)
            handles.append(Patch(facecolor=to_rgba(colour, 0.5),
                                 edgecolor=colour, linewidth=2))
            labels.append(_tex(sample.name))
        with_stat = options.get('plot-stat-unc', True)
        stat = np.sqrt(variance) if with_stat else np.zeros_like(variance)
        total_up = np.hypot(stat, self._total_syst[:, 0])
        total_down = np.hypot(stat, self._total_syst[:, 1])
        if self._backgrounds:
            if with_stat:
                band = _band(main, edges, nominal - stat, nominal + stat,
                             facecolor='none', edgecolor=GREY, hatch='////',
                             zorder=3)
            maximum = max(maximum, nominal.max())
            minimum = min(minimum, nominal.min())
            if (nominal > 0).any():
                min_positive = min(min_positive, nominal[nominal > 0].min())
            if self._sources:
                if with_stat:
                    handles.append(band)
                    labels.append('Stat. unc.')
                handles.append(_band(main, edges, nominal - total_down,
                                     nominal + total_up, facecolor='black',
                                     alpha=0.25, zorder=4))
                labels.append('Total unc.' if with_stat else 'Syst. unc.')
                maximum = max(maximum, (nominal + total_up).max())

        stacked = nominal.copy()  # signals on top of the backgrounds
        for i, (sample, (_, values, _)) in enumerate(self._signals):
            style = dict(color=_colour(sample.colour), linewidth=2,
                         linestyle=SIGNAL_LINESTYLES[i % len(SIGNAL_LINESTYLES)])
            if stack_signals:
                stacked = values = stacked + values
            main.stairs(values, edges, zorder=5, **style)
            handles.append(Line2D([], [], **style))
            signal_handles.append(handles[-1])
            labels.append(_tex(sample.name))
            maximum = max(maximum, values.max())
            minimum = min(minimum, values.min())
            if (values > 0).any():
                min_positive = min(min_positive, values[values > 0].min())

        data = None
        if self._data:
            data = sum(values for _, (_, values, _) in self._data)
            centres = 0.5 * (edges[1:] + edges[:-1])
            handles.append(main.errorbar(centres, data, yerr=np.sqrt(data),
                                         fmt='o', color='black', markersize=5,
                                         linewidth=1, zorder=6))
            labels.append(_tex(self._data[0][0].name))
            maximum = max(maximum, (data + np.sqrt(data)).max())
            if (data > 0).any():
                min_positive = min(min_positive, data[data > 0].min())

        drawable = maximum > 0. and np.isfinite(maximum)
        if not drawable:
            yields = ', '.join(
                f'\'{sample.name}\': integral={values.sum():g}, '
                f'non-finite bins={np.count_nonzero(~np.isfinite(values))}'
                for sample, (_, values, _)
                in self._backgrounds + self._signals + self._data)
            print(f'Warning: plot \'{self._name}\' has no drawable content '
                  f'({yields}). Check the input histograms.')
            maximum = 1.
        if logy and drawable:
            main.set_yscale('log')
            main.set_ylim(0.1 * (min_positive if min_positive < maximum
                                 else 1.e-3 * maximum), 1.e3 * maximum)
        else:
            main.set_ylim(minimum,
                          (1.4 + 0.1 * max(0, len(handles) - 4)) * maximum)
            main.ticklabel_format(axis='y', scilimits=(-3, 4),
                                  useMathText=True)
        y_range = options.get('log-y-range' if logy else 'y-range')
        if y_range and (not logy or y_range[0] > 0.):
            main.set_ylim(*y_range)
        main.set_xlim(edges[0], edges[-1])
        main.set_ylabel(self._ylabel)
        self._draw_legend(figure, main, options, breakdown, handles, labels,
                          signal_handles)
        main.text(1., 1.01, self._experiment_name, style='italic',
                  ha='right', va='bottom', transform=main.transAxes)
        main.text(0.05, 0.95, '\n'.join(_tex(label)
                                        for label in self._extra_labels),
                  ha='left', va='top', transform=main.transAxes)
        for x1, y1, lines in self._text_boxes:
            figure.text(x1, y1, '\n'.join(_tex(line) for line in lines),
                        ha='left', va='center')

        last = main
        if breakdown:
            last = figure.add_subplot(grid[1], sharex=main)
            main.tick_params(labelbottom=False)
            self._draw_breakdown(last, options, nominal, stat, total_up,
                                 total_down, data)
        if logx:
            main.set_xscale('log')
        last.set_xlabel(self._xlabel)
        figure.align_ylabels()
        return figure

    def _draw_legend(self, figure, main, options, breakdown, handles, labels,
                     signal_handles):
        kwargs = {}
        pad_bottom = 0.3 if breakdown else 0.  # main pad, in figure units
        text_size = options.get('legend-text-size')
        if text_size:  # fraction of the pad height, as for ROOT
            kwargs['fontsize'] = text_size * (1. - pad_bottom) * \
                figure.get_figheight() * 72.
        position = options.get('leg-position') or [None] * 4
        split = options.get('split-leg', False)
        if not split and all(coordinate is None for coordinate in position):
            main.legend(handles, labels, loc='upper right',
                        bbox_to_anchor=(0.98, 0.98), **kwargs)
            return
        defaults = (0.45 if split else 0.68, None, 0.96, 0.88)
        x1, y1, x2, y2 = (default if coordinate is None else coordinate
                          for coordinate, default in zip(position, defaults))
        # ROOT pad coordinates include the margins around the frame
        left, right = (options.get('margin_left', 0.14),
                       1. - options.get('margin_right', 0.08))
        low, high = (0.02 if breakdown else options.get('margin_bottom', 0.1),
                     1. - options.get('margin_top', 0.1))
        pad = BboxTransformTo(Bbox.from_extents(
            -left / (right - left), -low / (high - low),
            (1. - left) / (right - left), (1. - low) / (high - low))) + \
            main.transAxes

        def draw(entries, left, right):
            if not entries:
                return
            bottom = y2 - 0.02 - 0.04 * len(entries) if y1 is None else y1
            main.add_artist(Legend(
                main, *zip(*entries), loc='upper left', borderaxespad=0.,
                bbox_to_anchor=(left, bottom, right - left, y2 - bottom),
                bbox_transform=pad, **kwargs))

        entries = list(zip(handles, labels))
        if not split:
            draw(entries, x1, x2)
            return
        # signals listed apart, in the left half of the legend area
        signals = [entry for entry in entries if entry[0] in signal_handles]
        draw(signals, x1, 0.5 * (x1 + x2))
        draw([entry for entry in entries if entry not in signals],
             0.5 * (x1 + x2), x2)

    def _draw_breakdown(self, axis, options, nominal, stat, total_up,
                        total_down, data):
        edges = self._edges
        centre = 0. if data is None else 1.
        _band(axis, edges, centre - _ratio(total_down, nominal),
              centre + _ratio(total_up, nominal), facecolor='black',
              alpha=0.25)
        if options.get('plot-stat-unc', True):
            _band(axis, edges, centre - _ratio(stat, nominal),
                  centre + _ratio(stat, nominal), facecolor='none',
                  edgecolor=GREY, hatch='////')
        axis.axhline(centre, color='#666666', linewidth=1)

        ranking = sorted(self._sources,
                         key=lambda name: -np.abs(self._sources[name])
                         .max(axis=1).sum())
        handles = []
        for i, name in enumerate(ranking[:options.get('syst-max-sources', 6)]):
            colour = SYST_COLOURS[i % len(SYST_COLOURS)]
            for column, linestyle in enumerate(('-', '--')):
                axis.stairs(centre +
                            _ratio(self._sources[name][:, column], nominal),
                            edges, baseline=None, color=colour, linewidth=2,
                            linestyle=linestyle)
            handles.append(Line2D([], [], color=colour, linewidth=2,
                                  label=_tex(name)))
        largest = _ratio(self._total_syst.max(axis=1), nominal).max()
        if data is not None:
            filled = nominal > 0
            deviation = _ratio(data, nominal) - 1.
            axis.errorbar((0.5 * (edges[1:] + edges[:-1]))[filled],
                          centre + deviation[filled],
                          yerr=_ratio(np.sqrt(data), nominal)[filled],
                          fmt='o', color='black', markersize=5, linewidth=1,
                          zorder=6)
            if filled.any():
                largest = max(largest, np.abs(deviation[filled]).max())
        if not largest > 0.:
            largest = 1.
        axis.set_ylim(centre - 1.5 * largest, centre + 2.4 * largest)
        axis.set_ylabel('Rel. unc.' if data is None else 'Data / MC',
                        loc='center')
        if handles:
            axis.legend(handles=handles, loc='upper left',
                        ncols=min(len(handles), 3))
