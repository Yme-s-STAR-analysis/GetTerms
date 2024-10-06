#include "EffMaker.h"
#include "TH1F.h"
#include "TH2F.h"
#include "TFile.h"
#include "TF1.h"
#include "TString.h"
#include <iostream>

void EffMaker::ReadInEffFile(const char* tpc, const char* tof, const char* pid, const char* nSigTag) {
    TFile* tf_tpc = 0;
    TFile* tf_tof = 0;
    TFile* tf_pid = 0;
    if (strcmp(tpc, "none")) { // true for IS DIFFERENT
	    std::cout << "[LOG] - From EffMaker Module: TPC Efficiency root file path: " << tpc << ".\n";
        tf_tpc = TFile::Open(tpc);
        tpcOff = false;
    } else {
	    std::cout << "[LOG] - From EffMaker Module: TPC Efficiency OFF.\n";
        tpcOff = true;
    }
    if (strcmp(tof, "none")) { // true for IS DIFFERENT
	    std::cout << "[LOG] - From EffMaker Module: TOF Efficiency root file path: " << tof << ".\n";
        tf_tof = TFile::Open(tof);
        tofOff = false;
    } else {
	    std::cout << "[LOG] - From EffMaker Module: TOF Efficiency OFF.\n";
        tofOff = true;
    }
    if (strcmp(pid, "none")) { // true for IS DIFFERENT
        std::cout << "[LOG] - From EffMaker Module: PID Efficiency root file path: " << pid << " with nSigma Tag: " << nSigTag << ".\n";
        tf_pid = TFile::Open(pid);
        pidOff = false;
    } else {
	    std::cout << "[LOG] - From EffMaker Module: PID Efficiency OFF.\n";
        pidOff = true;
    }

    for (int iVz=0; iVz<nVz; iVz++) {
        for (int iCent=0; iCent<nCent; iCent++) {
            for (int iY=0; iY<nY; iY++) {
                if (!tpcOff) {
                    tf_tpc->GetObject(
                        Form("TpcEff_cent%d_vz%d_y%d_Pro", iCent, iVz, iY),
                        ftpc_pro[iCent][iVz][iY]
                    );
                    tf_tpc->GetObject(
                        Form("TpcEff_cent%d_vz%d_y%d_Pbar", iCent, iVz, iY),
                        ftpc_pbar[iCent][iVz][iY]
                    );
                }
                if (!tofOff) {
#ifndef __INTERPOLATE_TOF_EFF__
                    tf_tof->GetObject(
                        Form("TofEff_cent%d_vz%d_y%d_Pro", iCent, iVz, iY),
                        ftof_pro[iCent][iVz][iY]
                    );
                    tf_tof->GetObject(
                        Form("TofEff_cent%d_vz%d_y%d_Pbar", iCent, iVz, iY),
                        ftof_pbar[iCent][iVz][iY]
                    );
#else
                    tf_tof->GetObject(
                        Form("TofEff_cent%d_vz%d_y%d_Pro", iCent, iVz, iY),
                        htof_pro[iCent][iVz][iY]
                    );
                    tf_tof->GetObject(
                        Form("TofEff_cent%d_vz%d_y%d_Pbar", iCent, iVz, iY),
                        htof_pbar[iCent][iVz][iY]
                    );
#endif
                }
            }

        }
    }
    if (!pidOff) {
        tf_pid->GetObject(
            Form("PidEff_%s_Pro", nSigTag),
            pid_pro
        );
        tf_pid->GetObject(
            Form("PidEff_%s_Pbar", nSigTag),
            pid_pbar
        );
    }
    return;
}

double EffMaker::GetTpcEff(bool positive, double pt, double y, int cent, double vz_) {
    if (tpcOff) { return 1.0; }
    if (cent < 0 || cent >= nCent) { return -1; }
    int vz = VzSplit(vz_);
    if (vz < 0) { return -1; }
    int yb = YPSplit(y);
    if (yb < 0) { return -1; }
    if (positive) {
        ff = ftpc_pro[cent][vz][yb];
    } else {
        ff = ftpc_pbar[cent][vz][yb];
    }
    double eff = ff->Eval(pt);
    if (eff < 0 || eff > 1) { return -1; }
    return eff;
}

double EffMaker::GetTofEff(bool positive, double pt, double y, int cent, double vz_) {
    if (tofOff) { return 1.0; }
    if (cent < 0 || cent >= nCent) { return -1; }
    int vz = VzSplit(vz_);
    if (vz < 0) { return -1; }
    int yb = YPSplit(y);
    if (yb < 0) { return -1; }
    double eff = -1;
#ifndef __INTERPOLATE_TOF_EFF__
    if (positive) {
        eff = ftof_pro[cent][vz][yb]->Eval(pt);
    } else {
        eff = ftof_pbar[cent][vz][yb]->Eval(pt);
    }
#else
    if (positive) {
        eff = htof_pro[cent][vz][yb]->Interpolate(pt);
    } else {
        eff = htof_pbar[cent][vz][yb]->Interpolate(pt);
    }
#endif
    if (eff < 0 || eff > 1) { return -1; }
    return eff;
}

double EffMaker::GetPidEff(bool positive, double pt, double y) {
    if (pidOff) { return 1.0; }
    if (positive) {
        th2 = pid_pro;
    } else {
        th2 = pid_pbar;
    }
    int ybin = th2->GetXaxis()->FindBin(y);
    int ptbin = th2->GetYaxis()->FindBin(pt);
    double eff = th2->GetBinContent(ybin, ptbin);
    if (eff < 0 || eff > 1) { return -1; }
    return eff;
}

int EffMaker::VzSplit(double vz) {
    /*
        This depends on your vz split method.
        -1 means invalid vz
    */
    if (-30 < vz && vz < -10) {
        return 0;
    } else if (-10 < vz && vz < 10) {
        return 1;
    } else if (10 < vz && vz < 30) {
        return 2;
    } else if (-50 < vz && vz < -30) {
        return 3;
    } else if (30 < vz && vz < 50) {
        return 4;
    } else {
        return -1;
    }
}

int EffMaker::YPSplit(double y) {
    /*
        v3.0 new
        v3.5 2 more bins
    */
   if (-0.5 < y && y < -0.4) { return 0; }
   else if (-0.4 < y && y < -0.3) { return 1; }
   else if (-0.3 < y && y < -0.2) { return 2; }
   else if (-0.2 < y && y < -0.1) { return 3; }
   else if (-0.1 < y && y < 0.0) { return 4; }
   else if (0.0 < y && y < 0.1) { return 5; }
   else if (0.1 < y && y < 0.2) { return 6; }
   else if (0.2 < y && y < 0.3) { return 7; }
   else if (0.3 < y && y < 0.4) { return 8; }
   else if (0.4 < y && y < 0.5) { return 9; }
   else if (-0.6 < y && y < -0.5) { return 10; }
   else if (0.5 < y && y < 0.6) { return 11; }
   else { return -1; }
}