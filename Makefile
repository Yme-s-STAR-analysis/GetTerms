EXTRA_CPPFLAG=

all: compile

mdict:
	rootcint dict.cxx utils/StFemtoEvent.h utils/StFemtoTrack.h

compile: clean mdict
	g++ -o getTerms -std=c++11 dict.cxx utils/Loader.cxx utils/QualityController.cxx utils/StFemtoEvent.cxx utils/StFemtoTrack.cxx utils/EffMaker.cxx utils/CentCorrTool.cxx Core.cxx `root-config --libs --cflags` $(EXTRA_CPPFLAG)

clean:
	touch getTerms
	touch dictTmp
	rm dict* 
	rm getTerms
