#include <iostream>
#include <fstream>
#include <string>

#include "CentDefinition.h"

CentDefinition::CentDefinition() {
    for (int i=0; i<nCent; i++){
        edge[i] = 0;
    }
    set = false;
}

void CentDefinition::Init(const char* path) {
    std::cout << "[LOG] - CentDefinition: Now reading centrality bin edges from " << path << std::endl;
    std::ifstream fin;
    fin.open(path);
    std::string str;
    int i = 0;
    while(std::getline(fin, str)){
        edge[i] = std::atoi(str.c_str());
        i += 1;
        if (i > nCent){
            std::cout << "[Warning] - CentDefinition: The target centrality edge is out of range " << i << " of " << nCent << ".\n";
        }
    }
    fin.close();
    set = true;
    std::cout << "[LOG] - CentDefinition: Centrality edge read: ";
    for (int i=0; i<nCent; i++){
        std::cout << edge[i];
        if (i != nCent-1){
            std::cout << ", ";
        } else {
            std::cout << ".\n";
        }
    }
}

int CentDefinition::GetCentrality(int mult) {
    if (!set) {
        std::cout << "[Warning] - GetCentrality: Haven't called Init() priory to GetCentrality()\n";
        return -1;
    }
    for (int i=0; i<nCent; i++) {
        if (mult >= edge[i]) {
            return i;
        }
    }
    return -1;
}
