import ROOT
import os
import argparse

# ________________________________________________________________________________
def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--indir",
        help="path input directory",
        default="/tmp/selvaggi/data/pre_winter2023_tests_v2/selvaggi_2022Nov24",
    )
    parser.add_argument(
        "--outdir",
        help="path output directory",
        default="/eos/user/s/selvaggi/www/test_tag",
    )

    args = parser.parse_args()

    # Enable multi-threading
    ROOT.ROOT.EnableImplicitMT()

    from examples.FCCee.weaver.config import variables_pfcand, variables_jet, variables_event, flavors

    input_dir = args.indir
    output_dir = args.outdir

    os.system("mkdir -p {}".format(output_dir))

    for f in flavors:

        sample_a = {
            "file": "{}/ntuple_test_wzp6_ee_nunuH_H{}{}.root".format(input_dir, f, f),
            "flavor": f,
            "label": "WZ + Pythia6",
        }
        sample_b = {
            "file": "{}/ntuple_test_p8_ee_ZH_Znunu_H{}{}.root".format(input_dir, f, f),
            "flavor": f,
            "label": "Pythia8",
        }
        # We read the tree from the file and create a RDataFrame.
        df_a = ROOT.RDataFrame("tree", sample_a["file"])
        df_b = ROOT.RDataFrame("tree", sample_b["file"])

        print(sample_a["file"])
        print(sample_b["file"])

        sample_a["histos_pfcand"] = dfhs_pfcand(df_a, variables_pfcand)
        sample_b["histos_pfcand"] = dfhs_pfcand(df_b, variables_pfcand)

        sample_a["histos_jet"] = dfhs_jet(df_a, variables_jet)
        sample_b["histos_jet"] = dfhs_jet(df_b, variables_jet)

        #sample_a["histos_event"] = dfhs_event(df_a, variables_event)
        #sample_b["histos_event"] = dfhs_event(df_b, variables_event)

        # RunGraphs allows to run the event loops of the separate RDataFrame graphs
        # concurrently. This results in an improved usage of the available resources
        # if each separate RDataFrame can not utilize all available resources, e.g.,
        ROOT.RDF.RunGraphs(
            list(sample_a["histos_pfcand"].values())
            + list(sample_b["histos_pfcand"].values())
            + list(sample_a["histos_jet"].values())
            + list(sample_b["histos_jet"].values())
            #+ list(sample_a["histos_event"].values())
            #+ list(sample_b["histos_event"].values())
        )


        for var, params in variables_pfcand.items():
            plot(sample_a, sample_b, "histos_pfcand", var, params, output_dir)
        for var, params in variables_jet.items():
            plot(sample_a, sample_b, "histos_jet", var, params, output_dir)

        """
        for var, params in variables_event.items():
            plot(sample_a, sample_b, "histos_event", var, params, output_dir)
        """

# _______________________________________________________________________________
def dfhs_pfcand(df, vars):

    ## extract charged particles
    # df_charged = df.Filter("All(abs(pfcand_charge)>0)", "select charged constituents")
    df_charged = df

    ## order constituents in energy
    df_sorted_e = df_charged.Define("e_sorted_id", "Reverse(Argsort(pfcand_e))")

    df_dict = dict()

    for pfcand_var, params in vars.items():
        df_var = df_sorted_e.Redefine(pfcand_var, "Take({}, e_sorted_id)".format(pfcand_var))
        var = pfcand_var.replace("pfcand_", "")
        df_var = df_var.Define(var, "{}[0]".format(pfcand_var))
        df_dict[pfcand_var] = df_var.Histo1D(
            (
                "h_{}".format(var),
                ";{};N_{{Events}}".format(params["title"]),
                params["bin"],
                params["xmin"],
                params["xmax"],
            ),
            var,
        )
    return df_dict


# _______________________________________________________________________________
def dfhs_jet(df, vars):

    ## extract charged particles
    # df_charged = df.Filter("All(abs(pfcand_charge)>0)", "select charged constituents")
    df_dict = dict()
    for jet_var, params in vars.items():
        df_dict[jet_var] = df.Histo1D(
            (
                "h_{}".format(jet_var),
                ";{};N_{{Events}}".format(params["title"]),
                params["bin"],
                params["xmin"],
                params["xmax"],
            ),
            jet_var,
        )
    return df_dict


# _______________________________________________________________________________
def dfhs_event(df, vars):

    ## extract charged particles
    # df_charged = df.Filter("All(abs(pfcand_charge)>0)", "select charged constituents")
    df_dict = dict()
    for event_var, params in vars.items():
        print(event_var)
        df_dict[event_var] = df.Histo1D(
            (
                "h_{}".format(event_var),
                ";{};N_{{Events}}".format(params["title"]),
                params["bin"],
                params["xmin"],
                params["xmax"],
            ),
            event_var,
        )
    return df_dict


