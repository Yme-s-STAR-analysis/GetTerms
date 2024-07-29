/*

	Version: 7.0 (29.07.2024)

	1. Centrality tool is changed, so we don't need to compile many times for each data set anymore

	Version: 6.0 (26.06.2024)

	1. RefMult3 is off by default, one can switch it on by adding extra flag when compile

	Version: 4.3 (27.04.2024)

	1. Some useless quantites are removed, and interfaces are changed accordingly

	Version: 4.2 (5.04.2024)

	1. Using latest CentCorrTool with Indian method

	Version: 4.0 (30.01.2024)

	1. Support RefMult3X

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
#include "utils/Loader.h"
#include "utils/CentDefinition.h"
#include "utils/EffMaker.h"

int main(int argc, char** argv){
	/*
		==  v4.3 eTof flag is now canceled
		==  v3.0 new argument: efficiency factor (pabr)
		==  v2.4 new argument: eTOF
		==  v2.3 new argument: task tag
		Arguments: 7
		[1]:tpc eff path:
		[2]:tof eff path:
		[3]:pid eff path:
		[4]:nsigma cut tag: would be like XpY
		// :pid eff mode: 0 or 1 -> CANCELED
		[5]:eff factor (pro)
		[6]:eff factor (pbar)
		[7]:task tag: like trad.y5
		// :eTof: 1 or 0, for use eTOF mass2 or not -> CANCELED
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
#ifdef __REFMULT3__
    TH2D* hNpRef3 = new TH2D("hNprotonRefMult3", ";RefMult3;N_{proton}", 850, -0.5, 849.5, 100, -0.5, 99.5);
    TH2D* hNaRef3 = new TH2D("hNantiprotonRefMult3", ";RefMult3;N_{antiproton}", 850, -0.5, 849.5, 30, -0.5, 29.5);
    TH2D* hNnRef3 = new TH2D("hNnetprotonRefMult3", ";RefMult3;N_{net-proton}", 850, -0.5, 849.5, 80, -10.5, 69.5);
#endif
    TH2D* hNpRef3X = new TH2D("hNprotonRefMult3X", ";RefMult3X;N_{proton}", 1050, -0.5, 1049.5, 100, -0.5, 99.5);
    TH2D* hNaRef3X = new TH2D("hNantiprotonRefMult3X", ";RefMult3X;N_{antiproton}", 1050, -0.5, 1049.5, 30, -0.5, 29.5);
    TH2D* hNnRef3X = new TH2D("hNnetprotonRefMult3X", ";RefMult3X;N_{net-proton}", 1050, -0.5, 1049.5, 80, -10.5, 69.5);

  	std::cout << "[LOG] There will be " << nentries << " events.\n";

	// v2.3 single rapidity for each
	const char* task_tag = argv[7];
	std::cout << "[LOG] - From Core: The tag of this task would be: " << task_tag << ".\n";

	// v4.3 canceled
	// v2.4 eTOF mass2
	// const char* eTofUseInt = argv[8];
	// bool eTofUse;
	// if (atoi(eTofUseInt) == 0) {
	// 	std::cout << "[LOG] - From Core: eTOF mass square will NOT be used in the analysis!\n";
	// 	eTofUse = false;
	// } else {
	// 	std::cout << "[LOG] - From Core: eTOF mass square WILL be used in the analysis!\n";
	// 	eTofUse = true;
	// }
	
	std::ifstream* fin = new std::ifstream();
	fin->open(Form("%s.getTerms.cfg", argv[7]));
	QualityController* qc = new QualityController();
	qc->readConfig(fin);

#ifdef __REFMULT3__
	CentDefinition* centDef3 = new CentDefinition();
	std::cout << "[LOG] - From Core: Initializing centrality tool for RefMult3" << std::endl;
	centDef3->Init("cent_edge.txt");
#endif
	CentDefinition* centDef3X = new CentDefinition();
	std::cout << "[LOG] - From Core: Initializing centrality tool for RefMult3X" << std::endl;
	centDef3->Init("cent_edgeX.txt");

	// efficiency items here (for uncorrected case, just ignore them is okey)
	EffMaker* effMaker = new EffMaker();
	effMaker->ReadInEffFile(argv[1], argv[2], argv[3], argv[4]);
    double eff_factor_pro = std::atof(argv[5]);
    double eff_factor_pbar = std::atof(argv[6]);
	std::cout << "[LOG] - From Core: Efficiency Factor (proton): " << eff_factor_pro << std::endl;
	std::cout << "[LOG] - From Core: Efficiency Factor (antiproton): " << eff_factor_pbar << std::endl;

	StFemtoEvent *event = new StFemtoEvent();
	chain->SetBranchAddress("StFemtoEvent", &event);
	int MaxMult = 1000;

#ifdef __REFMULT3__
	TFile* terms3 = new TFile(Form("%s.root", task_tag), "recreate");
	Loader* lder_n = new Loader("Netp", terms3, MaxMult);
	Loader* lder_p = new Loader("Pro", terms3, MaxMult);
	Loader* lder_a = new Loader("Pbar", terms3, MaxMult);
#endif

	TFile* terms3X = new TFile(Form("%sX.root", task_tag), "recreate");
	Loader* lder_nX = new Loader("Netp", terms3X, MaxMult);
	Loader* lder_pX = new Loader("Pro", terms3X, MaxMult);
	Loader* lder_aX = new Loader("Pbar", terms3X, MaxMult);

	int progress = 0;	
  	for (int iEntry = 0; iEntry < nentries; iEntry++){
		// if (iEntry != 0 && iEntry % 100000 == 0){
		if (iEntry * 100.0 / progress > nentries) {
			std::cout << "[LOG]: Progress: " << iEntry << " / " << nentries << " events finished!\n";
			progress += 5; // show progress per 5% events done
		}

		chain->GetEntry(iEntry);

		// Make Event Cuts
		double vz = event->GetVz();

#ifdef __REFMULT3__
		double refMult3 = event->GetRefMult3();
		int centBin = cent_def->GetCentrality9(refMult3);
		if (refMult3 > MaxMult) { continue; }
		if (centBin < 0) { continue; }
#endif

		double refMult3X = event->GetRefMult3X();
		int centBinX = cent_def->GetCentrality9(refMult3X, true);
		if (refMult3X > MaxMult) { continue; }
		if (centBinX < 0) { continue; }

		if (qc->isBadEvent(vz)) { continue; }

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
			double dca = trk.GetDca();
			double nSig = trk.GetNSigmaProton();
			double mass2 = trk.GetMass2();
			double fYP = fabs(YP);
			// eTOF information is not stored in StFemtoDst now
			// Float_t isETofMass2 = trk.IsETofMass2(); // yes, it's a boolean but I store it using float
			// if (!eTofUse && isETofMass2 == 1.0) { mass2 = -999; }
			
			// Here is the PID selection: use TOF or not
			bool needTOF = false;
			if (fYP < 0.6 && pt > 0.8) { needTOF = true; }
			if (fYP > 0.6 && pt > 0.7) { needTOF = true; }

			// Make track Cut
			if (qc->isBadTrack(pt, YP, nHitsFit, nSig, dca, needTOF, mass2)) {
				continue;
			} // nHitsRatio quantity is already cut when generating the tree

			np += positive;
			na += !positive;

			// detector efficiency

			// for corrected case:
			double pid_eff = effMaker->GetPidEff(positive, pt, YP);

#ifdef __REFMULT3__
			double eff = 1.0;
			double tpc_eff = effMaker->GetTpcEff(positive, pt, YP, centBin, vz);
			double tof_eff = effMaker->GetTofEff(positive, pt, YP, centBin, vz);

			eff = tpc_eff * pid_eff;
			if (needTOF) { eff *= tof_eff; }
			double eff_factor = positive ? eff_factor_pro : eff_factor_pbar;
			eff *= eff_factor;
            eff = eff > 1.0 ? 1.0 : eff;

			if (positive) {
				lder_p->ReadTrack(1.0, eff);
				lder_n->ReadTrack(1.0, eff);
			} else {
				lder_a->ReadTrack(1.0, eff);
				lder_n->ReadTrack(-1.0, eff);
			}
#endif

			double effX = 1.0;
			double tpc_effX = effMaker->GetTpcEff(positive, pt, YP, centBinX, vz);
			double tof_effX = effMaker->GetTofEff(positive, pt, YP, centBinX, vz);

			effX = tpc_effX * pid_eff;
			if (needTOF) { effX *= tof_effX; }
			double eff_factor = positive ? eff_factor_pro : eff_factor_pbar;
			effX *= eff_factor;
            effX = effX > 1.0 ? 1.0 : effX;

			if (positive) {
				lder_pX->ReadTrack(1.0, effX);
				lder_nX->ReadTrack(1.0, effX);
			} else {
				lder_aX->ReadTrack(1.0, effX);
				lder_nX->ReadTrack(-1.0, effX);
			}

		} // track loop ends

#ifdef __REFMULT3__
		lder_p->Store(refMult3);
		lder_a->Store(refMult3);
		lder_n->Store(refMult3);
        hNpRef3->Fill(refMult3, np);
        hNaRef3->Fill(refMult3, na);
        hNnRef3->Fill(refMult3, np - na);
#endif

		lder_pX->Store(refMult3X);
		lder_aX->Store(refMult3X);
		lder_nX->Store(refMult3X);
        hNpRef3X->Fill(refMult3X, np);
        hNaRef3X->Fill(refMult3X, na);
        hNnRef3X->Fill(refMult3X, np - na);

  	} // event loop ends
	
#ifdef __REFMULT3__
	terms3->cd();
	terms3->Write();
	terms3->Close();
#endif

	terms3X->cd();
	terms3X->Write();
	terms3X->Close();

    TFile* p_dist_file = new TFile(Form("%s.pDist.root", task_tag), "recreate");
    p_dist_file->cd();

#ifdef __REFMULT3__
    hNpRef3->Write();
    hNaRef3->Write();
    hNnRef3->Write();
#endif

    hNpRef3X->Write();
    hNaRef3X->Write();
    hNnRef3X->Write();
    p_dist_file->Close();

	std::cout << "[LOG] - From Core: This is the end of getTerms." << std::endl;

  	return 0;
}
