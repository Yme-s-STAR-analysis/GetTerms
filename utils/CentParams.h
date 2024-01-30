#ifndef __CENT_TOOL_CONFXXX__
#define __CENT_TOOL_CONFXXX__

namespace cent_conf {

    static const int CentCorrToolPatch = 5;
    
    // The name and mode are used to check in the LOG file if the wrong parameter file is used.
    static const char* Name = "14p6";
    static const char* Mode = 
        // "TEST";
        // "PU";
        // "LUMI";
        // "VZ";
        "COMP";

    static const int nTrg = 1;
    static int trgList[nTrg] = {
        650000,
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
        31.515, 0.962225, 0.00350611, -8.76116e-06
    };
    static double beta_lower_pars[4] = {
        -17.7854, 0.632882, 0.000556707, 2.93963e-08
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
        {531.56	,-0.0259305	,0.00209309	,5.81154e-06	,-1.75629e-06	,-1.31774e-09	,2.44224e-10}
    };
    static double vz_parX[nTrg][7] = { // please follow the order of trigger id
        {715.902,-0.0282652	,-0.00746522,4.36012e-07	,-1.47285e-06	,-3.51241e-10	,2.59116e-10}
    };
      
    // centrality split with RefMult3
    static int cent_edge[9] = { // here fill in the centrality bin edge 
        492, 413, 288, 196, 128, 79, 46, 24, 12
    };
    // with RefMult3X
    static int cent_edgeX[9] = { // here fill in the centrality bin edge 
        596, 498, 347, 236, 154, 95, 55, 29, 14
    };

} // namespace cent_conf


#endif
