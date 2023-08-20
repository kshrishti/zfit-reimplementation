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
  
#include <map>
#include <sstream>
#include <string>
#include <iostream>
#include <fstream>
#include <cstring>
#include <chrono>

using namespace RooFit;

auto start = std::chrono::high_resolution_clock::now();

void DataExtract(std::string fileName="/afs/cern.ch/user/s/spankajk/CMSSW_11_3_4/python/HiggsAnalysis/CombinedLimit/datacards/ggf_hh4b_boosted/v9/HHModel_model_all.root",TString dname="data_obs") 
{
	std::ofstream outputFile("out.txt");

	// outputFile << "\t~~~~~~~~Begin Summary~~~~~~~~" << std::endl;

	TFile* f = new TFile(fileName.c_str());
    RooWorkspace* w = (RooWorkspace*)(f->Get("w"));
    RooStats::ModelConfig* mc = (RooStats::ModelConfig*)(w->obj("ModelConfig"));
    //RooDataSet* m_data = w->data("data_obs");

    // Useful functions:
    // RooArgSet* global_obs = (RooArgSet*)mc->GetGlobalObservables()
	outputFile << "\nNuisance parameters:" << std::endl;
    RooArgSet* nuisance_params = (RooArgSet*)mc->GetNuisanceParameters();
	nuisance_params->writeToStream(outputFile, false);

// In our case, the proto data is empty (nullptr)
	// outputFile << "Proto data:" << std::endl;
    // RooAbsData *proto_data = (RooAbsData*)mc->GetProtoData();
	// proto_data->printMultiline(outputFile, 1, false);
	outputFile << "\nObservables:" << std::endl;
    RooArgSet* obs = (RooArgSet*)mc->GetObservables();
	obs->writeToStream(outputFile, false);

	outputFile << "\nPOIs:" << std::endl;
    RooArgSet* pois = (RooArgSet*)mc->GetParametersOfInterest();
	pois->writeToStream(outputFile, false);

	outputFile << "\nData entries:" << std::endl;
    RooDataSet* m_data = (RooDataSet*)w->data(dname);
	// sumEntries() actually returns the sum of weigths, which is a much larger number than the actual number of observable increments
	for (int i = 0; i < m_data->sumEntries(); i++) {
		if (m_data->get(i) == NULL) {
			break;
		}
		else {
			m_data->get(i)->writeToStream(outputFile, false);
		}
	}

	// outputFile << "\nPDFs:" << std::endl;
    // simultaneous fitting of multiple PDFs, same thing as `RooAbsPdf* pdf = (RooAbsPdf*)mc->GetPdf();`
    RooSimultaneous* m_pdf = (RooSimultaneous*)mc->GetPdf();
	// m_pdf->printMultiline(outputFile, 1);

    // each channel is a category
    RooAbsCategoryLValue* m_cat = (RooAbsCategoryLValue*)&m_pdf->indexCat();
    int numChannels = m_cat->numBins(0);

    TList* m_dataList = m_data->split( *m_cat, true );
    //w->var("m_H")->setVal(mH);

    outputFile << "\n\tThere are " << numChannels << " sub channels:" << std::endl;
    for ( int i = 0; i < numChannels; i++ ) {
        m_cat->setBin(i);
	    TString channelname=m_cat->getLabel();
        RooAbsPdf* pdfi = m_pdf->getPdf(m_cat->getLabel());
        double value = pdfi->getVal();
        outputFile << "\tPdf normalised value:" << value << std::endl;
		pdfi->printMultiline(outputFile, 1, true);

        // This also prints out the normalised value: pdfi->printValue(std::cout);

        // RooAbsPdf* prior_pdfi = m_pdf->getPdf();
        RooDataSet* datai = ( RooDataSet* )( m_dataList->At( i ) );
        outputFile << "\n\tChannel data:" << value << std::endl;
        for (int j = 0; j < datai->sumEntries(); j++) {
            if (datai->get(j) == NULL) {
                break;
            }
            else {
                datai->get(j)->writeToStream(outputFile, false);
            }
        }
        // datai has the same information as m_data, but including the weights instead of the channel name
        // however, the weights all seem to be 0.0000 L(-1e+09 - 1e+09), so we don't need to reprint this information

	//double nsigi=w->function("atlas_nsig_ggF_"+channelname)->getVal() + w->function("atlas_nsig_VBF_"+channelname)->getVal() + w->function("atlas_nsig_WH_"+channelname)->getVal() + w->function("atlas_nsig_ZH_"+channelname)->getVal() + w->function("atlas_nsig_ttH_"+channelname)->getVal();
        //std::cout << "\t\tIndex: " << i << ", Pdf: " << pdfi->GetName() << ", Data: " << datai->GetName()  << ", SumEntries: " << datai->sumEntries() << ", NumEntries: "<< datai->numEntries() <<", Nsig: "<<nsigi<<std::endl;
        outputFile << "\t\tIndex: " << i << ", Pdf: " << pdfi->GetName() << ", Data: " << datai->GetName()  << ", SumEntries: " << datai->sumEntries() << ", NumEntries: "<< datai->numEntries() <<std::endl;
    }
    // outputFile << "\n\t~~~~~~~~~End Summary~~~~~~~~~" << std::endl;

    auto stop = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(stop - start);
    std::cout << "Time taken by function: " << duration.count() << " microseconds" << std::endl;

	outputFile.close();
}


