#ifndef LOADER_H
#define LOADER_H

class TProfile;
class TH1D;
class TFile;

//	CumLoader saves terms for cumulants calculation only.
//	Loader also saves terms for stat. error calculation.

class Loader {

  	public:
		Loader(const char*, TFile*, int);
		~Loader();
		void ReadTrack(float, float);
		void Store(int);
		// void Save(const char*);
		// void Update(const char*);

  	private:
		int _nMultBin;
		const char* ParticleType;
		int LowEventCut;
		Double_t _q[5][5];
		Double_t ppb;
		// static const Int_t _nTerms = 2535;
		static const Int_t _nTerms = 223; // add p+pbar
		TProfile* _V[_nTerms+1]; // -> _nTerms + 1
		const Char_t* Terms[_nTerms]={"q01_01q02_01q02_02q03_02", "q01_01q02_01q02_02q03_01", "q01_01q02_01q02_02q03_03", "q01_01_2q02_01_2q02_02", "q01_01_2q02_01q02_02_2", "q01_01q02_01_2q03_03", "q01_01q02_02_2q03_03", "q01_01_2q02_02q03_01", "q01_01_2q02_01q04_03", "q01_01_2q02_01q04_02", "q01_01_2q03_02q03_03", "q01_01q02_01_2q02_02", "q01_01_2q03_01q03_02", "q01_01q02_01_2q03_02", "q01_01_2q02_01q04_04", "q01_01_3q02_01q03_02", "q01_01q02_02_2q03_01", "q01_01_3q02_02q03_01", "q01_01_3q02_01q03_03", "q01_01_2q02_02q04_01", "q01_01_2q02_02q04_04", "q01_01q02_01_2q03_01", "q01_01_2q02_01q03_01", "q01_01_4q02_01q02_02", "q01_01_2q02_01q03_03", "q01_01_3q02_02q03_03", "q01_01q02_01q02_02_2", "q01_01_3q02_01q03_01", "q01_01_3q02_02q03_02", "q01_01_3q02_01q02_02", "q01_01_2q03_01q03_03", "q01_01_2q02_02q04_02", "q01_01_2q02_01q03_02", "q01_01_2q02_01q04_01", "q01_01_2q02_02q04_03", "q01_01q02_02_2q03_02", "q01_01_2q02_02q03_02", "q01_01_2q02_02q03_03", "q01_01_2q02_01q02_02", "q01_01q02_01q04_01", "q02_01q02_02q04_02", "q02_01q02_02q03_03", "q01_01q02_01q03_03", "q01_01q03_02q03_03", "q02_01q02_02q04_03", "q01_01q02_01q03_01", "q01_01q02_01q04_03", "q01_01q03_02q04_01", "q02_01q02_02q04_04", "q01_01q03_01q04_01", "q01_01q03_03q04_01", "q02_01q02_02q04_01", "q01_01q02_01q03_02", "q01_01q02_02q04_02", "q01_01q02_01q04_04", "q01_01q03_02q04_02", "q01_01q03_01q04_02", "q01_01q02_02q04_04", "q01_01q02_02q03_01", "q01_01q02_02q04_01", "q01_01q03_01q04_04", "q01_01q03_03q04_02", "q02_01q02_02q03_01", "q01_01q02_02q03_03", "q01_01q02_02q03_02", "q01_01q03_03q04_03", "q01_01q02_02q04_03", "q01_01q03_02q04_04", "q02_01q02_02q03_02", "q01_01q03_01q03_03", "q01_01q03_02q04_03", "q01_01q02_01q02_02", "q01_01q03_03q04_04", "q01_01q02_01q04_02", "q01_01q03_01q04_03", "q01_01q03_01q03_02", "q01_01_2q03_02_2", "q01_01_2q03_03_2", "q01_01_4q02_02_2", "q01_01_2q03_01_2", "q01_01_2q02_01_2", "q01_01_3q02_01_2", "q01_01_4q02_01_2", "q02_01_2q02_02_2", "q01_01_2q02_01_3", "q01_01_2q02_02_2", "q01_01_3q02_02_2", "q01_01_2q02_02_3", "q01_01_2q03_02", "q01_01_4q02_01", "q01_01_4q04_03", "q01_01_2q04_04", "q01_01_3q03_03", "q01_01q02_02_2", "q02_02_2q04_04", "q01_01_3q04_03", "q02_01_2q02_02", "q01_01_4q04_04", "q02_01_3q02_02", "q01_01q02_02_3", "q01_01_6q02_02", "q01_01_6q02_01", "q01_01_4q03_02", "q01_01_4q03_03", "q02_02_2q03_01", "q01_01_2q04_02", "q01_01q02_01_2", "q01_01_4q04_02", "q01_01_4q03_01", "q01_01_2q04_01", "q02_02_2q04_03", "q01_01_3q04_02", "q02_01_2q03_03", "q01_01_5q03_02", "q01_01_2q04_03", "q01_01_4q02_02", "q02_01_2q04_02", "q02_01_2q03_01", "q02_01_2q03_02", "q01_01_5q02_01", "q01_01_5q02_02", "q02_01q02_02_3", "q02_02_2q04_02", "q02_02_2q03_02", "q01_01q03_03_2", "q01_01_2q03_01", "q01_01_2q03_03", "q02_01_2q04_03", "q01_01_3q02_02", "q01_01_3q04_01", "q02_01_2q04_04", "q01_01q03_02_2", "q02_01q02_02_2", "q01_01_2q02_02", "q01_01_5q03_03", "q01_01q03_01_2", "q01_01_2q02_01", "q01_01q02_01_3", "q02_02_2q03_03", "q01_01_3q03_01", "q01_01_4q04_01", "q01_01_5q03_01", "q02_01_2q04_01", "q02_02_2q04_01", "q01_01_3q02_01", "q01_01_3q04_04", "q01_01_3q03_02", "q03_03q04_04", "q03_01q04_02", "q03_03q04_02", "q04_03q04_04", "q01_01q03_01", "q02_02q04_01", "q03_02q04_03", "q02_01q04_03", "q03_03q04_03", "q03_01q03_03", "q02_02q04_03", "q02_02q03_02", "q02_01q04_01", "q01_01q02_01", "q02_02q03_03", "q01_01q03_03", "q04_02q04_03", "q04_02q04_04", "q03_01q04_03", "q02_01q04_02", "q03_01q04_01", "q02_01q02_02", "q03_01q04_04", "q02_01q03_01", "q02_01q03_03", "q02_01q04_04", "q01_01q02_02", "q03_03q04_01", "q01_01q04_01", "q03_01q03_02", "q03_02q04_02", "q03_02q03_03", "q02_02q04_02", "q02_01q03_02", "q04_01q04_02", "q01_01q04_04", "q03_02q04_01", "q01_01q03_02", "q01_01q04_02", "q01_01q04_03", "q02_02q03_01", "q02_02q04_04", "q03_02q04_04", "q04_01q04_03", "q04_01q04_04", "q01_01_4", "q02_02_3", "q01_01_8", "q01_01_6", "q03_03_2", "q02_02_2", "q02_01_4", "q04_02_2", "q04_04_2", "q01_01_3", "q01_01_7", "q03_01_2", "q02_02_4", "q02_01_3", "q01_01_5", "q01_01_2", "q04_03_2", "q02_01_2", "q04_01_2", "q03_02_2", "q04_04", "q03_03", "q03_02", "q04_02", "q04_01", "q03_01", "q01_01", "q02_02", "q02_01", "q04_03", "ppb"};
};

#endif
