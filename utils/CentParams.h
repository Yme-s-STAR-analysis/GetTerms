#ifndef __CENT_TOOL_CONFXXX__
#define __CENT_TOOL_CONFXXX__

namespace cent_conf {

    static const int CentCorrToolPatch = 6;
    
    // The name and mode are used to check in the LOG file if the wrong parameter file is used.
    static const char* Name = "DATASET";
    static const char* Mode = 
        // "TEST";
        // "PU";
        // "LUMI";
        // "VZ";
        // "COMP";
        "INDIAN";

    static const int nTrg = 1;
    static int trgList[nTrg] = {
        123456,
    };

    // Pile-up parameters

    // Official vz-dependent nTofMatch cut parameters the vz bins are:
    //  - 0 for -70 to -29
    //  - 1 for -29 to +29
    //  - 2 for +29 to +70
    // Will apply 4th order polynoial, instead of 3rd order
    static double match_upper_pars[3][5] = {
        {36.4811873257854, 1.96363692967013, -0.00491528146300182, 1.45179464078414e-5, -1.82634741809226e-8},
        {36.4811873257854, 1.96363692967013, -0.00491528146300182, 1.45179464078414e-5, -1.82634741809226e-8},
        {36.4811873257854, 1.96363692967013, -0.00491528146300182, 1.45179464078414e-5, -1.82634741809226e-8}
    };
    static double match_lower_pars[3][5] = {
        {-16.176117733536, 0.780745107634961, -2.03347057620351e-5, 3.80646723724747e-6, -9.43403282145648e-9},
        {-16.176117733536, 0.780745107634961, -2.03347057620351e-5, 3.80646723724747e-6, -9.43403282145648e-9},
        {-16.176117733536, 0.780745107634961, -2.03347057620351e-5, 3.80646723724747e-6, -9.43403282145648e-9}
    };
    
    // Customized nTofBeta cut parameters, no Vz dependence
    static double beta_upper_pars[4] = {
        0, 0, 0, 0
    };
    static double beta_lower_pars[4] = {
        0, 0, 0, 0
    };

    // Luminosity arguments
    static double lumi_par[nTrg][2] = { // please follow the order of trigger id
        {0, 0}
    };
    static double lumi_parX[nTrg][2] = { // please follow the order of trigger id
        {0, 0}
    };

    // vz arguments
    static double vz_par[nTrg][7] = { // please follow the order of trigger id
        {0, 0, 0, 0, 0, 0, 0}
    };
    static double vz_parX[nTrg][7] = { // please follow the order of trigger id
        {0, 0, 0, 0, 0, 0, 0}
    };
      
    // centrality split with RefMult3
    static int cent_edge[9] = { // here fill in the centrality bin edge 
        492, 413, 288, 196, 128, 79, 46, 24, 12
    };
    // with RefMult3X
    static int cent_edgeX[9] = { // here fill in the centrality bin edge 
        492, 413, 288, 196, 128, 79, 46, 24, 12
    };

    // ======================== Here below are parameters using Indian method
    // Pile-up parameters
    // fitting function: [0] + [1] / pow(x, [2])
    // Note: par [2] is close to -1, whcih means this is indeed approximate a linear function
    static constexpr double Indian_tofMult_upper_pars[3] = {
        0, 0, 0
    };
    static constexpr double Indian_tofMult_lower_pars[3] = {
        0, 0, 0
    };
    static constexpr double Indian_tofMatch_upper_pars[3] = {
        0, 0, 0
    };
    static constexpr double Indian_tofMatch_lower_pars[3] = {
        0, 0, 0
    };
    static constexpr double Indian_tofBeta_upper_pars[3] = {
        0, 0, 0
    };
    static constexpr double Indian_tofBeta_lower_pars[3] = {
        0, 0, 0
    };
    // No luminosity correction in Indian method
    // Vz correction: no trigger bias, point-wise correction
    static constexpr double Indian_vz_pars[100] = { 0.0 };
    static constexpr double Indian_vz_parsX[100] = { 0.0 };
    // Centrality bin edge
    static constexpr int Indian_cent_edge[9] = {
        0, 0, 0, 0, 0, 0, 0, 0, 0
    };
    static constexpr int Indian_cent_edgeX[9] = {
        0, 0, 0, 0, 0, 0, 0, 0, 0
    };


} // namespace cent_conf


#endif
