#include "CentParams.h"
#include "CentCorrTool.h"

CentCorrTool::CentCorrTool() {
    nTofMatchUpperPoly4[0] = new TF1("nTofMatchUpperPoly3_negativeVz", "pol4", 0, 850);
    nTofMatchUpperPoly4[1] = new TF1("nTofMatchUpperPoly3_centralVz", "pol4", 0, 850);
    nTofMatchUpperPoly4[2] = new TF1("nTofMatchUpperPoly3_positiveVz", "pol4", 0, 850);
    nTofMatchLowerPoly4[0] = new TF1("nTofMatchLowerPoly3_negativeVz", "pol4", 0, 850);
    nTofMatchLowerPoly4[1] = new TF1("nTofMatchLowerPoly3_centralVz", "pol4", 0, 850);
    nTofMatchLowerPoly4[2] = new TF1("nTofMatchLowerPoly3_positiveVz", "pol4", 0, 850);
    nTofBetaUpperPoly3 = new TF1("nTofBetaUpperPoly3", "pol3", 0, 850);
    nTofBetaLowerPoly3 = new TF1("nTofBetaLowerPoly3", "pol3", 0, 850);
    for (int i=0; i<3; i++) {
        SetPileUpNTofMatchUpperParam(0., 0., 0., 0., 0., i);
        SetPileUpNTofMatchLowerParam(0., 0., 0., 0., 0., i);
    }

    for (int i=0; i<MAX_TRG; i++) {
        kLumi[i] = 0;
        bLumi[i] = 0;
    }
    
    funcVz = new TF1("funcVz", "pol6", -70, 70);
    for (int i=0; i<9; i++) {
        centSplitEdge[i] = 0;
    }
    doMatchPileUp = doBetaPileUp = doLumi = doVz = true;
    doSplit = false;
}

void CentCorrTool::ReadParams() {
    nTrg = cent_conf::nTrg; 
    std::cout << "[LOG] - ReadParams: The parameter list is named as [" << cent_conf::Name << "] version [" << cent_conf::Mode << "]." << std::endl;
    std::cout << "[LOG] - ReadParams: Number of triggers: " << nTrg << ", list: ";
    for (int i=0; i<nTrg; i++) {
        std::cout << cent_conf::trgList[i] << "\t";
    }
    std::cout << std::endl;

    for (int i=0; i<3; i++) {
        SetPileUpNTofMatchUpperParam(cent_conf::match_upper_pars[i], i);
        SetPileUpNTofMatchLowerParam(cent_conf::match_lower_pars[i], i);
    }
    SetPileUpNTofBetaUpperParam(cent_conf::beta_upper_pars);
    SetPileUpNTofBetaLowerParam(cent_conf::beta_lower_pars);

    for (int i=0; i<nTrg; i++) {
        SetLumiParam(cent_conf::trgList[i], cent_conf::lumi_par[i][0], cent_conf::lumi_par[i][1]);
    }

    for (int i=0; i<nTrg; i++) {
        SetVzParam(cent_conf::trgList[i], &cent_conf::vz_par[i][0]);
    }

    SetCentEdge(cent_conf::cent_edge);
}

int CentCorrTool::ConvertTrg(int trg) {
    for (int i=0; i<nTrg; i++) {
        if (trg == cent_conf::trgList[i]) { 
            return i;
        }
    }
    return -1;
}

int CentCorrTool::LumiCorrection(int trg, int ref3, int zdcx) {
    // trg means converted trgid
    // like: 0 for 610001, 0 is trg and 610001 is trgid 
    double f = zdcx * kLumi[trg] + bLumi[trg];
    double factor = f == 0 ? 0.0 : bLumi[trg] / f;
    return (int)(factor * ref3);
}

int CentCorrTool::VzCorrection(int trg, int ref3, double vz) {
    double factor = parVz[trg][0] / funcVz->Eval(vz);
    return (int)(factor * ref3);
}

int CentCorrTool::GetRefMult3Corr(int refmult, int ref3, int nTofMatch, int nTofBeta, double zdcx, double vz, int trgid) {
    int trg = ConvertTrg(trgid);
    if (trg >= nTrg || trg < 0) {
        return -1;
    }
    int vzbin = GetPileUpVzBin(vz);
    if (vzbin < 0) {
        return -1;
    }
    if (IsPileUp(refmult, nTofMatch, nTofBeta, vzbin)) {
        return -1;
    }
    if (doLumi) {
        ref3 = LumiCorrection(trg, ref3, zdcx);
    }
    if (doVz) {
        ref3 = VzCorrection(trg, ref3, vz);
    }
    return ref3;
}

int CentCorrTool::GetCentrality9(int ref3) {
    if (!doSplit) {
        std::cout << "[WARNING] - GetCentrality9: Centrality bin edge not set yet." << std::endl;
        return -1;
    }
    for (int i=0; i<9; i++) {
        if (ref3 > centSplitEdge[i]) {
            return i;
        }
    }
    return -1;
}

bool CentCorrTool::IsMatchPileUp(int refmult, int nTofMatch, int vzbin) {
    return nTofMatchUpperPoly4[vzbin]->Eval(nTofMatch) < refmult || nTofMatchLowerPoly4[vzbin]->Eval(nTofMatch) > refmult || nTofMatch <= 1;
}

bool CentCorrTool::IsBetaPileUp(int refmult, int nTofBeta) {
    return nTofBetaUpperPoly3->Eval(nTofBeta) < refmult || nTofBetaLowerPoly3->Eval(nTofBeta) > refmult || nTofBeta <= 1;
}

