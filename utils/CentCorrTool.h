#ifndef __CENT_TOOL_HEADER__
#define __CENT_TOOL_HEADER__

/*
    Version: 4.0
    Author: yghuang
    Date: 22.11.2023
*/

#include <iostream>
#include "TF1.h"

class CentCorrTool {

    private:

        static const int MAX_TRG = 10; // the maximum of triggers
        int nTrg; // actual number of triggers, will be read from config file
        
        // Pile up rejection parameters
        double matchUpperPars[5];
        double matchLowerPars[5];
        double betaUpperPars[4];
        double betaLowerPars[4];
        TF1* nTofMatchUpperPoly4[3];
        TF1* nTofMatchLowerPoly4[3];
        TF1* nTofBetaUpperPoly3;
        TF1* nTofBetaLowerPoly3;
        bool doMatchPileUp;
        bool doBetaPileUp;

        // Luminosity correction parameters
        double kLumi[MAX_TRG];
        double bLumi[MAX_TRG];
        bool doLumi;

        // vz correction parameters
        double parVz[MAX_TRG][7]; // 6-order poly + constant
        TF1* funcVz;
        bool doVz;

        // centrality split with bin edge
        double centSplitEdge[9];
        bool doSplit;

    public:
        CentCorrTool();
        ~CentCorrTool(){}

        // -------------------------------------------------------------------
        int ConvertTrg(int trg);
        void ReadParams();
        void SetDoMatchPileUp(bool do_) {
            doMatchPileUp = do_;
            if (do_) {
                std::cout << "[LOG] - nTofMatch pile-up removal: " << "ON" <<std::endl;
            } else {
                std::cout << "[LOG] - nTofMatch pile-up removal: " << "OFF" <<std::endl;
            }
        }
        void SetDoBetaPileUp(bool do_) {
            doBetaPileUp = do_;
            if (do_) {
                std::cout << "[LOG] - nTofBeta pile-up removal: " << "ON" <<std::endl;
            } else {
                std::cout << "[LOG] - nTofBeta pile-up removal: " << "OFF" <<std::endl;
            }
        }
        void SetDoPileUp(bool do_) {
            SetDoMatchPileUp(do_);
            SetDoBetaPileUp(do_);
        }
        void SetDoLumi(bool do_) {
            doLumi = do_;
            if (do_) {
                std::cout << "[LOG] - luminosity correction: " << "ON" <<std::endl;
            } else {
                std::cout << "[LOG] - luminosity correction: " << "OFF" <<std::endl;
            }
        }
        void SetDoVz(bool do_) {
            doVz = do_;
            if (do_) {
                std::cout << "[LOG] - Vz correction: " << "ON" <<std::endl;
            } else {
                std::cout << "[LOG] - Vz correction: " << "OFF" <<std::endl;
            }
        }
        
        // -------------------------------------------------------------------
        // - pile up settings
        // helper functions
        void SetPileUpNTofMatchUpperParam(double p0, double p1, double p2, double p3, double p4, int vzbin) {
            matchUpperPars[0] = p0;
            matchUpperPars[1] = p1;
            matchUpperPars[2] = p2;
            matchUpperPars[3] = p3;
            matchUpperPars[4] = p4;
            SetPileUpNTofMatchUpperParam(matchUpperPars, vzbin);
        }

        void SetPileUpNTofMatchUpperParam(double *p, int vzbin) {
            nTofMatchUpperPoly4[vzbin]->SetParameters(p);
        }

        void SetPileUpNTofMatchLowerParam(double p0, double p1, double p2, double p3, double p4, int vzbin) {
            matchLowerPars[0] = p0;
            matchLowerPars[1] = p1;
            matchLowerPars[2] = p2;
            matchLowerPars[3] = p3;
            matchLowerPars[4] = p4;
            SetPileUpNTofMatchLowerParam(matchLowerPars, vzbin);
        }

        void SetPileUpNTofMatchLowerParam(double *p, int vzbin) {
            nTofMatchLowerPoly4[vzbin]->SetParameters(p);
        }


        void SetPileUpNTofBetaUpperParam(double p0, double p1, double p2, double p3) {
            betaUpperPars[0] = p0;
            betaUpperPars[1] = p1;
            betaUpperPars[2] = p2;
            betaUpperPars[3] = p3;
            nTofBetaUpperPoly3->SetParameters(betaUpperPars);
        }