# _______________________________________________________________________________
def plot(sample_a, sample_b, histo_coll, var, params, outdir):

    dfh_a = sample_a[histo_coll][var].GetValue()
    dfh_b = sample_b[histo_coll][var].GetValue()

    # Create canvas with pads for main plot and data/MC ratio
    c = ROOT.TCanvas("c", "", 700, 750)

    ROOT.gStyle.SetOptStat(0)
    upper_pad = ROOT.TPad("upper_pad", "", 0, 0.35, 1, 1)
    lower_pad = ROOT.TPad("lower_pad", "", 0, 0, 1, 0.35)
    for p in [upper_pad, lower_pad]:
        p.SetLeftMargin(0.14)
        p.SetRightMargin(0.05)
        p.SetTickx(False)
        p.SetTicky(False)
    upper_pad.SetBottomMargin(0)
    lower_pad.SetTopMargin(0)
    lower_pad.SetBottomMargin(0.3)
    upper_pad.Draw()
    lower_pad.Draw()

    # Draw dfh_a
    upper_pad.cd()
    if params["scale"] == "log":
        upper_pad.SetLogy()
    dfh_a.SetMarkerStyle(20)
    dfh_a.SetMarkerSize(0)
    dfh_a.SetLineWidth(4)
    dfh_a.SetLineColor(ROOT.kGreen + 2)
    dfh_a.GetYaxis().SetLabelSize(0.045)
    dfh_a.GetYaxis().SetTitleSize(0.05)
    dfh_a.SetStats(0)
    dfh_a.SetTitle("")
    dfh_a.Draw("hist")

    # Draw dfh_b
    dfh_b.SetLineColor(ROOT.kRed + 1)
    dfh_b.SetLineStyle(2)
    dfh_b.SetLineWidth(4)
    dfh_b.Draw("hist SAME")

    # Draw ratio
    lower_pad.cd()

    ratio = ROOT.TH1I(
        "zero",
        "",
        params["bin"],
        params["xmin"],
        params["xmax"],
    )
    ratio.SetLineColor(ROOT.kBlack)
    ratio.SetLineStyle(2)
    ratio.SetLineWidth(4)
    ratio.SetMinimum(0.0)
    ratio.SetMaximum(2.0)
    ratio.GetXaxis().SetLabelSize(0.08)
    ratio.GetXaxis().SetTitleSize(0.12)
    ratio.GetXaxis().SetTitleOffset(1.0)
    ratio.GetYaxis().SetLabelSize(0.08)
    ratio.GetYaxis().SetTitleSize(0.09)
    ratio.GetYaxis().SetTitle("ratio")
    ratio.GetYaxis().CenterTitle()
    ratio.GetYaxis().SetTitleOffset(0.7)
    # ratio.GetYaxis().SetNdivisions(503, False)
    ratio.GetYaxis().ChangeLabel(-1, -1, 0)
    ratio.GetXaxis().SetTitle(params["title"])
    ratio.Draw("AXIS")

    ratiodata = dfh_a.Clone()
    ratiodata.Sumw2()
    ratiodata.Divide(dfh_b)
    ratiodata.SetLineColor(ROOT.kBlack)
    ratiodata.SetMarkerColor(ROOT.kBlack)
    ratiodata.Draw("same e")

    # Add legend
    upper_pad.cd()
    legend = ROOT.TLegend(0.55, 0.68, 0.926, 0.85)
    legend.SetTextFont(42)
    legend.SetFillStyle(0)
    legend.SetBorderSize(0)
    legend.SetTextSize(0.045)
    legend.SetTextAlign(12)
    legend.AddEntry(dfh_a, "{} ({}-jets)".format(sample_a["label"], sample_a["flavor"]), "l")
    legend.AddEntry(dfh_b, "{} ({}-jets)".format(sample_b["label"], sample_b["flavor"]), "l")
    legend.Draw()

    # Add ATLAS label
    text = ROOT.TLatex()
    text.SetNDC()
    text.SetTextFont(72)
    text.SetTextSize(0.05)
    text.DrawLatex(0.14, 0.91, "FCC-ee")
    text.SetTextFont(42)
    text.DrawLatex(0.27, 0.91, "(Delphes Simulation)")
    text.SetTextSize(0.05)
    text.DrawLatex(0.25, 0.78, "e^{+}e^{-} #rightarrow Z (#nu #nu) H (j j)")
    text.SetTextSize(0.04)
    text.DrawLatex(0.28, 0.71, "j = q, s, c, b, g")
    text.SetTextSize(0.05)
    text.SetTextAlign(31)
    text.DrawLatex(0.95, 0.91, "#sqrt{s} = 240 GeV, 5 ab^{-1}")

    # Save the plot
    figpath = "{}/{}_{}.png".format(outdir, sample_a["flavor"], var)
    c.SaveAs(figpath)


# _______________________________________________________________________________________
if __name__ == "__main__":
    main()
