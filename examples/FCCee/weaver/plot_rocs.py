import ROOT
import os
import argparse
import numpy as np
import glob
import sys
from collections import OrderedDict
from copy import deepcopy
from examples.FCCee.weaver.config import variables_pfcand, variables_jet, flavors
import matplotlib.pyplot as plt

## LaTeX rendering (needs latex on PATH, e.g. the LCG texlive)
plt.rc("text", usetex=True)
plt.rc("font", family="serif")
plt.rcParams.update({"font.size": 18})


def texesc(s):
    ## escape LaTeX special characters in a plain string used as a label
    return s.replace("\\", r"\textbackslash{}").replace("_", r"\_").replace("&", r"\&").replace("%", r"\%")


# compute binary discriminant
ROOT.gInterpreter.Declare(
    """
ROOT::VecOps::RVec<float> binary_discriminant(ROOT::VecOps::RVec<float> score_s, ROOT::VecOps::RVec<float> score_b)
{
    ROOT::VecOps::RVec<float> out;
    for (int i=0; i<score_s.size(); i++) {
        float den = score_s.at(i) + score_b.at(i);
        float d = (den > 0) ? score_s.at(i) / den : 0;
        //std::cout<<i<<", "<<d<<std::endl;
        out.push_back(d);
    }
    return out;
}
"""
)

# Enable multi-threading
ROOT.ROOT.EnableImplicitMT()

# ________________________________________________________________________________
## inference-output dirs, laid out as <dir>/wzp6_ee_nunuH_H{f}{f}_ecm240/*.root
DIR_70M = "/eos/experiment/fcc/ee/jet_flavour_tagging/pre_summer2026/roc_inference_70M/"
DIR_W23 = "/eos/experiment/fcc/ee/jet_flavour_tagging/winter2023/wc_pt_7classes_12_04_2023/"

def main():
    args = argparse.ArgumentParser().parse_args()

    ## two 7-class models to compare, same sample layout
    proc_70M = Process("wzp6_70M", "wzp6_ee_nunuH", "pre_summer2026 (70M)", DIR_70M)
    proc_w23 = Process("wzp6_w23", "wzp6_ee_nunuH", "winter2023 (7-class)", DIR_W23)
    variants = [proc_70M, proc_w23]

    ## load the per-flavour score trees for both variants
    samples = dict()
    ## ROC_NFILES caps files/flavour (each ~100k events) for quick tests; 0 = all. MT-safe.
    nfiles_max = int(os.environ.get("ROC_NFILES", "0")) or 10**9
    for proc in variants:
        samples[proc] = dict()
        for f in flavors:
            dirpath = "{}/{}_H{}{}_ecm240/".format(proc.dir, proc.name, f, f)
            files = sorted(glob.glob("{}/*.root".format(dirpath)))[:nfiles_max]
            samples[proc][f] = Sample(files, "events", f, proc)

    roc_param = RocParam(2, 40000)  # nbins = discriminant-histogram bins (ROC threshold resolution)

    def plot_param():
        return PlotParams(
            [Text("FCC-ee simulation (IDEA)", (0.75, 1.03), "bold", 13)],
            ((0.0, 1.0), (0.0001, 1.0)),
            ("jet tagging efficiency", "jet misid. probability"),
            ("linear", "log"),
        )

    ## (signal flavour, [background flavours], short tag); background scores are summed
    pairs = [
        ("b", ["c"],          "b_vs_c"),
        ("b", ["u", "d", "s"], "b_vs_uds"),
        ("c", ["b"],          "c_vs_b"),
        ("c", ["u", "d", "s"], "c_vs_uds"),
        ("s", ["b"],          "s_vs_b"),
        ("s", ["c"],          "s_vs_c"),
        ("s", ["u", "d"],     "s_vs_ud"),
    ]

    for sig, bkg, tag in pairs:
        roc_plot(sig, bkg, tag, variants, samples, roc_param, plot_param())


# _______________________________________________________________________________
class Sample:
    def __init__(self, files, treename, flavor, label):
        self.files = files
        self.treename = treename
        self.flavor = flavor
        self.label = label


# _______________________________________________________________________________
class Process:
    def __init__(self, procname, name, label, dir):
        self.procname = procname
        self.name = name
        self.label = label
        self.dir = dir


# _______________________________________________________________________________
class RocParam:
    def __init__(self, ndec, nbins):
        self.ndec = ndec  # how many decades for log scale
        self.nbins = nbins


