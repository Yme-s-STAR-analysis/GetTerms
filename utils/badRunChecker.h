#include <unordered_map>
#include <fstream>
#include <string>
#include "TMath.h"

using std::ifstream;
using std::string;
using std::unordered_map;

class BadRunChecker{
    private:
        unordered_map<Int_t, Int_t> runList;
        
    public:
        BadRunChecker(const char* badList){
            ifstream fin;
            fin.open(badList);
            string tmp;
            while(getline(fin, tmp)){
                runList[std::stoi(tmp)] = 1;
            }
            fin.close();
        }
        ~BadRunChecker(){}

        bool isBadRun(Int_t runid){
            return runList[runid];
        }
};