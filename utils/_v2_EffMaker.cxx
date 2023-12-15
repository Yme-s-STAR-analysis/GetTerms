#include "EffMaker.h"
#include "TH1D.h"
#include "TH2F.h"
#include "TFile.h"
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
            if (!tpcOff) {
                tf_tpc->GetObject(
                    Form("TpcEff_cent%d_vz%d_Pro", iCent, iVz),
                    tpc_pro[iCent][iVz]
                );
                tf_tpc->GetObject(
                    Form("TpcEff_cent%d_vz%d_Pbar", iCent, iVz),
                    tpc_pbar[iCent][iVz]
                );
            }
            if (!tofOff) {
                tf_tof->GetObject(
                    Form("TofEff_cent%d_vz%d_Pro", iCent, iVz),
                    tof_pro[iCent][iVz]
                );
                tf_tof->GetObject(
                    Form("TofEff_cent%d_vz%d_Pbar", iCent, iVz),
                    tof_pbar[iCent][iVz]
                );
            }
        }
        if (!pidOff) {
            tf_pid->GetObject(
                Form("PidEff_%s_vz%d_Pro", nSigTag, iVz),
                pid_pro[iVz]
            );
            tf_pid->GetObject(
                Form("PidEff_%s_vz%d_Pbar", nSigTag, iVz),
                pid_pbar[iVz]
            );
        }
    }
    return;
}

double EffMaker::GetTpcEff(bool positive, double pt, double y, int cent, double vz_) {
    if (tpcOff) { return 1.0; }
    if (cent < 0 || cent >= nCent) { return -1; }
    int vz = VzSplit(vz_);
    if (vz < 0) { return -1; }
    if (positive) {
        th2 = tpc_pro[cent][vz];
    } else {
        th2 = tpc_pbar[cent][vz];
    }
    int x1 = th2->GetXaxis()->FindBin(y);
    int x2 = th2->GetYaxis()->FindBin(pt);
    double eff = th2->GetBinContent(x1, x2);
    if (eff < 0 || eff > 1) { return -1; }
    return eff;
}

double EffMaker::GetTofEff(bool positive, double pt, double y, int cent, double vz_) {
    if (tofOff) { return 1.0; }
    if (cent < 0 || cent >= nCent) { return -1; }
    int vz = VzSplit(vz_);
    if (vz < 0) { return -1; }
    if (positive) {
        th2 = tof_pro[cent][vz];
    } else {
        th2 = tof_pbar[cent][vz];
    }
    int x1 = th2->GetXaxis()->FindBin(y);
    int x2 = th2->GetYaxis()->FindBin(pt);
    double eff = th2->GetBinContent(x1, x2);
    if (eff < 0 || eff > 1) { std::cout << "BAD EFF " << eff << std::endl;return -1; }
    return eff;
}

double EffMaker::GetPidEff(bool positive, double p, double vz_) {
    if (pidOff) { return 1.0; }
    p = p > 3.4 ? 3.4 : p;
    int vz = VzSplit(vz_);
    if (vz < 0) { return -1; }
    if (positive) {
        th1 = pid_pro[vz];
    } else {
        th1 = pid_pbar[vz];
    }
    int x = th1->FindBin(p);
    double eff = th1->GetBinContent(x);
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
    } else {
        return -1;
    }
}