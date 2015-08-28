CXXFLAGS?=-std=c++11 -g -I.. -O1

ifdef MULTIPRECISION_DIGITS10
  CXXFLAGS+=-DMULTIPRECISION_DIGITS10=$(MULTIPRECISION_DIGITS10)
else
  # _GLIBCXX_DEBUG caused errors with boost::multiprecision::exp(...)
  CXXFLAGS+=-D_GLIBCXX_DEBUG
endif
CXXFLAGS+=$(EXTRA_FLAGS)
test: test_bateman
	./$<

clean:
	rm test_bateman

.PHONY: test clean

test_bateman: test_bateman.cpp ../bateman.hpp
	$(CXX) $(CXXFLAGS) -o $@ $<