        void SetPileUpNTofBetaUpperParam(double *p) {
            nTofBetaUpperPoly3->SetParameters(p);
        }

        void SetPileUpNTofBetaLowerParam(double p0, double p1, double p2, double p3) {
            betaLowerPars[0] = p0;
            betaLowerPars[1] = p1;
            betaLowerPars[2] = p2;
            betaLowerPars[3] = p3;
            nTofBetaLowerPoly3->SetParameters(betaLowerPars);
        }

        void SetPileUpNTofBetaLowerParam(double *p) {
            nTofBetaLowerPoly3->SetParameters(p);
        }

        bool IsMatchPileUp(int refmult, int nTofMatch, int vzbin);
        bool IsBetaPileUp(int refmult, int nTofBeta);

        bool IsPileUp(int refmult, int nTofMatch, int nTofBeta, int vzbin) {
            if (doMatchPileUp && doBetaPileUp) {
                return IsMatchPileUp(refmult, nTofMatch, vzbin) || IsBetaPileUp(refmult, nTofBeta);
            }
            if (doMatchPileUp) {
                return IsMatchPileUp(refmult, nTofMatch, vzbin);
            }
            if (doBetaPileUp) {
                return IsBetaPileUp(refmult, nTofBeta);
            }
            return false; // always return NOT pile-up when both switches are OFF
        }

        int GetPileUpVzBin(double vz) {
            // this bin is fixed: for official pile-up cuts with nTofMatch
            if (-70 < vz && vz < -29) { return 0; }
            if (-29 < vz && vz < +29) { return 1; }
            if (+29 < vz && vz < +70) { return 2; }
            return -1;
        }

        // -------------------------------------------------------------------
        // - luminosity settings
        void SetLumiParam(int trgid, double k, double b) {
            int trg = ConvertTrg(trgid);
            if (trg != -1) {
                kLumi[trg] = k;
                bLumi[trg] = b;
            }
        }
        int LumiCorrection(int trg, int ref3, int zdcx);

        // -------------------------------------------------------------------
        // - vz settings
        void SetVzParam(int trgid, double p0, double p1, double p2, double p3, double p4, double p5, double p6) {
            int trg = ConvertTrg(trgid);
            parVz[trg][0] = p0;
            parVz[trg][1] = p1;
            parVz[trg][2] = p2;
            parVz[trg][3] = p3;
            parVz[trg][4] = p4;
            parVz[trg][5] = p5;
            parVz[trg][6] = p6;
            funcVz->SetParameters(&parVz[trg][0]);
        }

        void SetVzParam(int trgid, double* p) {
            int trg = ConvertTrg(trgid);
            parVz[trg][0] = *(p+0);
            parVz[trg][1] = *(p+1);
            parVz[trg][2] = *(p+2);
            parVz[trg][3] = *(p+3);
            parVz[trg][4] = *(p+4);
            parVz[trg][5] = *(p+5);
            parVz[trg][6] = *(p+6);
            funcVz->SetParameters(&parVz[trg][0]);
        }

        int VzCorrection(int trg, int ref3, double vz);

        // -------------------------------------------------------------------
        // - do correction
        int GetRefMult3Corr(int refmult, int ref3, int nTofMatch, int nTofBeta, double zdcx, double vz, int trgid);

        // -------------------------------------------------------------------
        // - centrality split functions
        void SetCentEdge(int e0, int e1, int e2, int e3, int e4, int e5, int e6, int e7, int e8) {
            centSplitEdge[0] = e0;
            centSplitEdge[1] = e1;
            centSplitEdge[2] = e2;
            centSplitEdge[3] = e3;
            centSplitEdge[4] = e4;
            centSplitEdge[5] = e5;
            centSplitEdge[6] = e6;
            centSplitEdge[7] = e7;
            centSplitEdge[8] = e8;
            doSplit = true;
            std::cout << "[LOG] - Centrality bin edge specified.\n";
        }

        void SetCentEdge(int* arr) {
            for (int i=0; i<9; i++) {
                centSplitEdge[i] = *(arr+i);
            }
            doSplit = true;
            std::cout << "[LOG] - Centrality bin edge specified.\n";
        }

        int GetCentrality9(int ref3);

};

#endif