# _______________________________________________________________________________
class ROC:
    def __init__(self, name, sig_flavor, bkg_flavors, sample_s, sample_b, param, color, style, variant_label):
        self.name = name
        self.sig_flavor = sig_flavor
        self.bkg_flavors = bkg_flavors
        self.sample_s = sample_s
        self.sample_b = sample_b
        self.range = param.ndec
        self.nbins = param.nbins
        self.color = color
        self.style = style
        self.x = []
        self.y = []

        self.label = "{} vs {} ({})".format(sig_flavor, "".join(bkg_flavors), variant_label)
        df_s = ROOT.RDataFrame(self.sample_s.treename, self.sample_s.files)
        df_b = ROOT.RDataFrame(self.sample_b.treename, self.sample_b.files)

        ## one fine histogram of the tagging discriminant per sample (filled in a single
        ## event loop); the ROC is then the reverse-cumulative of these histograms
        self.h_s = dfh(df_s, sig_flavor, bkg_flavors, self.nbins, "sig_{}".format(self.name))
        self.h_b = dfh(df_b, sig_flavor, bkg_flavors, self.nbins, "bkg_{}".format(self.name))
        self.dhs = [self.h_s, self.h_b]

    def get_roc(self):
        def eff(h):
            nb = h.GetNbinsX()
            c = np.array([h.GetBinContent(i) for i in range(nb + 2)])  # 0=under .. nb+1=over
            tot = c.sum()
            if tot == 0:
                sys.exit("ERROR: histogram is empty...")
            # efficiency to pass D >= threshold, one point per bin lower edge
            revcum = np.cumsum(c[1:nb + 1][::-1])[::-1] + c[nb + 1]
            return revcum / tot

        self.x = eff(self.h_s)  # signal efficiency
        self.y = eff(self.h_b)  # background mis-id

        out_root = ROOT.TFile("{}.root".format(self.name), "RECREATE")
        self.h_s.Write()
        self.h_b.Write()
        out_root.Close()
        return self.x, self.y


# _______________________________________________________________________________
class Text:
    def __init__(self, text, location, weight, size):
        self.text = text
        self.location = location
        self.weight = weight
        self.size = size


# _______________________________________________________________________________
class PlotParams:
    def __init__(self, texts, ranges, axlabels, scales):
        self.texts = texts
        self.ranges = ranges
        self.axlabels = axlabels
        self.scales = scales


# _______________________________________________________________________________
class Graph:
    def __init__(self, rocs, params, fig_file):
        self.rocs = rocs
        self.texts = params.texts
        self.ranges = params.ranges
        self.titles = params.axlabels
        self.scales = params.scales
        self.fig_file = fig_file

        fig, ax = plt.subplots()

        ## plot curves
        print(fig_file)
        for roc in rocs:
            ax.plot(
                roc.x,
                roc.y,
                linestyle=roc.style,
                color=roc.color,
                label=texesc(roc.label),
                linewidth=3,
            )

        # add text to plot
        for text in self.texts:
            ax.text(
                text.location[0],
                text.location[1],
                text.text,
                verticalalignment="center",
                horizontalalignment="center",
                transform=ax.transAxes,
                weight=text.weight,
                fontsize=text.size,
            )

        handles, labels = ax.get_legend_handles_labels()
        ax.legend(
            labels=labels,
            frameon=False,
            # loc=self.leg_loc,
            fontsize=14,
        )

        ax.grid(linestyle="dashed")
        ax.tick_params(axis="both", labelsize=14)
        ax.set_xlabel(self.titles[0], fontsize=14)
        ax.set_ylabel(self.titles[1], fontsize=14)
        ax.set_xscale(self.scales[0])
        ax.set_yscale(self.scales[1])

        ax.set_xlim(self.ranges[0][0], self.ranges[0][1])
        ax.set_ylim(self.ranges[1][0], self.ranges[1][1])

        fig.tight_layout()
        fig.savefig(fig_file)


# _______________________________________________________________________________
def roc_plot(sig, bkg, tag, variants, samples, roc_param, plot_param):
    ## one curve per model variant; background = the flavours in `bkg` combined
    colors = ["black", "red", "blue", "purple", "green"]

    rocs = []
    for iv, proc in enumerate(variants):
        bkg_files = []
        for fb in bkg:
            bkg_files += samples[proc][fb].files
        sample_b = Sample(bkg_files, "events", "".join(bkg), proc)
        name = "{}_{}".format(tag, proc.procname)
        rocs.append(
            ROC(
                name,
                sig,
                bkg,
                samples[proc][sig],
                sample_b,
                roc_param,
                colors[iv % len(colors)],
                "-",
                proc.label,
            )
        )

    dh_list = []
    for roc in rocs:
        dh_list += roc.dhs

    ROOT.RDF.RunGraphs(dh_list)

    for roc in rocs:
        roc.get_roc()

    Graph(rocs, plot_param, "plots/roc_{}.png".format(tag))


# ______________________________________________________________________________
def dfh(df, fs, bkg_flavors, nbins, label):
    ## single fine histogram of the binary discriminant D = score_s / (score_s + Σ score_bkg);
    ## the ROC is recovered from its reverse-cumulative sum (see ROC.get_roc)
    fb = "".join(bkg_flavors)
    score_s = "recojet_is{}".format(fs.upper())
    score_b = "(" + "+".join("recojet_is{}".format(f.upper()) for f in bkg_flavors) + ")"
    dvar = "d_{}{}".format(fs, fb)

    print("producing roc curve: {} vs {} -- {}".format(fs, fb, label))
    df = df.Define(dvar, "binary_discriminant({}, {})".format(score_s, score_b))
    return df.Histo1D(("h_{}".format(label), ";D({},{});jets".format(fs, fb), nbins, 0.0, 1.0), dvar)


# _______________________________________________________________________________________
if __name__ == "__main__":
    main()
