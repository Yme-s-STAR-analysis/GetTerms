#include <TMath.h>

#include "QualityController.h"

QualityController::QualityController() {
    vzMin = -50;
    vzMax = 50;
    // v4.3 vr cut is already applied
    // vrCut = 2;

    // v2.0 these DCAxy/z cut are no more useful
    // nSigDCAzCut = 30.0;
    // nSigsDCAxyCut = 10.0;
    
    ptMin = 0.4;
    ptMax = 2.0;
    // v1.3, by default, rapidity mode is 1 (symmetric about 0)
    rapidityMode = 1; 
    yMin = 0.0;
    yMax = 0.5;
    nHitsFitCut = 20;
    // v4.3 nHitsDedx and nHitsRatio cut are already applied
    // nHitsDedxCut = 5;
    // nHitsRatioCut = 0.52;
    nSigmaCut = 2;
    dcaCut = 1;
    mass2Min = 0.6;
    mass2Max = 1.2;

    isDefault = true;
}

void QualityController::readConfig(std::ifstream* ifConfig) {
    mIfConfig = ifConfig;
    if (!mIfConfig || !mIfConfig->is_open()) {
        std::cout << "[ERROR] - From QualityController Module: Loading hyperparams config failed.\n";
        exit(0);
    }
    std::cout << "[LOG] From QualityController Module: Config file read in, now parsing...\n";
    isDefault = false;

    while (!mIfConfig->eof()) {
        std::string types, val1, val2;
        *mIfConfig >> types;

        if (types == "VARLIST") { // just a header
            continue;
        } else if (types == "VZ") {
            *mIfConfig >> val1 >> val2;
            vzMin = std::stod(val1);
            vzMax = std::stod(val2);
        } else if (types == "PT") {
            *mIfConfig >> val1 >> val2;
            ptMin = std::stod(val1);
            ptMax = std::stod(val2);
        } else if (types == "YP") {
            *mIfConfig >> val1 >> val2;
            yMin = std::stod(val1);
            yMax = std::stod(val2);
        } else if (types == "NHITSFIT") {
            *mIfConfig >> val1;
            nHitsFitCut = std::stod(val1);
        } else if (types == "NSIG") {
            *mIfConfig >> val1;
            nSigmaCut = std::stod(val1);
        } else if (types == "DCA") {
            *mIfConfig >> val1;
            dcaCut = std::stod(val1);
        } else if (types == "MASS2") {
            *mIfConfig >> val1 >> val2;
            mass2Min = std::stod(val1);
            mass2Max = std::stod(val2);
        } else if (types == "RMODE") {
            *mIfConfig >> val1;
            rapidityMode = std::stoi(val1);
        } else if (types == "END") {
            break;
        } else {
            std::cout << "[ERROR] - From QualityController Module: Invalid arugument (" << types << ").\n";
            exit(0);
        }
    }
    // print
    std::cout << "[LOG] From QualityController Module: Parameters read, here is the summary: \n";
    Print();
}

void QualityController::Print() {
    if (isDefault) {
        std::cout << "[LOG] From QualityController Module: Using default cuts:\n";
    } else {
        std::cout << "[LOG] From QualityController Module: Here are the cuts specified:\n";
    }

    std::cout << "=== Event Wise Cuts ===\n";
    std::cout << "= Vz cut: " << vzMin << " - " << vzMax << std::endl;
    std::cout << "= Track Wise Cuts ===\n";
    std::cout << "= pt range: " << ptMin << " - " << ptMax << std::endl;
    if (rapidityMode == 1) {
        std::cout << "= y (proton) range: |" << yMin << "| - |" << yMax << "|" << std::endl;
    } else if (rapidityMode == 2) {
        std::cout << "= y (proton) range: " << yMin << " - " << yMax << std::endl;
    }
    std::cout << "= nHitsFit cut: " << nHitsFitCut << std::endl;
    std::cout << "= nSigma cut: " << nSigmaCut << std::endl;
    std::cout << "= dca cut: " << dcaCut << std::endl;
    std::cout << "= m2 range: " << mass2Min << " - " << mass2Max << std::endl;
}

bool QualityController::isBadEvent(double vz) {
    return (vz < vzMin || vz > vzMax);
}

bool QualityController::isBadTrack(double pt, double y, int nHitsFit, double nSigma, double dca, bool needTOF, double mass2, bool asCut) {
    if (pt <= ptMin || pt >= ptMax) { return true; }
    if (rapidityMode == 1) { y = fabs(y); } // v1.3 new feature, only if the mode is 1, we use absolute value of rapidity
    if (y <= yMin || y >= yMax) { return true; }
    if (nHitsFit <= nHitsFitCut) { return true; }
    if (asCut && !needTOF) {
        if (nSigma >= nSigmaCut || nSigma < 0) { return true; };
    } else {
        if (fabs(nSigma) >= nSigmaCut) { return true; };
    }
    if (dca >= dcaCut) { return true; }
    if (needTOF && (mass2 <= mass2Min || mass2 >= mass2Max)) { 
        return true; 
    }
    return false;
}