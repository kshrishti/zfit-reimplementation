
#include "RooWorkspace.h"
#include "RooWorkspaceHandle.h"
#include "RooAbsPdf.h"
#include "RooRealVar.h"
#include "RooCategory.h"
#include "RooAbsData.h"
#include "RooCmdConfig.h"
#include "RooMsgService.h"
#include "RooConstVar.h"
#include "RooResolutionModel.h"
#include "RooPlot.h"
#include "RooRandom.h"
#include "TBuffer.h"
#include "TInterpreter.h"
#include "TClassTable.h"
#include "TBaseClass.h"
#include "TSystem.h"
#include "TRegexp.h"
#include "RooFactoryWSTool.h"
#include "RooAbsStudy.h"
#include "RooTObjWrap.h"
#include "RooAbsOptTestStatistic.h"
#include "TROOT.h"
#include "TFile.h"
#include "TH1.h"
#include "TClass.h"
#include "strlcpy.h"
 
#include "ROOT/StringUtils.hxx"
 
#include <map>
#include <sstream>
#include <string>
#include <iostream>
#include <fstream>
#include <cstring>

using namespace RooFit;

std::unique_ptr<TFile> myFile( TFile::Open("HHModel_model_all.root") );
// can also do TFile *f = new TFile("HHModel_model_all.root");

myFile->ls()
/* 
This should return the following:
TFile**         HHModel_model_all.root
 TFile*         HHModel_model_all.root
  KEY: RooWorkspace     w;1     w
  KEY: TProcessID       ProcessID0;1    4eefebd0-27c5-11ee-892c-0611b9bcbeef
*/
std::unique_ptr<RooWorkspace> w(myFile->Get<RooWorkspace>("w"));
// can also do RooWorkspace *w = (RooWorkspace *)myFile->Get("w");

std::list<RooAbsData *> l = w->allData()
/*
This should return:
(std::list<RooAbsData *>) { @0xe0fe4a0 }
*/
auto l_front = l.begin();
std::advance(l_front, 4);
std::cout << *l_front << '\n'; // but this seems only to return one object, which we can verify with
l.size() // which also returns 1 - therefore for this root file, there seems to be only one RooArgSet of data

w->allFunctions()   // size = 3399
w->allPdfs()        // size = 1172
/*
These should all return:
(RooArgSet) {@0x1292dd60, ...}

None of the lengths match to anything else, though - NuisParams and globalObservables both have a length of 1085
*/

w->allGenericObjects()
/* 
Returns:
(std::list<TObject *>) { @0xe74caa0, @0xee48ec0, @0xd4fdd70 }

This corresponds to end of the output of w->Print():
generic objects
---------------
RooStats::ModelConfig::ModelConfig
RooStats::ModelConfig::ModelConfig_bonly
RooArgSet::discreteParams
*/
std::list<TObject *> g_objs = w->allGenericObjects()
g_objs.back()->Print()
/*
Returns:
RooArgSet:: = () 

Which means there are no discreteParams
*/
g_objs.front()->Print()
/*
=== Using the following for ModelConfig ===
Observables:             RooArgSet:: = (msd,CMS_channel)
Parameters of Interest:  RooArgSet:: = (r,r_gghh,r_qqhh,kl,kt,CV,C2V)
Nuisance Parameters:     RooArgSet:: = (BR_hbb,CMS_bbbb_boosted_ggf_PNetHbbScaleFactors_correlated, ..., THU_HH)
Global Observables:      RooArgSet:: = (BR_hbb_In,CMS_bbbb_boosted_ggf_PNetHbbScaleFactors_correlated_In, ..., THU_HH_In)
PDF:                     RooSimultaneousOpt::model_s[ indexCat=CMS_channel fitfail=pdf_binfitfail SRBin1=pdf_binSRBin1 SRBin2=pdf_binSRBin2 SRBin3=pdf_binSRBin3 extraConstraints=() channelMasks=() ] = 0.000454606
*/
w->pdf("pdf_binfitfail")->Print()     // can do the same for the other pdfs too
/*
RooProdPdf::pdf_binfitfail[ SRBin3_bbbb_boosted_ggf_others_mcstat_bin16_Pdf * SRBin3_bbbb_boosted_ggf_others_mcstat_bin11_Pdf * ... * pdf_binfitfail_nuis * pdfbins_binfitfail ] = 0.000459238
RooProdPdf::pdf_binSRBin1[ SRBin3_bbbb_boosted_ggf_others_mcstat_bin16_Pdf * ... * SRBin1_bbbb_boosted_ggf_others_mcstat_bin13_Pdf * pdf_binSRBin1_nuis * pdfbins_binSRBin1 ] = 0.000380228
RooProdPdf::pdf_binSRBin2 ... = 0.000575812
RooProdPdf::pdf_binSRBin3 ... = 0.000442838
*/

