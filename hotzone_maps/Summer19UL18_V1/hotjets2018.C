#include "TFile.h"
#include "TH2D.h"
#include "TMath.h"
#include "TBox.h"

#include "tdrstyle_mod15.C"

bool excludeHEM1516 = false;

// Set negative values to zero in TH2D for better "BOX" drawing
void rezero(TH2D* h2, double thr=0, double max=10) {
  
  assert(h2);

  for (int i = 1; i != h2->GetNbinsX()+1; ++i) {
    for (int j = 1; j != h2->GetNbinsY()+1; ++j) {
      if (h2->GetBinContent(i,j)<thr) h2->SetBinContent(i,j,0);
      if (h2->GetBinContent(i,j)>max) h2->SetBinContent(i,j,max);
    }
  }
} // void rezero


void hotjets2018() {

  setTDRStyle();
  TDirectory *curdir = gDirectory;

  //TFile *fem = new TFile("../jecsys2018/rootfiles/coldjets-2018D.root","READ");
  TFile *fem = new TFile("rootfiles/coldjets-18runABCD.root","READ");
  assert(fem && !fem->IsZombie());

  TFile *f0 = new TFile("rootfiles/hotjets-18runABCD.root","READ");
  assert(f0 && !f0->IsZombie());

  //TFile *f1 = new TFile("rootfiles/hotjets-18runABCD.root","READ");
  //assert(f1 && !f1->IsZombie());


  curdir->cd();

  TH2D *h2all = (TH2D*)f0->Get("h2hotfilter"); assert(h2all);
  TH2D *h2em = (TH2D*)fem->Get("all/h2hole"); assert(h2em);

  TH1D *h = new TH1D("h",";#eta_{jet};#phi_{jet}",100,-4.7,4.7);
  h->SetMaximum(+TMath::Pi());
  h->SetMinimum(-TMath::Pi());

  lumi_13TeV = "2018 UL, X.X fb^{-1}";
  TCanvas *c1 = tdrCanvas("c1",h,4,0,kRectangular);

  TLine *l = new TLine();

  l->SetLineStyle(kSolid);
  double etahf = 2.964;
  l->DrawLine(-etahf,-TMath::Pi(),-etahf,+TMath::Pi());
  l->DrawLine(+etahf,-TMath::Pi(),+etahf,+TMath::Pi());
  l->SetLineStyle(kDashed);
  double etatr = 2.5;
  l->DrawLine(-etatr,-TMath::Pi(),-etatr,+TMath::Pi());
  l->DrawLine(+etatr,-TMath::Pi(),+etatr,+TMath::Pi());
  l->SetLineStyle(kDotted);
  double etaec = 1.305;
  l->DrawLine(-etaec,-TMath::Pi(),-etaec,+TMath::Pi());
  l->DrawLine(+etaec,-TMath::Pi(),+etaec,+TMath::Pi());


  rezero(h2all);
  h2all->GetZaxis()->SetRangeUser(-10,10);
  h2all->SetLineColor(kRed);
  h2all->SetLineStyle(kNone);
  h2all->SetFillStyle(1001);
  //h2all->DrawClone("SAMEBOX");
  h2all->SetFillColor(kRed);
  h2all->SetFillColorAlpha(kRed, 0.35); // 35% transparent
  //h2all->DrawClone("SAMEBOX");

  /*
  rezero(h2e);
  h2e->GetZaxis()->SetRangeUser(-10,10);
  h2e->SetFillStyle(1001);
  h2e->SetLineColor(kYellow+1);
  h2e->SetFillColorAlpha(kYellow, 0.35); // 35% transparent
  h2e->Draw("SAMEBOX");
  */

  h2all->SetLineColor(kGray+1);//kRed);
  h2all->SetLineStyle(kNone);
  h2all->SetFillStyle(1001);
  h2all->SetFillColor(kNone);
  h2all->DrawClone("SAMEBOX");

  rezero(h2em);
  h2em->GetZaxis()->SetRangeUser(-10,10);
  h2em->SetLineColor(kBlue);
  h2em->SetFillStyle(1001);
  h2em->SetFillColor(kNone);
  //h2em->SetFillColorAlpha(kBlue, 0.35); // 35% transparent
  h2em->Draw("SAMEBOX");

  // combination of regions
  TH2D *h2sum = (TH2D*)h2all->Clone("h2hot_ul18");
  /*
  h2sum->Add(h2c);
  h2sum->Add(h2d);
  h2sum->Add(h2e);
  h2sum->Add(h2f);
  */
  //rezero(h2sum,20,10); // overlap min. 2
  rezero(h2sum); // no overlap needed

  // Remove also HEM1516
  //TBox HEP17(1.31,-0.5236,2.96,-0.8727); // centered at 28*dphi+/-2
  TBox HEM1516(-2.96,-0.8727,-1.31,-1.5708);
  //TBox HBP2(0,0.5236,1.31,0.8727); // HCAL barrel wedge 2
  TBox HBP2m1(0,0.4363,1.31,0.7854); // HCAL barrel wedge 2 minus 1 tower
  TH2D *h2hem1516 = (TH2D*)h2sum->Clone("h2hot_ul18_plus_hem1516");
  TH2D *h2hbp2m1 = (TH2D*)h2sum->Clone("h2hot_ul18_plus_hbp2m1");
  TH2D *h2both = (TH2D*)h2sum->Clone("h2hot_ul18_plus_hem1516_and_hbp2m1");
  for (int i = 1; i != h2sum->GetNbinsX()+1; ++i) {
    for (int j = 1; j != h2sum->GetNbinsY()+1; ++j) {
      double eta = h2sum->GetXaxis()->GetBinCenter(i);
      double phi = h2sum->GetYaxis()->GetBinCenter(j);
      if (eta>HEM1516.GetX1() && eta<HEM1516.GetX2() &&
	  phi>HEM1516.GetY1() && phi<HEM1516.GetY2())
	h2hem1516->SetBinContent(i, j, 10);
      if (eta>HBP2m1.GetX1() && eta<HBP2m1.GetX2() &&
	  phi>HBP2m1.GetY1() && phi<HBP2m1.GetY2())
	h2hbp2m1->SetBinContent(i, j, 10);
      if ((eta>HEM1516.GetX1() && eta<HEM1516.GetX2() &&
	   phi>HEM1516.GetY1() && phi<HEM1516.GetY2()) ||
	  (eta>HBP2m1.GetX1() && eta<HBP2m1.GetX2() &&
	   phi>HBP2m1.GetY1() && phi<HBP2m1.GetY2()))
	h2both->SetBinContent(i, j, 10);
    } // for i
  } // for j

  h2both->SetLineColor(kMagenta-9);
  h2both->SetLineStyle(kNone);
  h2both->SetFillStyle(1001);
  h2both->SetFillColor(kNone);
  h2both->DrawClone("SAMEBOX");

  h2hem1516->SetLineColor(kRed-9);
  h2hem1516->SetLineStyle(kNone);
  h2hem1516->SetFillStyle(1001);
  h2hem1516->SetFillColor(kNone);
  h2hem1516->DrawClone("SAMEBOX");

  h2hbp2m1->SetLineColor(kOrange-9);
  h2hbp2m1->SetLineStyle(kNone);
  h2hbp2m1->SetFillStyle(1001);
  h2hbp2m1->SetFillColor(kNone);
  h2hbp2m1->DrawClone("SAMEBOX");

  h2sum->SetLineColor(kBlack);
  h2sum->SetLineWidth(2);
  h2sum->SetLineStyle(kNone);
  h2sum->SetFillStyle(1001);
  h2sum->SetFillColor(kNone);
  h2sum->DrawClone("SAMEBOX");

  h2em->DrawClone("SAMEBOX");

  //TLegend *leg = tdrLeg(0.43,0.60,0.63,0.90);
  TLegend *leg = tdrLeg(0.27,0.78,0.47,0.90);
  //leg->AddEntry(h2all,"hot","F");
  leg->AddEntry(h2sum,"hot","F");
  /*
  leg->AddEntry(h2b,"B","F");
  leg->AddEntry(h2c,"C","F");
  leg->AddEntry(h2d,"D","F");
  leg->AddEntry(h2e,"E","F");
  leg->AddEntry(h2f,"F","F");
  //leg->AddEntry(h2em,"EM mask","F");
  leg->AddEntry(h2sum,"UL (min. 2)","F");
  //leg->AddEntry(h2sum,"UL (min. 1)","F");
  */
  leg->AddEntry(h2em,"cold","F");

  // Count fraction of towers in the veto map
  /*
  double sum_bb(0), sum_ec1(0), sum_ec2(0), sum_hf(0);
  double em_bb(0), em_ec1(0), em_ec2(0), em_hf(0);
  double hot_bb(0), hot_ec1(0), hot_ec2(0), hot_hf(0);
  for (int ieta = 1; ieta != h2em->GetNbinsX()+1; ++ieta) {

    double eta = h2em->GetXaxis()->GetBinCenter(ieta);
    for (int iphi = 1; iphi != h2em->GetNbinsY()+1; ++iphi) {

      if (fabs(eta)<etaec) {
	++sum_bb;
	if (h2em->GetBinContent(ieta,iphi)>0) ++em_bb;
	if (h2all->GetBinContent(ieta,iphi)>0) ++hot_bb;
      }
      if (fabs(eta)>etaec && fabs(eta)<etatr) {
	++sum_ec1;
	if (h2em->GetBinContent(ieta,iphi)>0) ++em_ec1;
	if (h2all->GetBinContent(ieta,iphi)>0) ++hot_ec1;
      }
      if (fabs(eta)>etatr && fabs(eta)<etahf) {
	++sum_ec2;
	if (h2em->GetBinContent(ieta,iphi)>0) ++em_ec2;
	if (h2all->GetBinContent(ieta,iphi)>0) ++hot_ec2;
      }
      if (fabs(eta)>etahf) {
	++sum_hf;
	if (h2em->GetBinContent(ieta,iphi)>0) ++em_hf;
	if (h2all->GetBinContent(ieta,iphi)>0) ++hot_hf;
      }
      
    } // for iphi
  } // for ieta

  // Draw fraction of towers in veto map
  TLatex *tex = new TLatex();
  tex->SetNDC();
  tex->SetTextSize(0.030);

  // For EM masked towers (cold jets)
  tex->SetTextColor(kBlue);
  tex->DrawLatex(0.439,0.656,Form("%1.1f%% (%1.1f / %1.1f / %1.1f)",
				100.*(em_bb+em_ec1+em_ec2) /
				  (sum_bb+sum_ec1+sum_ec2),
				  100.*em_bb/sum_bb, 100.*em_ec1/sum_ec1,
				  100.*em_ec2/sum_ec2));

  // For EM IC issues and other excesses (hot jets)
  tex->SetTextColor(kRed);
  tex->DrawLatex(0.668,0.817,Form("%1.1f%% (%1.1f / %1.1f / %1.1f / %1.1f)",
				  100.*(hot_bb+hot_ec1+hot_ec2+hot_hf) /
				  (sum_bb+sum_ec1+sum_ec2+sum_hf),
				  100.*hot_bb/sum_bb, 100.*hot_ec1/sum_ec1,
				  100.*hot_ec2/sum_ec2, 100.*hot_hf/sum_hf));
  */

  double dphi = TMath::TwoPi()/72.;
  HEM1516.SetFillStyle(kNone);
  HEM1516.SetLineColor(kRed+2);
  HEM1516.Draw("SAME");

  HBP2m1.SetFillStyle(kNone);
  HBP2m1.SetLineColor(kOrange+2);
  HBP2m1.Draw("SAME");

  TLatex *tex = new TLatex();
  tex->SetNDC(); tex->SetTextSize(0.045);
  tex->SetTextColor(kRed+2);
  tex->DrawLatex(0.28,0.42,"HEM15/16");
  tex->SetTextColor(kOrange+2);
  //tex->DrawLatex(0.53,0.67,"HBP2: BPIX?");
  tex->DrawLatex(0.50,0.63,"HBP2-1: BPIX?");
  
  gPad->Paint();

  c1->SaveAs("pdf/hotjets2018UL.pdf");

  TFile *fout = new TFile("rootfiles/hotjets-UL18.root","RECREATE");
  h2sum->Write();
  h2hem1516->Write();
  h2hbp2m1->Write();
  h2both->Write();
  fout->Close();
}
