#include <TFile.h>
#include <TH1F.h>
#include <THStack.h>
#include <TStyle.h>
#include <TCanvas.h>

int main()
{
  TFile *hists=TFile::Open("histZuds.root");

  TH1F* pT = (TH1F*)hists->Get("h_pT");
  TH1F* p = (TH1F*)hists->Get("h_p");
  TH1F* e = (TH1F*)hists->Get("h_e");
  TH1F* theta = (TH1F*)hists->Get("h_theta");
  TH1F* phi = (TH1F*)hists->Get("h_phi");
  TH1F* invM = (TH1F*)hists->Get("h_invM");
  TH1F* invM_RP = (TH1F*)hists->Get("h_invM_RP");
  TH1F* nreco = (TH1F*)hists->Get("h_nreco");

  TH1F* njet = (TH1F*)hists->Get("h_njet");
  TH1F* pjet = (TH1F*)hists->Get("h_pjet");
  TH1F* pTjet = (TH1F*)hists->Get("h_pTjet");
  TH1F* Ejet = (TH1F*)hists->Get("h_Ejet");
  TH1F* jetTheta = (TH1F*)hists->Get("h_jetTheta");
  TH1F* jetPhi = (TH1F*)hists->Get("h_jetPhi");
  TH1F* invMjets = (TH1F*)hists->Get("h_invMjets");
  TH1F* invMjets_b = (TH1F*)hists->Get("h_invMjets_b");
  TH1F* invMjets_c = (TH1F*)hists->Get("h_invMjets_c");
  TH1F* invMjets_s = (TH1F*)hists->Get("h_invMjets_s");
  TH1F* invMjets_u = (TH1F*)hists->Get("h_invMjets_u");
  TH1F* invMjets_d = (TH1F*)hists->Get("h_invMjets_d");
  TH1F* angJP = (TH1F*)hists->Get("h_angJP");
  TH1F* thetaJP = (TH1F*)hists->Get("h_thetaJP");
  TH1F* phiJP = (TH1F*)hists->Get("h_phiJP");

  //hists->Close();

  TCanvas *c1 = new TCanvas("c1","Reco Particles",700,700);
  c1->Divide(2,2);
  //
  c1->cd(1);
  nreco->GetXaxis()->SetTitle("#");
  nreco->Draw();
  //
  c1->cd(2);
  p->GetXaxis()->SetTitle("|p| [GeV]");
  c1->cd(2)->SetLogy();
  p->Draw();
  //
  c1->cd(3);
  e->GetXaxis()->SetTitle("Energy [GeV]");
  c1->cd(3)->SetLogy();
  e->Draw();
  //
  c1->cd(4);
  pT->GetXaxis()->SetTitle("p_{T} [GeV]");
  c1->cd(4)->SetLogy();
  pT->Draw();
  //
  c1->Print("recoParticles.pdf");
  
  TCanvas *c2 = new TCanvas("c2","Reco Particles - Angular Distribution",710,710);
  c2->Divide(1,2);
  //
  c2->cd(1);
  theta->GetXaxis()->SetTitle("#theta");
  theta->Draw();
  //
  c2->cd(2);
  phi->GetXaxis()->SetTitle("#phi");
  phi->Draw();
  //
  c2->Print("reco_angDistribution.pdf");
  
  TCanvas *c3 = new TCanvas("c3","Invariant Mass",720,720);
  c3->Divide(1,2);
  //
  c3->cd(1);
  invM->GetXaxis()->SetTitle("M_{inv} [GeV]");
  invM->Draw();
  //
  c3->cd(2);
  invM_RP->GetXaxis()->SetTitle("M_{inv} [MeV]");
  c3->cd(2)->SetLogy();
  invM_RP->Draw();
  //
  c3->Print("invM_reco.pdf");

  TCanvas *c4 = new TCanvas("c4","Jets (eekt)",730,730);
  c4->Divide(2,2);
  //
  c4->cd(1);
  njet->GetXaxis()->SetTitle("#");
  njet->Draw();
  //
  c4->cd(2);
  pjet->GetXaxis()->SetTitle("|p| [GeV]");
  //c4->cd(2)->SetLogy();
  pjet->Draw();
  //
  c4->cd(3);
  Ejet->GetXaxis()->SetTitle("Energy [GeV]");
  //c4->cd(3)->SetLogy();
  Ejet->Draw();
  //
  c4->cd(4);
  pTjet->GetXaxis()->SetTitle("p_{T} [GeV]");
  //c4->cd(4)->SetLogy();
  pTjet->Draw();
  //
  c4->Print("jets_eekt.pdf");

  TCanvas *c5 = new TCanvas("c5","Jets - Angular Distribution (eekt)",740,740);
  c5->Divide(1,2);
  //
  c5->cd(1);
  jetTheta->GetXaxis()->SetTitle("#theta");
  //c5->cd(1)->SetLogy();
  jetTheta->Draw();
  //
  c5->cd(2);
  jetPhi->GetXaxis()->SetTitle("#phi");
  //c5->cd(2)->SetLogy();
  jetPhi->Draw();
  //
  c5->Print("jetAngularDist_eekt.pdf");
  
  TCanvas *c6 = new TCanvas("c6","Invariant Mass (jet sum)",750,750);
  invMjets->GetXaxis()->SetTitle("M_{inv} [GeV]");
  invMjets->Draw();
  //
  c6->Print("invM_jetsum_eekt.pdf");

  TCanvas *c7 = new TCanvas("c7","Invariant Mass - uds (stacked)",760,760);
  THStack *hs = new THStack("hs","Invariant Mass - uds");
  gStyle->SetPalette(kOcean);
  //invMjets_s->SetFillColor(kRed);
  hs->Add(invMjets_s);
  //invMjets_u->SetFillColor(kBlue);
  hs->Add(invMjets_u);
  //invMjets_d->SetFillColor(kGreen);
  hs->Add(invMjets_d);
  hs->Add(invMjets_c);
  hs->Add(invMjets_b);
  hs->Draw("pfc");
  hs->GetXaxis()->SetTitle("M_{inv} [GeV]");
  gPad->BuildLegend(0.75,0.75,0.95,0.95,"");
  //
  c7->Print("invM_stack_eekt.pdf");

  TCanvas *c8 = new TCanvas("c8","Jet Constituents - Angular Distribution (eekt)",770,770);
  c8->Divide(2,2);
  //
  c8->cd(1);
  angJP->GetXaxis()->SetTitle("[rad]");
  c8->cd(1)->SetLogy();
  angJP->Draw();
  //
  c8->cd(2);
  thetaJP->GetXaxis()->SetTitle("#Delta#theta [rad]");
  c8->cd(2)->SetLogy();
  thetaJP->Draw();
  //
  c8->cd(3);
  phiJP->GetXaxis()->SetTitle("#Delta#phi [rad]");
  c8->cd(3)->SetLogy();
  phiJP->Draw();
  //
  c8->Print("jetConstAngularDist_eekt.pdf");
  
  hists->Close();
  
  return -1;
}
