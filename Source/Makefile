ACTHOMO3=
ACTREFMULT3=
ACTFOURTH=
ACTINTTOFEFF=

# check: is REFMULT3 activated
ifdef REFMULT3
	ACTREFMULT3=-D__REFMULT3__
endif

# check: is FOURTH activated
ifdef FOURTH
	ACTFOURTH=-D__FOURTH__
	LOADERSRC=utils/Loader4.cxx
else 
#check: is homogenous (up to 3rd order) activated
	ifdef HOMO3
		ACTHOMO3=-D__HOMO3__
		LOADERSRC=utils/LoaderHomo.cxx
	else
		LOADERSRC=utils/Loader6.cxx
	endif
endif

# check: is INTERPOLATE
ifdef INTERPOLATE
	ACTINTTOFEFF=-D__INTERPOLATE_TOF_EFF__
endif

all: compile

mdict:
	rootcint dict.cxx utils/StFemtoEvent.h utils/StFemtoTrack.h

compile: clean mdict
	g++ -o getTerms -std=c++11 dict.cxx $(LOADERSRC) utils/QualityController.cxx utils/StFemtoEvent.cxx utils/StFemtoTrack.cxx utils/EffMaker.cxx utils/CentDefinition.cxx Core.cxx `root-config --libs --cflags` $(ACTREFMULT3) $(ACTFOURTH) $(ACTHOMO3) $(ACTINTTOFEFF)

clean:
	touch getTerms
	touch dictTmp
	rm dict* 
	rm getTerms