// can also get more detailed view of the pdf - print structure of composite pdf
w->pdf("pdf_binfitfail")->Print("t");
/*
...
0xb03c7c0/V- SimpleGaussianConstraint::SRBin1_qqHH_CV_1_C2V_2_kl_1_hbbhbb_mcstat_bin9_Pdf = 1 [Auto,Dirty] 
    0xb03c0a0/V- RooRealVar::SRBin1_qqHH_CV_1_C2V_2_kl_1_hbbhbb_mcstat_bin9 = 0 +/- 1
    0xb03d220/V- RooRealVar::SRBin1_qqHH_CV_1_C2V_2_kl_1_hbbhbb_mcstat_bin9_In = 0
    0x7279b80/V- RooConstVar::1 = 1
...
Ideally we would also have something like this so we can actually get the values of the coefficients:
0x55abd55192c0 RooAddPdf::model = 0.9/1 [Auto,Clean] 
  0x55abd57f3f50/V- RooChebychev::bkg = 0.8 [Auto,Dirty] 
    0x55abd53f5f10/V- RooRealVar::x = 5
    0x55abd58c75d0/V- RooRealVar::a0 = 0.5
    0x55abd58c7dd0/V- RooRealVar::a1 = 0.2
  0x55abd58c8820/V- RooRealVar::bkgfrac = 0.5
  0x55abd58bce40/V- RooAddPdf::sig = 1/1 [Auto,Clean] 
    0x55abd5842130/V- RooGaussian::sig1 = 1 [Auto,Dirty] 
      0x55abd53f5f10/V- RooRealVar::x = 5
      0x55abd52aa020/V- RooRealVar::mean = 5
      0x55abd58c6890/V- RooRealVar::sigma1 = 0.5
    0x55abd34cf340/V- RooRealVar::sig1frac = 0.8
    0x55abd586ad80/V- RooGaussian::sig2 = 1 [Auto,Dirty] 
      0x55abd53f5f10/V- RooRealVar::x = 5
      0x55abd52aa020/V- RooRealVar::mean = 5
      0x55abd39bef00/V- RooRealVar::sigma2 = 1

An instance of RooAbsArg can have named attributes. 
It also has flags to indicate that either its value or its shape were changed (= it is dirty)
*/


// This prints all the contents of the workspace to the terminal
// Ideally we would be able to print it to a txt file instead of just printing to the terminal 
w->Print()

w->var("msd")->Print()
/*
Returns:
RooRealVar::msd = 215  L(50 - 220) B(17) 
*/
w->var("msd")->writeToStream(std::cout, false)
/*  215.00 L(50 - 220) B(17) */
w->var("msd")->writeToStream(std::cout, true)
/* 215 */

// To print multiline detailed information
w->var("msd")->Print("V")
w->var("msd")->printMultiline(std::cout, 0)

// RooArgSet * 	getAllConstraints (const RooArgSet &observables, RooArgSet &constrainedParams, bool stripDisconnected=true, bool removeConstraintsFromPdf=false)


// // // // // // // // // // // // // // // // // // // // // // // // 

// HOW TO GET INFORMATION STORED IN A FILE
// to redirect to a file?
freopen("out.txt","w",stdout);
w->Print()

// if we know the names of the model, data, and observable, we can use the following code
RooRealVar *x = w->var("x");
RooAbsPdf *model = w->pdf("model");
RooAbsData *data = w->data("modelData");

// This writes the workspace to another root file, but our goal is to write the contents to a txt file
// which can then be read by our zfit algorithm. 
w->writeToFile("RooWorkspace_contents.root")
