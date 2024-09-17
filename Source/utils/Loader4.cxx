// Yige Huang -- 30.01.2024 update
//Zhang Yu -- Dec 2020
#include "TProfile.h"
#include "TH1D.h"
#include "TFile.h"
#include "Loader4.h"

Loader::Loader(const char* type, TFile* tf, int MaxMult) : ParticleType(type), _nMultBin(MaxMult+1) {
	for(int r=1;r<=4;++r) {
		for(int s=1; s<=r;++s) {
			_q[r][s] = 0;
		}
  	}
	ppb = 0;
	tf->cd();
  	for(int i=1;i<=_nTerms;++i) {
		_V[i] = new TProfile(Form("%s_%s", ParticleType, Terms[i-1]),"", _nMultBin, -0.5, _nMultBin-0.5);
		_V[i]->SetDirectory(tf->CurrentDirectory());
  	}
}

Loader::~Loader() {
  	for(int i=1;i<=_nTerms;++i) {
		delete _V[i];
  	}
}

void Loader::ReadTrack(float Particle, float eff) {
  	for(int r=1;r<=4; ++r){
		for(int s=1; s<=r; ++s) {
	  		_q[r][s] += (pow(Particle,r)/pow(eff, s));
		}
  	}
	ppb += fabs(Particle)/eff; // only 1st order
}

