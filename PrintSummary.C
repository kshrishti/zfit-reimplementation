
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
 
// #include "ROOT/StringUtils.hxx"
 
#include <map>
#include <sstream>
#include <string>
#include <iostream>
#include <fstream>
#include <cstring>

void printSummary(std::string fileName="/afs/cern.ch/user/s/spankajk/CMSSW_11_3_4/python/HiggsAnalysis/CombinedLimit/datacards/ggf_hh4b_boosted/v9/HHModel_model_all.root",TString dname="data_obs")
{
    TFile* f = new TFile(fileName.c_str());
    RooWorkspace* w = (RooWorkspace*)(f->Get("w"));
    RooStats::ModelConfig* mc = (RooStats::ModelConfig*)(w->obj("ModelConfig"));
    //RooDataSet* m_data = w->data("data_obs");

    // Useful functions:
    // RooArgSet* global_obs = (RooArgSet*)mc->GetGlobalObservables()
    // RooArgSet* nuisance_params = (RooArgSet*)mc->GetNuisanceParameters()
    // RooAbsData *proto_data = (RooArgSet*)mc->GetProtoData()
    RooArgSet* obs = (RooArgSet*)mc->GetObservables();
    RooArgSet* pois = (RooArgSet*)mc->GetParametersOfInterest();
    RooDataSet* m_data = (RooDataSet*)w->data(dname);
    // simultaneous fitting of multiple PDFs
    RooSimultaneous* m_pdf = (RooSimultaneous*)mc->GetPdf();
    RooAbsPdf* pdf = (RooAbsPdf*)mc->GetPdf();

    // each channel is a category
    RooAbsCategoryLValue* m_cat = (RooAbsCategoryLValue*)&m_pdf->indexCat();
    int numChannels = m_cat->numBins(0);

    TList* m_dataList = m_data->split( *m_cat, true );
    //w->var("m_H")->setVal(mH);
    std::cout << "\t~~~~~~~~Begin Summary~~~~~~~~" << std::endl;
    std::cout << "\tThe observables are:" << std::endl;
    obs->Print();
    std::cout << "\tThe pois are:" << std::endl;
    pois->Print();
    std::cout << "\tThere are " << numChannels << " sub channels:" << std::endl;
    for ( int i = 0; i < numChannels; i++ ) {
        m_cat->setBin(i);
	    TString channelname=m_cat->getLabel();
        RooAbsPdf* pdfi = m_pdf->getPdf(m_cat->getLabel());
        double value = pdfi->getVal();
        std::cout << "\tPdf value:" << value << std::endl;

        // This also prints out the normalised value: pdfi->printValue(std::cout);

        // RooAbsPdf* prior_pdfi = m_pdf->getPdf();
        RooDataSet* datai = ( RooDataSet* )( m_dataList->At( i ) );
	//double nsigi=w->function("atlas_nsig_ggF_"+channelname)->getVal() + w->function("atlas_nsig_VBF_"+channelname)->getVal() + w->function("atlas_nsig_WH_"+channelname)->getVal() + w->function("atlas_nsig_ZH_"+channelname)->getVal() + w->function("atlas_nsig_ttH_"+channelname)->getVal();
        //std::cout << "\t\tIndex: " << i << ", Pdf: " << pdfi->GetName() << ", Data: " << datai->GetName()  << ", SumEntries: " << datai->sumEntries() << ", NumEntries: "<< datai->numEntries() <<", Nsig: "<<nsigi<<std::endl;
        std::cout << "\t\tIndex: " << i << ", Pdf: " << pdfi->GetName() << ", Data: " << datai->GetName()  << ", SumEntries: " << datai->sumEntries() << ", NumEntries: "<< datai->numEntries() <<std::endl;
    }
    std::cout << "\t~~~~~~~~~End Summary~~~~~~~~~" << std::endl;
}
