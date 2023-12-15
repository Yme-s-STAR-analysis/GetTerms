/*

    Version 3.0 (16.10.2023)

    1. Now try read efficiency from root file. NOTE: needs root6!

    2. Vz bins are 5 not 3 now.

    Version 2.1 (29.09.2023)

    > Can directly switch off efficiency (for uncorrected calculation).

    Version 2.0 (16.08.2023)

    > Now Tpc, Tof and Pid effificency will consider Vz dependence.

    Version 1.1.1 (08.06.2023)

    > Fix a little mistake (about the description of pidmode).

    Version 1.1 (05.06.2023)

    > Add PID efficiency

*/

#ifndef YIGE_EFF_MAKER_HEADER
#define YIGE_EFF_MAKER_HEADER

class TH1D;
class TH2F;
class TF1;

class EffMaker{
    private:
        static const int nCent = 9;
        static const int nVz = 5;
    
        // version 2 and lower
        TH2F* tpc_pro[nCent][nVz];
        TH2F* tpc_pbar[nCent][nVz];
        TH2F* tof_pro[nCent][nVz];
        TH2F* tof_pbar[nCent][nVz];

        TH1D* pid_pro[nVz];
        TH1D* pid_pbar[nVz];

        TH1D* th1;
        TH2F* th2;

        // version 3
        static const int nY = 10;
        TF1* ftpc_pro[nCent][nVz][nY];
        TF1* ftpc_pbar[nCent][nVz][nY];
        TF1* ftof_pro[nCent][nVz][nY];
        TF1* ftof_pbar[nCent][nVz][nY];
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
        double GetPidEff(bool positive, double p, double vz);
        // version 3 new
        int YPSplit(double y);
        int VzSplit(double vz);
};

#endif