// Yige Huang -- 30.01.2024 update
//Zhang Yu -- Dec 2020
#include "TProfile.h"
#include "TH1D.h"
#include "TFile.h"
#include "LoaderHomo.h"

Loader::Loader(const char* type, TFile* tf, int MaxMult) : ParticleType(type), _nMultBin(MaxMult+1) {
	for(int r=1;r<=3;++r) {
		for(int s=1; s<=r;++s) {
			_q[r][s] = 0;
		}
  	}
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
  	for(int r=1;r<=3; ++r){
		for(int s=1; s<=r; ++s) {
	  		_q[r][s] += (pow(Particle,r)/pow(eff, s));
		}
  	}
}

void Loader::Store(int RefMult) {

	_V[1]->Fill(RefMult, _q[1][1]*_q[3][3]);
	_V[2]->Fill(RefMult, _q[1][1]*_q[2][2]*_q[3][1]);
	_V[3]->Fill(RefMult, pow(_q[1][1], 3)*_q[3][3]);
	_V[4]->Fill(RefMult, _q[2][1]*_q[3][1]);
	_V[5]->Fill(RefMult, pow(_q[1][1], 4)*_q[2][1]);
	_V[6]->Fill(RefMult, pow(_q[1][1], 3));
	_V[7]->Fill(RefMult, pow(_q[1][1], 6));
	_V[8]->Fill(RefMult, _q[1][1]*pow(_q[2][1], 2));
	_V[9]->Fill(RefMult, pow(_q[1][1], 2)*_q[3][1]);
	_V[10]->Fill(RefMult, _q[2][1]);
	_V[11]->Fill(RefMult, _q[2][2]*_q[3][2]);
	_V[12]->Fill(RefMult, pow(_q[1][1], 3)*_q[2][2]);
	_V[13]->Fill(RefMult, _q[3][1]);
	_V[14]->Fill(RefMult, pow(_q[1][1], 2)*pow(_q[2][1], 2));
	_V[15]->Fill(RefMult, _q[3][3]);
	_V[16]->Fill(RefMult, _q[3][1]*_q[3][2]);
	_V[17]->Fill(RefMult, _q[2][1]*_q[3][3]);
	_V[18]->Fill(RefMult, pow(_q[1][1], 2)*_q[3][2]);
	_V[19]->Fill(RefMult, pow(_q[1][1], 3)*_q[3][1]);
	_V[20]->Fill(RefMult, _q[1][1]*_q[2][2]*_q[3][2]);
	_V[21]->Fill(RefMult, _q[1][1]*_q[2][1]);
	_V[22]->Fill(RefMult, _q[2][1]*_q[3][2]);
	_V[23]->Fill(RefMult, pow(_q[1][1], 4));
	_V[24]->Fill(RefMult, _q[1][1]*_q[2][1]*_q[3][2]);
	_V[25]->Fill(RefMult, pow(_q[3][1], 2));
	_V[26]->Fill(RefMult, pow(_q[1][1], 2)*_q[2][2]);
	_V[27]->Fill(RefMult, pow(_q[1][1], 5));
	_V[28]->Fill(RefMult, _q[1][1]*pow(_q[2][2], 2));
	_V[29]->Fill(RefMult, _q[3][1]*_q[3][3]);
	_V[30]->Fill(RefMult, _q[1][1]*_q[3][2]);
	_V[31]->Fill(RefMult, _q[1][1]*_q[3][1]);
	_V[32]->Fill(RefMult, _q[2][1]*_q[2][2]);
	_V[33]->Fill(RefMult, pow(_q[1][1], 4)*_q[2][2]);
	_V[34]->Fill(RefMult, pow(_q[3][3], 2));
	_V[35]->Fill(RefMult, pow(_q[2][1], 2));
	_V[36]->Fill(RefMult, _q[1][1]*_q[2][1]*_q[2][2]);
	_V[37]->Fill(RefMult, _q[3][2]);
	_V[38]->Fill(RefMult, _q[1][1]*_q[2][2]*_q[3][3]);
	_V[39]->Fill(RefMult, _q[1][1]);
	_V[40]->Fill(RefMult, pow(_q[1][1], 3)*_q[2][1]);
	_V[41]->Fill(RefMult, _q[1][1]*_q[2][2]);
	_V[42]->Fill(RefMult, _q[2][2]*_q[3][1]);
	_V[43]->Fill(RefMult, _q[1][1]*_q[2][1]*_q[3][3]);
	_V[44]->Fill(RefMult, pow(_q[1][1], 2)*_q[2][1]*_q[2][2]);
	_V[45]->Fill(RefMult, pow(_q[2][2], 2));
	_V[46]->Fill(RefMult, pow(_q[1][1], 3)*_q[3][2]);
	_V[47]->Fill(RefMult, _q[3][2]*_q[3][3]);
	_V[48]->Fill(RefMult, pow(_q[1][1], 2)*pow(_q[2][2], 2));
	_V[49]->Fill(RefMult, _q[2][2]*_q[3][3]);
	_V[50]->Fill(RefMult, pow(_q[1][1], 2)*_q[3][3]);
	_V[51]->Fill(RefMult, _q[2][2]);
	_V[52]->Fill(RefMult, pow(_q[3][2], 2));
	_V[53]->Fill(RefMult, pow(_q[1][1], 2));
	_V[54]->Fill(RefMult, pow(_q[1][1], 2)*_q[2][1]);
	_V[55]->Fill(RefMult, _q[1][1]*_q[2][1]*_q[3][1]);

	// reset
	for(int r=1;r<=3; ++r){
		for(int s=1; s<=r; ++s){
		_q[r][s] = 0;
		}
	}

}



