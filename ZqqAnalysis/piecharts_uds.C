#include <TFile.h>
#include <TPie.h>
#include <TPieSlice.h>
#include <TCanvas.h>

int main()
{
  //TFile *huds=TFile::Open("histZuds.root");
  TFile *huds=TFile::Open("histZuds_truthtag.root");

  TPie* h_sJets = (TPie*)huds->Get("sJets");
  TPie* h_dJets = (TPie*)huds->Get("dJets");
  TPie* h_uJets = (TPie*)huds->Get("uJets");

  huds->Close();

  TCanvas *cpie = new TCanvas("cpie","Jet Constituent Distribution",700,700);
  cpie->Divide(2,1);

  cpie->cd(1);
  h_sJets->GetSlice(0)->SetTitle("#pi^{#pm}");
  h_sJets->GetSlice(1)->SetTitle("K^{#pm}");
  h_sJets->GetSlice(2)->SetTitle("K_{L}");
  h_sJets->GetSlice(3)->SetTitle("p");
  h_sJets->GetSlice(4)->SetTitle("n");
  h_sJets->GetSlice(5)->SetTitle("Leptons");
  h_sJets->GetSlice(6)->SetTitle("#gamma");
  //h_sJets->SetRadius(.2);
  h_sJets->SetCircle(0.5,0.77,0.3);
  h_sJets->SetLabelsOffset(.01);
  h_sJets->SetHeight(0.0015);
  //h_sJets->SetLabelFormat("#splitline{%txt}{%perc}");
  h_sJets->Draw("nol 3d");

  cpie->cd(2);
  h_dJets->GetSlice(0)->SetTitle("#pi^{#pm}");
  h_dJets->GetSlice(1)->SetTitle("K^{#pm}");
  h_dJets->GetSlice(2)->SetTitle("K_{L}");
  h_dJets->GetSlice(3)->SetTitle("p");
  h_dJets->GetSlice(4)->SetTitle("n");
  h_dJets->GetSlice(5)->SetTitle("Leptons");
  h_dJets->GetSlice(6)->SetTitle("#gamma");
  //h_dJets->SetRadius(.2);
  h_dJets->SetCircle(0.5,0.77,0.3);
  h_dJets->SetLabelsOffset(.01);
  h_dJets->SetHeight(0.0015);
  //h_dJets->SetLabelFormat("#splitline{%txt}{%perc}");
  h_dJets->Draw("nol 3d");

  cpie->SaveAs("piechart_sd.pdf");

  return -1;
}
