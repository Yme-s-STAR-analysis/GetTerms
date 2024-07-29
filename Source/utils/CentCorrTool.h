#ifndef __CENT_TOOL_HEADER__
#define __CENT_TOOL_HEADER__

/*
    Version: 6.0
    Author: yghuang
    Date: 04.04.2024
*/

#include <iostream>
#include "TF1.h"
#include "TRandom3.h"

class CentCorrTool {

    private:

        static const int PatchNumber = 6;

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
        // v4.1 new: interfaces for RefMult3X
        double kLumiX[MAX_TRG];
        double bLumiX[MAX_TRG];
        bool doLumiX;

        // vz correction parameters
        double parVz[MAX_TRG][7]; // 6-order poly + constant
        TF1* funcVz;
        bool doVz;
        // v4.1 new: interfaces for RefMult3X
        double parVzX[MAX_TRG][7]; // 6-order poly + constant
        TF1* funcVzX;
        bool doVzX;

        // centrality split with bin edge
        double centSplitEdge[9];
        bool doSplit;
        double centSplitEdgeX[9];
        bool doSplitX;

        // Indian method
        TF1* Indian_PileUpCurve[3][2]; // [tofMult, tofMatch, tofBeta][upper lower]
        double Indian_vzPars[100];
        double Indian_vzParsX[100];
        double Indian_centSplitEdge[9];
        double Indian_centSplitEdgeX[9];
        TRandom3* rd;
        bool IsIndian;

    public:
        CentCorrTool();
        ~CentCorrTool(){}

        // -------------------------------------------------------------------
        int ConvertTrg(int trg);
        void ReadParams();
        void SetDoMatchPileUp(bool do_) {
            doMatchPileUp = do_;
            if (do_) {
                std::cout << "[LOG] - CentCorrTool: nTofMatch pile-up removal: " << "ON" <<std::endl;
            } else {
                std::cout << "[LOG] - CentCorrTool: nTofMatch pile-up removal: " << "OFF" <<std::endl;
            }
        }
        void SetDoBetaPileUp(bool do_) {
            doBetaPileUp = do_;
            if (do_) {
                std::cout << "[LOG] - CentCorrTool: nTofBeta pile-up removal: " << "ON" <<std::endl;
            } else {
                std::cout << "[LOG] - CentCorrTool: nTofBeta pile-up removal: " << "OFF" <<std::endl;
            }
        }
        void SetDoPileUp(bool do_) {
            SetDoMatchPileUp(do_);
            SetDoBetaPileUp(do_);
        }
        void SetDoLumi(bool do_) {
            doLumi = do_;
            if (do_) {
                std::cout << "[LOG] - CentCorrTool: Luminosity correction (RefMult3): " << "ON" <<std::endl;
            } else {
                std::cout << "[LOG] - CentCorrTool: Luminosity correction (RefMult3): " << "OFF" <<std::endl;
            }
        }
        void SetDoLumiX(bool do_) {
            doLumiX = do_;
            if (do_) {
                std::cout << "[LOG] - CentCorrTool: Luminosity correction (RefMult3X): " << "ON" <<std::endl;
            } else {
                std::cout << "[LOG] - CentCorrTool: Luminosity correction (RefMult3X): " << "OFF" <<std::endl;
            }
        }
        void SetDoVz(bool do_) {
            doVz = do_;
            if (do_) {
                std::cout << "[LOG] - CentCorrTool: Vz correction (RefMult3): " << "ON" <<std::endl;
            } else {
                std::cout << "[LOG] - CentCorrTool: Vz correction (RefMult3): " << "OFF" <<std::endl;
            }
        }
        void SetDoVzX(bool do_) {
            doVzX = do_;
            if (do_) {
                std::cout << "[LOG] - CentCorrTool: Vz correction (RefMult3X): " << "ON" <<std::endl;
            } else {
                std::cout << "[LOG] - CentCorrTool: Vz correction (RefMult3X): " << "OFF" <<std::endl;
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

        // -------------------------------------------------------------------
        // - luminosity settings for RefMult3X
        void SetLumiParamX(int trgid, double k, double b) {
            int trg = ConvertTrg(trgid);
            if (trg != -1) {
                kLumiX[trg] = k;
                bLumiX[trg] = b;
            }
        }

        int LumiCorrection(int trg, int ref3, int zdcx, bool withX=false);

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

        // -------------------------------------------------------------------
        // - vz settings for RefMult3X
        void SetVzParamX(int trgid, double p0, double p1, double p2, double p3, double p4, double p5, double p6) {
            int trg = ConvertTrg(trgid);
            parVzX[trg][0] = p0;
            parVzX[trg][1] = p1;
            parVzX[trg][2] = p2;
            parVzX[trg][3] = p3;
            parVzX[trg][4] = p4;
            parVzX[trg][5] = p5;
            parVzX[trg][6] = p6;
            funcVzX->SetParameters(&parVzX[trg][0]);
        }

        void SetVzParamX(int trgid, double* p) {
            int trg = ConvertTrg(trgid);
            parVzX[trg][0] = *(p+0);
            parVzX[trg][1] = *(p+1);
            parVzX[trg][2] = *(p+2);
            parVzX[trg][3] = *(p+3);
            parVzX[trg][4] = *(p+4);
            parVzX[trg][5] = *(p+5);
            parVzX[trg][6] = *(p+6);
            funcVzX->SetParameters(&parVzX[trg][0]);
        }

        int VzCorrection(int trg, int ref3, double vz, bool withX=false);

        // -------------------------------------------------------------------
        // - do correction
        int GetRefMult3Corr(int refmult, int ref3, int nTofMatch, int nTofBeta, double zdcx, double vz, int trgid, bool withX=false);

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
            std::cout << "[LOG] - CentCorrTool: Centrality bin edge (RefMult3) specified.\n";
        }

        void SetCentEdge(int* arr) {
            for (int i=0; i<9; i++) {
                centSplitEdge[i] = *(arr+i);
            }
            doSplit = true;
            std::cout << "[LOG] - CentCorrTool: Centrality bin edge (RefMult3) specified.\n";
        }

        // -------------------------------------------------------------------
        // - centrality split functions for RefMult3X
        void SetCentEdgeX(int e0, int e1, int e2, int e3, int e4, int e5, int e6, int e7, int e8) {
            centSplitEdgeX[0] = e0;
            centSplitEdgeX[1] = e1;
            centSplitEdgeX[2] = e2;
            centSplitEdgeX[3] = e3;
            centSplitEdgeX[4] = e4;
            centSplitEdgeX[5] = e5;
            centSplitEdgeX[6] = e6;
            centSplitEdgeX[7] = e7;
            centSplitEdgeX[8] = e8;
            doSplitX = true;
            std::cout << "[LOG] - CentCorrTool: Centrality bin edge (RefMult3X) specified.\n";
        }
        void SetCentEdgeX(int* arr) {
            for (int i=0; i<9; i++) {
                centSplitEdgeX[i] = *(arr+i);
            }
            doSplitX = true;
            std::cout << "[LOG] - CentCorrTool: Centrality bin edge (RefMult3X) specified.\n";
        }

        int GetCentrality9(int ref3, bool withX=false);

        // Indian method
        void EnableIndianMethod(bool enable=false) { IsIndian = enable; }
        bool IsIndianPileUp(int refMult, int tofMult, int tofMatch, int tofBeta);
        int IndianVzCorrection(int ref3, double vz, bool withX=false);
        int GetIndianRefMult3Corr(int refMult, int ref3, int tofMult, int tofMatch, int tofBeta, double vz, bool withX=false);

};

#endif
