/*

	Version: 3.2 (15.12.2023)

	1. DCAxy/z cut here are deprecated, (see QualityController module)

	2. Interfaces from centrality tool are changed

	Version: 3.0 (23.10.2023)

	1. Efficiency factor now need 2 places, 1 for proton and 1 for antiproton.

	Version: 2.6 (16.10.2023)

	1. The VZ range now needs a minimum and a maximum, not a symmetric cut anymore. This change is made in QC module.

	Version: 2.5 (29.09.2023)

	1. The efficiency can be switched off, but it is handled by EffMaker.
	2. eTOF mass is avaliable with new version StFemtoTrack, and we can choose to use it or not with a new argument.
	3. The n sigma of DCAz/xy getter is changed in StFemtoEvent.
	4. Now we support asymmetry rapidity scan (like, -0.7 to 0.5)

	Version: 2.4 (16.08.2023)

	1. The efficiency module now will consider vz, the interfaces are changed so the main function need to be changed.
	2. Will always use 1D pid efficiency, so PID mode argument is canceled.

	Version: 2.3 (07.06.2023)

	1. Cancel: rapidity scan. This will take much time and cost a lot of memory.
	2. Adjust other modules respectively. (using modules version 1.2)

	Version: 2.2 (06.06.2023)

	1. Now using modules version 1.1
	2. PID efficiency was used, no need to use nsigma cut correction
	3. New QualityController Module
	4. Add a __RAPSCAN__ macro for choosing single case or rapidity scan

	Version: 2.1 (10.05.2023)

	1. C1 correction method for nSigma changed cases
	2. Add THIS header on the main.cxx code

*/

// #define __RAPSCAN__

#include <iostream>
#include <utility>
#include <numeric>
#include <algorithm>
#include <fstream>
#include <sstream>
#include <string>
#include <cmath>

#include "TFile.h"
#include "TH2D.h"
#include "TChain.h"
#include "TRandom3.h"
#include "TF1.h"

#include "utils/StFemtoTrack.h"
#include "utils/StFemtoEvent.h"
#include "utils/QualityController.h"
#include "utils/badRunChecker.h"
#include "utils/Loader.h"
#include "utils/CentCorrTool.h"
#include "utils/EffMaker.h"

