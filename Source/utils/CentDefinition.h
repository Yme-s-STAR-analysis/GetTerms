#ifndef __CENTDEFCLASS__
#define __CENTDEFCLASS__

class CentDefinition {

    private:
        static const int nCent = 9;
        int edge[nCent];
        bool set;

    public:
        CentDefinition();
        ~CentDefinition(){}

        void Init(const char* path);
        int GetCentrality(int mult);
};

#endif