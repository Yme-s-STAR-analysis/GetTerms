#ifndef YIGE_EFF_MAKER_HEADER
#define YIGE_EFF_MAKER_HEADER

class TH1D;
class TH2F;
class TF1;

class EffMaker{
    private:
        static const int nCent = 9;
        static const int nVz = 5;

        TH2F* pid_pro;
        TH2F* pid_pbar;

        TH2F* th2;

        static const int nY = 12;
        TF1* ftpc_pro[nCent][nVz][nY];
        TF1* ftpc_pbar[nCent][nVz][nY];
#ifdef __INTERPOLATE_TOF_EFF__
        TH1D* htof_pro[nCent][nVz][nY];
        TH1D* htof_pbar[nCent][nVz][nY];
#else
        TF1* ftof_pro[nCent][nVz][nY];
        TF1* ftof_pbar[nCent][nVz][nY];
#endif
        TF1* ff;

        bool tpcOff;
        bool tofOff;
        bool pidOff;

    public:
        EffMaker(){}
        ~EffMaker(){}

        void ReadInEffFile(const char* tpc, const char* tof, const char* pid, const char* nSigTag);
        double GetTpcEff(bool positive, double pt, double y, int cent, double vz);
        double GetTofEff(bool positive, double pt, double y, int cent, double vz);
        // double GetPidEff(bool positive, double p, double vz);
        double GetPidEff(bool positive, double pt, double y, bool asCut);
        // version 3 new
        int YPSplit(double y);
        int VzSplit(double vz);
};

#endif