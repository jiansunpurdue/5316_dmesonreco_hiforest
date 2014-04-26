# ======================================================================
# NOTE: make all
# -----
#
# ======================================================================


ifdef ROOTSYS
  ROOTCINT      = $(ROOTSYS)/bin/rootcint
  ROOTCFLAGS    = $(shell $(ROOTSYS)/bin/root-config --cflags)
  ROOTLIBS      = $(shell $(ROOTSYS)/bin/root-config --libs)
  ROOTGLIBS     = $(shell $(ROOTSYS)/bin/root-config --glibs)
else 
  ROOTCINT      = rootcint
  ROOTCFLAGS    = $(shell root-config --cflags)
  ROOTLIBS      = $(shell root-config --libs)
  ROOTGLIBS     = $(shell root-config --glibs)
endif

ifdef SCRAM_ARCH
  CXX         := $(shell scramv1 tool info gcc-cxxcompiler | grep CXX= | sed s/CXX=//)
else 
  ifdef CXXCOMPILER
    CXX         := $(CXXCOMPILER)
  else 
    CXX         := c++
  endif
endif

CXXFLAGS      = -g -Os -Wall -fPIC -pipe
LD            = $(CXX)
LDFLAGS       = -g
SOFLAGS       = -shared

CXXFLAGS     += $(ROOTCFLAGS)
LIBS          = $(ROOTLIBS)
#GLIBS         = $(ROOTGLIBS)
GLIBS         = $(filter-out -lz, $(ROOTGLIBS))

#########
# FILES #
#########

#used by all targets
ROOTIO_HEADERS = TAnaCand.hh TAnaVertex.hh TAna01Event.hh TAnaTrack.hh hfcand.hh hfcand_v0.hh snglhfcand.hh snglhfcand_v0.hh candAna.hh mapRunLumiHfTreeFile.hh map_info.hh

# Ana00 compilation
ANA00 = TAnaCand.o TAnaVertex.o TAna01Event.o TAnaTrack.o hfcand.o hfcand_v0.o snglhfcand.o snglhfcand_v0.o candAna.o mapRunLumiHfTreeFile.o map_info.o
ANA00_DICT = ${ANA00:.o=Dict.o}

#################
# PATTERN RULES #
#################

# Default rule compiling c++ files
obj/%.o : %.cc $(addprefix ,$(ROOTIO_HEADERS))
	$(CXX) $(CXXFLAGS) -I. -c $< -o $@

obj/%.o : tnp/%.cc $(addprefix tnp/,$(TNP_HEADERS))
	$(CXX) $(CXXFLAGS) -I. -c $< -o $@

# Default rules creating dictionaries
%Dict.cc : %.hh %LinkDef.h
	$(ROOTCINT) -f $@ -c $^

%Dict.cc : %.hh
	$(ROOTCINT) -f $@ -c $<

tnp/%Dict.cc : tnp/%.hh tnp/%LinkDef.h
	$(ROOTCINT) -f $@ -c $^

tnp/%Dict.cc : tnp/%.hh
	$(ROOTCINT) -f $@ -c $<


###########
# TARGETS #
###########

all: ana00 links
	@true

#short
ana00: lib/libAna00.so
	@true

lib/libAna00.so: $(addprefix obj/, $(ANA00) $(ANA00_DICT))
	$(CXX) $(SOFLAGS) $(GLIBS) $(addprefix obj/,$(ANA00) $(ANA00_DICT)) -o lib/libAna00.so


# ================================================================================
links:
	mkdir -p ../../../../lib/$(SCRAM_ARCH)
	cd ../../../../lib/$(SCRAM_ARCH)/ && rm -f libAna00.so && ln -s ../../src/UserCode/OpenHF/data_format/lib/libAna00.so && cd -

copy:
	cd ../../../../lib/$(SCRAM_ARCH)/ && rm -f libAna00.so && cp ../../src/UserCode/OpenHF/data_format/lib/libAna00.so . && cd -

# ================================================================================
clean:
	rm -f obj/*.o *Dict.* test/*Dict.* tnp/*Dict.* lib/libAna00.so 

# --------------------------------------------------------------------------------
cleanall:
	@$(MAKE) clean
	rm -f lib/lib*.so
	rm -f ../../../../lib/$(SCRAM_ARCH)/libAna00.so
