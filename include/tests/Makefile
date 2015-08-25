CXXFLAGS?=-std=c++11 -g -I.. -Wall -I~/urania_tmp/boost_1_59_0

ifdef MULTIPRECISION_DIGITS10
  CXXFLAGS+=-DMULTIPRECISION_DIGITS10=$(MULTIPRECISION_DIGITS10)
endif

test: test_bateman
	./$<

clean:
	rm test_bateman

.PHONY: test clean

test_baseman: test_bateman.cpp
	$(CXX) $(CXXFLAGS) -o $@ $^
