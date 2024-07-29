/*
    Version 2.0 (15.12.2023)

    > DCAxy/z cut is done when generate fDst tree, this options are deprecated, but the interfaces are kept

    Version 1.4 (16.10.2023)

    > Vz range now needs a minimum and maximum instead of symmetric cut

    Version 1.3 (29.09.2023)

    > Additional rapidity mode option, if is 1, we use the symmetric window (about 0), if is 2, we use the specified range
    > Example, 1 with (0.0, 0.5), means -0.5 to 0.5.
    > Example, 2 with (0.0, 0.5), means 0.0 to 0.5

    Version 1.2 (07.06.2023)

    > Add rapidity as a condition.
    
    Version 1.1 (05.06.2023)

    > New hyperparam reading and control system.
*/

#ifndef __YIGE_QLT_CTRL__
#define __YIGE_QLT_CTRL__

#include <fstream>
#include <iostream>
#include <string>

class QualityController {

    private:
        std::ifstream* mIfConfig;
        // event quantities
        double vzMin;
        double vzMax;
        // double vrCut;
        // double nSigDCAzCut;
        // double nSigsDCAxyCut;

        // track quantities
        double ptMin;
        double ptMax;
        int rapidityMode;
        double yMin;
        double yMax;
        double nHitsFitCut;
        // double nHitsDedxCut;
        // double nHitsRatioCut;
        double nSigmaCut;
        double dcaCut;
        double mass2Min;
        double mass2Max;
        // switch: have read config
        bool isDefault;

    public:
        QualityController();
        ~QualityController(){}

        void readConfig(std::ifstream* ifConfig);
        void Print();
        bool isBadEvent(double vz); // vr is removed
        bool isBadTrack(double pt, double y, int nHitsFit, double nSigma, double dca, bool needTOF, double mass2); // nHitsDedx and nHitsRatio are removed
};

#endif