int main(int argc, char** argv){
	/*
		==  v3.0 new argument: efficiency factor (pabr)
		==  v2.4 new argument: eTOF
		==  v2.3 new argument: task tag
		Arguments: 8
		[1]:tpc eff path:
		[2]:tof eff path:
		[3]:pid eff path:
		[4]:nsigma cut tag: would be like XpY
		// :pid eff mode: 0 or 1 -> CANCELED
		[5]:eff factor (pro)
		[6]:eff factor (pbar)
		[7]:task tag: like trad.y5
		[8]:eTof: 1 or 0, for use eTOF mass2 or not
	*/

	TChain *chain = new TChain("fDst");
	std::ifstream fileList("file.list");
	std::string filename;
	while (fileList >> filename){
		chain->Add(filename.c_str());
	}
  	long int nentries = chain->GetEntries();
  	
	// BadRunChecker cker("/star/u/yghuang/Work/DataAnalysis/BES2/7p7/cumulant/Oct25/empty.list"); // if need a bad run checker
    // prepare a np hist (TH2D for Np and RefMult3)
	// only for |y| < 0.5
    TH2D* hNpRef3 = new TH2D("hNprotonRefMult3", ";RefMult3;N_{proton}", 850, -0.5, 849.5, 100, -0.5, 99.5);
    TH2D* hNaRef3 = new TH2D("hNantiprotonRefMult3", ";RefMult3;N_{antiproton}", 850, -0.5, 849.5, 30, -0.5, 29.5);
    TH2D* hNnRef3 = new TH2D("hNnetprotonRefMult3", ";RefMult3;N_{net-proton}", 850, -0.5, 849.5, 80, -10.5, 69.5);

  	std::cout << "[LOG] There will be " << nentries << " events.\n";

	// v2.3 single rapidity for each
	const char* task_tag = argv[7];
	std::cout << "[LOG] - From Core: The tag of this task would be: " << task_tag << ".\n";

	// v2.4 eTOF mass2
	const char* eTofUseInt = argv[8];
	bool eTofUse;
	if (atoi(eTofUseInt) == 0) {
		std::cout << "[LOG] - From Core: eTOF mass square will NOT be used in the analysis!\n";
		eTofUse = false;
	} else {
		std::cout << "[LOG] - From Core: eTOF mass square WILL be used in the analysis!\n";
		eTofUse = true;
	}
	
	std::ifstream* fin = new std::ifstream();
	fin->open(Form("%s.getTerms.cfg", argv[7]));
	QualityController* qc = new QualityController();
	qc->readConfig(fin);

	CentCorrTool* cent_def = new CentCorrTool();
	cent_def->SetDoMatchPileUp(true);
	cent_def->SetDoBetaPileUp(true);
	cent_def->SetDoLumi(false);
	cent_def->SetDoVz(true);
	cent_def->ReadParams();

	// efficiency items here (for uncorrected case, just ignore them is okey)
	EffMaker* effMaker = new EffMaker();
	effMaker->ReadInEffFile(argv[1], argv[2], argv[3], argv[4]);
    double eff_factor_pro = std::atof(argv[5]);
    double eff_factor_pbar = std::atof(argv[6]);
	std::cout << "[LOG] - From Core: Efficiency Factor (proton): " << eff_factor_pro << std::endl;
	std::cout << "[LOG] - From Core: Efficiency Factor (antiproton): " << eff_factor_pbar << std::endl;

	StFemtoEvent *event = new StFemtoEvent();
	chain->SetBranchAddress("StFemtoEvent", &event);
	int MaxMult = 2000;

	Loader* lder_n = new Loader("Netp", MaxMult);
	Loader* lder_p = new Loader("Pro", MaxMult);
	Loader* lder_a = new Loader("Pbar", MaxMult);

  	for (int iEntry = 0; iEntry < nentries; iEntry++){
		if (iEntry != 0 && iEntry % 100000 == 0){
			std::cout << "[LOG]: - From core: " << iEntry << " events finshed.\n";
		}

		chain->GetEntry(iEntry);

		// Make Event Cuts
		double vz = event->GetVz();
		double vr = event->GetVr();
		double refMult3 = event->GetRefMult3();
		int centBin = cent_def->GetCentrality9(refMult3);
		if (refMult3 > MaxMult){
			continue;
		}
		if (centBin < 0){
			continue;
		}

		if (qc->isBadEvent(vz, vr)) {
			continue;
		}

		// Int_t runId = event->GetRunId(); // uncomment this block if need bad run checker
		// if (cker.isBadRun(runId)){ 
		//   continue;
		// }

		// track loop
        Int_t np = 0;
        Int_t na = 0;
		for (int iTrack = 0; iTrack < event->GetEntries(); iTrack++){

			StFemtoTrack trk = event->GetFemtoTrack(iTrack);
			
			double pt = trk.GetPt(); 
			bool positive = pt > 0; // true if positive pt
			pt = fabs(pt);
			double pcm = trk.GetP();
			double YP = trk.GetY();
			short nHitsFit = trk.GetNHitsFit();
			short nHitsDedx = trk.GetNHitsDedx();
			double dca = trk.GetDca();
			double nSig = trk.GetNSigmaProton();
			double mass2 = trk.GetMass2();
			double fYP = fabs(YP);
			Float_t isETofMass2 = trk.IsETofMass2(); // yes, it's a boolean but I store it using float
			if (!eTofUse && isETofMass2 == 1.0) { mass2 = -999; }
			
			// Here is the PID selection: use TOF or not
			bool needTOF = false;
			if (fYP < 0.6 && pt > 0.8) {
				needTOF = true;
			}
			if (fYP > 0.6 && pt > 0.7) {
				needTOF = true;
			}

			// Make track Cut
			if (qc->isBadTrack(pt, YP, nHitsFit, nHitsDedx, 1.0, nSig, dca, needTOF, mass2)) {
				continue;
			} // nHitsRatio quantity is already cut when generating the tree

			if (positive) { 
				np ++; 
			} else {
				na ++;
			}

			// detector efficiency

			// for corrected case:
			double eff = 1.0;
			double tpc_eff = effMaker->GetTpcEff(positive, pt, YP, centBin, vz);
			double tof_eff = effMaker->GetTofEff(positive, pt, YP, centBin, vz);
			double pid_eff = effMaker->GetPidEff(positive, pcm, vz);

			if (needTOF) {
				eff = tpc_eff * tof_eff * pid_eff;
			} else {
				eff = tpc_eff * pid_eff;
			}

			if (positive) { eff *= eff_factor_pro; } 
			else { eff *= eff_factor_pbar; }

            eff = eff > 1.0 ? 1.0 : eff;
			
			if (positive) {
				lder_p->ReadTrack(1.0, eff);
				lder_n->ReadTrack(1.0, eff);
			} else {
				lder_a->ReadTrack(1.0, eff);
				lder_n->ReadTrack(-1.0, eff);
			}
		} // track loop ends

		lder_p->Store(refMult3);
		lder_a->Store(refMult3);
		lder_n->Store(refMult3);

        hNpRef3->Fill(refMult3, np);
        hNaRef3->Fill(refMult3, na);
        hNnRef3->Fill(refMult3, np - na);

  	} // event loop ends

	lder_p->Save(Form("%s.root", task_tag));
	lder_a->Update(Form("%s.root", task_tag));
	lder_n->Update(Form("%s.root", task_tag));

    TFile* p_dist_file = new TFile(Form("%s.pDist.root", task_tag), "recreate");
    p_dist_file->cd();
    hNpRef3->Write();
    hNaRef3->Write();
    hNnRef3->Write();
    p_dist_file->Close();

	std::cout << "[LOG] - From Core: This is the end of getTerms." << std::endl;

  	return 0;
}