void Loader::Store(int RefMult) {

	_V[1]->Fill(RefMult, _q[1][1]*_q[2][1]*_q[2][2]*_q[3][2]);
	_V[2]->Fill(RefMult, _q[1][1]*_q[2][1]*_q[2][2]*_q[3][1]);
	_V[3]->Fill(RefMult, _q[1][1]*_q[2][1]*_q[2][2]*_q[3][3]);
	_V[4]->Fill(RefMult, pow(_q[1][1], 2)*pow(_q[2][1], 2)*_q[2][2]);
	_V[5]->Fill(RefMult, pow(_q[1][1], 2)*_q[2][1]*pow(_q[2][2], 2));
	_V[6]->Fill(RefMult, _q[1][1]*pow(_q[2][1], 2)*_q[3][3]);
	_V[7]->Fill(RefMult, _q[1][1]*pow(_q[2][2], 2)*_q[3][3]);
	_V[8]->Fill(RefMult, pow(_q[1][1], 2)*_q[2][2]*_q[3][1]);
	_V[9]->Fill(RefMult, pow(_q[1][1], 2)*_q[2][1]*_q[4][3]);
	_V[10]->Fill(RefMult, pow(_q[1][1], 2)*_q[2][1]*_q[4][2]);
	_V[11]->Fill(RefMult, pow(_q[1][1], 2)*_q[3][2]*_q[3][3]);
	_V[12]->Fill(RefMult, _q[1][1]*pow(_q[2][1], 2)*_q[2][2]);
	_V[13]->Fill(RefMult, pow(_q[1][1], 2)*_q[3][1]*_q[3][2]);
	_V[14]->Fill(RefMult, _q[1][1]*pow(_q[2][1], 2)*_q[3][2]);
	_V[15]->Fill(RefMult, pow(_q[1][1], 2)*_q[2][1]*_q[4][4]);
	_V[16]->Fill(RefMult, pow(_q[1][1], 3)*_q[2][1]*_q[3][2]);
	_V[17]->Fill(RefMult, _q[1][1]*pow(_q[2][2], 2)*_q[3][1]);
	_V[18]->Fill(RefMult, pow(_q[1][1], 3)*_q[2][2]*_q[3][1]);
	_V[19]->Fill(RefMult, pow(_q[1][1], 3)*_q[2][1]*_q[3][3]);
	_V[20]->Fill(RefMult, pow(_q[1][1], 2)*_q[2][2]*_q[4][1]);
	_V[21]->Fill(RefMult, pow(_q[1][1], 2)*_q[2][2]*_q[4][4]);
	_V[22]->Fill(RefMult, _q[1][1]*pow(_q[2][1], 2)*_q[3][1]);
	_V[23]->Fill(RefMult, pow(_q[1][1], 2)*_q[2][1]*_q[3][1]);
	_V[24]->Fill(RefMult, pow(_q[1][1], 4)*_q[2][1]*_q[2][2]);
	_V[25]->Fill(RefMult, pow(_q[1][1], 2)*_q[2][1]*_q[3][3]);
	_V[26]->Fill(RefMult, pow(_q[1][1], 3)*_q[2][2]*_q[3][3]);
	_V[27]->Fill(RefMult, _q[1][1]*_q[2][1]*pow(_q[2][2], 2));
	_V[28]->Fill(RefMult, pow(_q[1][1], 3)*_q[2][1]*_q[3][1]);
	_V[29]->Fill(RefMult, pow(_q[1][1], 3)*_q[2][2]*_q[3][2]);
	_V[30]->Fill(RefMult, pow(_q[1][1], 3)*_q[2][1]*_q[2][2]);
	_V[31]->Fill(RefMult, pow(_q[1][1], 2)*_q[3][1]*_q[3][3]);
	_V[32]->Fill(RefMult, pow(_q[1][1], 2)*_q[2][2]*_q[4][2]);
	_V[33]->Fill(RefMult, pow(_q[1][1], 2)*_q[2][1]*_q[3][2]);
	_V[34]->Fill(RefMult, pow(_q[1][1], 2)*_q[2][1]*_q[4][1]);
	_V[35]->Fill(RefMult, pow(_q[1][1], 2)*_q[2][2]*_q[4][3]);
	_V[36]->Fill(RefMult, _q[1][1]*pow(_q[2][2], 2)*_q[3][2]);
	_V[37]->Fill(RefMult, pow(_q[1][1], 2)*_q[2][2]*_q[3][2]);
	_V[38]->Fill(RefMult, pow(_q[1][1], 2)*_q[2][2]*_q[3][3]);
	_V[39]->Fill(RefMult, pow(_q[1][1], 2)*_q[2][1]*_q[2][2]);
	_V[40]->Fill(RefMult, _q[1][1]*_q[2][1]*_q[4][1]);
	_V[41]->Fill(RefMult, _q[2][1]*_q[2][2]*_q[4][2]);
	_V[42]->Fill(RefMult, _q[2][1]*_q[2][2]*_q[3][3]);
	_V[43]->Fill(RefMult, _q[1][1]*_q[2][1]*_q[3][3]);
	_V[44]->Fill(RefMult, _q[1][1]*_q[3][2]*_q[3][3]);
	_V[45]->Fill(RefMult, _q[2][1]*_q[2][2]*_q[4][3]);
	_V[46]->Fill(RefMult, _q[1][1]*_q[2][1]*_q[3][1]);
	_V[47]->Fill(RefMult, _q[1][1]*_q[2][1]*_q[4][3]);
	_V[48]->Fill(RefMult, _q[1][1]*_q[3][2]*_q[4][1]);
	_V[49]->Fill(RefMult, _q[2][1]*_q[2][2]*_q[4][4]);
	_V[50]->Fill(RefMult, _q[1][1]*_q[3][1]*_q[4][1]);
	_V[51]->Fill(RefMult, _q[1][1]*_q[3][3]*_q[4][1]);
	_V[52]->Fill(RefMult, _q[2][1]*_q[2][2]*_q[4][1]);
	_V[53]->Fill(RefMult, _q[1][1]*_q[2][1]*_q[3][2]);
	_V[54]->Fill(RefMult, _q[1][1]*_q[2][2]*_q[4][2]);
	_V[55]->Fill(RefMult, _q[1][1]*_q[2][1]*_q[4][4]);
	_V[56]->Fill(RefMult, _q[1][1]*_q[3][2]*_q[4][2]);
	_V[57]->Fill(RefMult, _q[1][1]*_q[3][1]*_q[4][2]);
	_V[58]->Fill(RefMult, _q[1][1]*_q[2][2]*_q[4][4]);
	_V[59]->Fill(RefMult, _q[1][1]*_q[2][2]*_q[3][1]);
	_V[60]->Fill(RefMult, _q[1][1]*_q[2][2]*_q[4][1]);
	_V[61]->Fill(RefMult, _q[1][1]*_q[3][1]*_q[4][4]);
	_V[62]->Fill(RefMult, _q[1][1]*_q[3][3]*_q[4][2]);
	_V[63]->Fill(RefMult, _q[2][1]*_q[2][2]*_q[3][1]);
	_V[64]->Fill(RefMult, _q[1][1]*_q[2][2]*_q[3][3]);
	_V[65]->Fill(RefMult, _q[1][1]*_q[2][2]*_q[3][2]);
	_V[66]->Fill(RefMult, _q[1][1]*_q[3][3]*_q[4][3]);
	_V[67]->Fill(RefMult, _q[1][1]*_q[2][2]*_q[4][3]);
	_V[68]->Fill(RefMult, _q[1][1]*_q[3][2]*_q[4][4]);
	_V[69]->Fill(RefMult, _q[2][1]*_q[2][2]*_q[3][2]);
	_V[70]->Fill(RefMult, _q[1][1]*_q[3][1]*_q[3][3]);
	_V[71]->Fill(RefMult, _q[1][1]*_q[3][2]*_q[4][3]);
	_V[72]->Fill(RefMult, _q[1][1]*_q[2][1]*_q[2][2]);
	_V[73]->Fill(RefMult, _q[1][1]*_q[3][3]*_q[4][4]);
	_V[74]->Fill(RefMult, _q[1][1]*_q[2][1]*_q[4][2]);
	_V[75]->Fill(RefMult, _q[1][1]*_q[3][1]*_q[4][3]);
	_V[76]->Fill(RefMult, _q[1][1]*_q[3][1]*_q[3][2]);
	_V[77]->Fill(RefMult, pow(_q[1][1], 2)*pow(_q[3][2], 2));
	_V[78]->Fill(RefMult, pow(_q[1][1], 2)*pow(_q[3][3], 2));
	_V[79]->Fill(RefMult, pow(_q[1][1], 4)*pow(_q[2][2], 2));
	_V[80]->Fill(RefMult, pow(_q[1][1], 2)*pow(_q[3][1], 2));
	_V[81]->Fill(RefMult, pow(_q[1][1], 2)*pow(_q[2][1], 2));
	_V[82]->Fill(RefMult, pow(_q[1][1], 3)*pow(_q[2][1], 2));
	_V[83]->Fill(RefMult, pow(_q[1][1], 4)*pow(_q[2][1], 2));
	_V[84]->Fill(RefMult, pow(_q[2][1], 2)*pow(_q[2][2], 2));
	_V[85]->Fill(RefMult, pow(_q[1][1], 2)*pow(_q[2][1], 3));
	_V[86]->Fill(RefMult, pow(_q[1][1], 2)*pow(_q[2][2], 2));
	_V[87]->Fill(RefMult, pow(_q[1][1], 3)*pow(_q[2][2], 2));
	_V[88]->Fill(RefMult, pow(_q[1][1], 2)*pow(_q[2][2], 3));
	_V[89]->Fill(RefMult, pow(_q[1][1], 2)*_q[3][2]);
	_V[90]->Fill(RefMult, pow(_q[1][1], 4)*_q[2][1]);
	_V[91]->Fill(RefMult, pow(_q[1][1], 4)*_q[4][3]);
	_V[92]->Fill(RefMult, pow(_q[1][1], 2)*_q[4][4]);
	_V[93]->Fill(RefMult, pow(_q[1][1], 3)*_q[3][3]);
	_V[94]->Fill(RefMult, _q[1][1]*pow(_q[2][2], 2));
	_V[95]->Fill(RefMult, pow(_q[2][2], 2)*_q[4][4]);
	_V[96]->Fill(RefMult, pow(_q[1][1], 3)*_q[4][3]);
	_V[97]->Fill(RefMult, pow(_q[2][1], 2)*_q[2][2]);
	_V[98]->Fill(RefMult, pow(_q[1][1], 4)*_q[4][4]);
	_V[99]->Fill(RefMult, pow(_q[2][1], 3)*_q[2][2]);
	_V[100]->Fill(RefMult, _q[1][1]*pow(_q[2][2], 3));
	_V[101]->Fill(RefMult, pow(_q[1][1], 6)*_q[2][2]);
	_V[102]->Fill(RefMult, pow(_q[1][1], 6)*_q[2][1]);
	_V[103]->Fill(RefMult, pow(_q[1][1], 4)*_q[3][2]);
	_V[104]->Fill(RefMult, pow(_q[1][1], 4)*_q[3][3]);
	_V[105]->Fill(RefMult, pow(_q[2][2], 2)*_q[3][1]);
	_V[106]->Fill(RefMult, pow(_q[1][1], 2)*_q[4][2]);
	_V[107]->Fill(RefMult, _q[1][1]*pow(_q[2][1], 2));
	_V[108]->Fill(RefMult, pow(_q[1][1], 4)*_q[4][2]);
	_V[109]->Fill(RefMult, pow(_q[1][1], 4)*_q[3][1]);
	_V[110]->Fill(RefMult, pow(_q[1][1], 2)*_q[4][1]);
	_V[111]->Fill(RefMult, pow(_q[2][2], 2)*_q[4][3]);
	_V[112]->Fill(RefMult, pow(_q[1][1], 3)*_q[4][2]);
	_V[113]->Fill(RefMult, pow(_q[2][1], 2)*_q[3][3]);
	_V[114]->Fill(RefMult, pow(_q[1][1], 5)*_q[3][2]);
	_V[115]->Fill(RefMult, pow(_q[1][1], 2)*_q[4][3]);
	_V[116]->Fill(RefMult, pow(_q[1][1], 4)*_q[2][2]);
	_V[117]->Fill(RefMult, pow(_q[2][1], 2)*_q[4][2]);
	_V[118]->Fill(RefMult, pow(_q[2][1], 2)*_q[3][1]);
	_V[119]->Fill(RefMult, pow(_q[2][1], 2)*_q[3][2]);
	_V[120]->Fill(RefMult, pow(_q[1][1], 5)*_q[2][1]);
	_V[121]->Fill(RefMult, pow(_q[1][1], 5)*_q[2][2]);
	_V[122]->Fill(RefMult, _q[2][1]*pow(_q[2][2], 3));
	_V[123]->Fill(RefMult, pow(_q[2][2], 2)*_q[4][2]);
	_V[124]->Fill(RefMult, pow(_q[2][2], 2)*_q[3][2]);
	_V[125]->Fill(RefMult, _q[1][1]*pow(_q[3][3], 2));
	_V[126]->Fill(RefMult, pow(_q[1][1], 2)*_q[3][1]);
	_V[127]->Fill(RefMult, pow(_q[1][1], 2)*_q[3][3]);
	_V[128]->Fill(RefMult, pow(_q[2][1], 2)*_q[4][3]);
	_V[129]->Fill(RefMult, pow(_q[1][1], 3)*_q[2][2]);
	_V[130]->Fill(RefMult, pow(_q[1][1], 3)*_q[4][1]);
	_V[131]->Fill(RefMult, pow(_q[2][1], 2)*_q[4][4]);
	_V[132]->Fill(RefMult, _q[1][1]*pow(_q[3][2], 2));
	_V[133]->Fill(RefMult, _q[2][1]*pow(_q[2][2], 2));
	_V[134]->Fill(RefMult, pow(_q[1][1], 2)*_q[2][2]);
	_V[135]->Fill(RefMult, pow(_q[1][1], 5)*_q[3][3]);
	_V[136]->Fill(RefMult, _q[1][1]*pow(_q[3][1], 2));
	_V[137]->Fill(RefMult, pow(_q[1][1], 2)*_q[2][1]);
	_V[138]->Fill(RefMult, _q[1][1]*pow(_q[2][1], 3));
	_V[139]->Fill(RefMult, pow(_q[2][2], 2)*_q[3][3]);
	_V[140]->Fill(RefMult, pow(_q[1][1], 3)*_q[3][1]);
	_V[141]->Fill(RefMult, pow(_q[1][1], 4)*_q[4][1]);
	_V[142]->Fill(RefMult, pow(_q[1][1], 5)*_q[3][1]);
	_V[143]->Fill(RefMult, pow(_q[2][1], 2)*_q[4][1]);
	_V[144]->Fill(RefMult, pow(_q[2][2], 2)*_q[4][1]);
	_V[145]->Fill(RefMult, pow(_q[1][1], 3)*_q[2][1]);
	_V[146]->Fill(RefMult, pow(_q[1][1], 3)*_q[4][4]);
	_V[147]->Fill(RefMult, pow(_q[1][1], 3)*_q[3][2]);
	_V[148]->Fill(RefMult, _q[3][3]*_q[4][4]);
	_V[149]->Fill(RefMult, _q[3][1]*_q[4][2]);
	_V[150]->Fill(RefMult, _q[3][3]*_q[4][2]);
	_V[151]->Fill(RefMult, _q[4][3]*_q[4][4]);
	_V[152]->Fill(RefMult, _q[1][1]*_q[3][1]);
	_V[153]->Fill(RefMult, _q[2][2]*_q[4][1]);
	_V[154]->Fill(RefMult, _q[3][2]*_q[4][3]);
	_V[155]->Fill(RefMult, _q[2][1]*_q[4][3]);
	_V[156]->Fill(RefMult, _q[3][3]*_q[4][3]);
	_V[157]->Fill(RefMult, _q[3][1]*_q[3][3]);
	_V[158]->Fill(RefMult, _q[2][2]*_q[4][3]);
	_V[159]->Fill(RefMult, _q[2][2]*_q[3][2]);
	_V[160]->Fill(RefMult, _q[2][1]*_q[4][1]);
	_V[161]->Fill(RefMult, _q[1][1]*_q[2][1]);
	_V[162]->Fill(RefMult, _q[2][2]*_q[3][3]);
	_V[163]->Fill(RefMult, _q[1][1]*_q[3][3]);
	_V[164]->Fill(RefMult, _q[4][2]*_q[4][3]);
	_V[165]->Fill(RefMult, _q[4][2]*_q[4][4]);
	_V[166]->Fill(RefMult, _q[3][1]*_q[4][3]);
	_V[167]->Fill(RefMult, _q[2][1]*_q[4][2]);
	_V[168]->Fill(RefMult, _q[3][1]*_q[4][1]);
	_V[169]->Fill(RefMult, _q[2][1]*_q[2][2]);
	_V[170]->Fill(RefMult, _q[3][1]*_q[4][4]);
	_V[171]->Fill(RefMult, _q[2][1]*_q[3][1]);
	_V[172]->Fill(RefMult, _q[2][1]*_q[3][3]);
	_V[173]->Fill(RefMult, _q[2][1]*_q[4][4]);
	_V[174]->Fill(RefMult, _q[1][1]*_q[2][2]);
	_V[175]->Fill(RefMult, _q[3][3]*_q[4][1]);
	_V[176]->Fill(RefMult, _q[1][1]*_q[4][1]);
	_V[177]->Fill(RefMult, _q[3][1]*_q[3][2]);
	_V[178]->Fill(RefMult, _q[3][2]*_q[4][2]);
	_V[179]->Fill(RefMult, _q[3][2]*_q[3][3]);
	_V[180]->Fill(RefMult, _q[2][2]*_q[4][2]);
	_V[181]->Fill(RefMult, _q[2][1]*_q[3][2]);
	_V[182]->Fill(RefMult, _q[4][1]*_q[4][2]);
	_V[183]->Fill(RefMult, _q[1][1]*_q[4][4]);
	_V[184]->Fill(RefMult, _q[3][2]*_q[4][1]);
	_V[185]->Fill(RefMult, _q[1][1]*_q[3][2]);
	_V[186]->Fill(RefMult, _q[1][1]*_q[4][2]);
	_V[187]->Fill(RefMult, _q[1][1]*_q[4][3]);
	_V[188]->Fill(RefMult, _q[2][2]*_q[3][1]);
	_V[189]->Fill(RefMult, _q[2][2]*_q[4][4]);
	_V[190]->Fill(RefMult, _q[3][2]*_q[4][4]);
	_V[191]->Fill(RefMult, _q[4][1]*_q[4][3]);
	_V[192]->Fill(RefMult, _q[4][1]*_q[4][4]);
	_V[193]->Fill(RefMult, pow(_q[1][1], 4));
	_V[194]->Fill(RefMult, pow(_q[2][2], 3));
	_V[195]->Fill(RefMult, pow(_q[1][1], 8));
	_V[196]->Fill(RefMult, pow(_q[1][1], 6));
	_V[197]->Fill(RefMult, pow(_q[3][3], 2));
	_V[198]->Fill(RefMult, pow(_q[2][2], 2));
	_V[199]->Fill(RefMult, pow(_q[2][1], 4));
	_V[200]->Fill(RefMult, pow(_q[4][2], 2));
	_V[201]->Fill(RefMult, pow(_q[4][4], 2));
	_V[202]->Fill(RefMult, pow(_q[1][1], 3));
	_V[203]->Fill(RefMult, pow(_q[1][1], 7));
	_V[204]->Fill(RefMult, pow(_q[3][1], 2));
	_V[205]->Fill(RefMult, pow(_q[2][2], 4));
	_V[206]->Fill(RefMult, pow(_q[2][1], 3));
	_V[207]->Fill(RefMult, pow(_q[1][1], 5));
	_V[208]->Fill(RefMult, pow(_q[1][1], 2));
	_V[209]->Fill(RefMult, pow(_q[4][3], 2));
	_V[210]->Fill(RefMult, pow(_q[2][1], 2));
	_V[211]->Fill(RefMult, pow(_q[4][1], 2));
	_V[212]->Fill(RefMult, pow(_q[3][2], 2));
	_V[213]->Fill(RefMult, _q[4][4]);
	_V[214]->Fill(RefMult, _q[3][3]);
	_V[215]->Fill(RefMult, _q[3][2]);
	_V[216]->Fill(RefMult, _q[4][2]);
	_V[217]->Fill(RefMult, _q[4][1]);
	_V[218]->Fill(RefMult, _q[3][1]);
	_V[219]->Fill(RefMult, _q[1][1]);
	_V[220]->Fill(RefMult, _q[2][2]);
	_V[221]->Fill(RefMult, _q[2][1]);
	_V[222]->Fill(RefMult, _q[4][3]);

	// p+pbar
	_V[223]->Fill(RefMult, ppb);

	// reset
	for(int r=1;r<=4; ++r){
		for(int s=1; s<=r; ++s){
		_q[r][s] = 0;
		}
	}
	ppb = 0;

}



