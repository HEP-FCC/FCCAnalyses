#include "FCCAnalyses/EventFilter.h"
// Standard library
#include <iostream>

namespace FCCAnalyses ::EventFilter {
// ----------------------------------------------------------------------------
stride::stride(const ULong64_t stride) : m_stride(stride) {}

bool
stride::operator()(const ULong64_t rdfEntry) {
  return rdfEntry % m_stride == 0;
}

// ----------------------------------------------------------------------------
nEvents::nEvents(const ULong64_t nEventsMax) : m_nEventsMax(nEventsMax) {}

std::atomic<ULong64_t> nEvents::m_nEventsSeen = 0;

bool
nEvents::operator()() {
  ++m_nEventsSeen;
  return m_nEventsSeen <= m_nEventsMax;
}

} // namespace FCCAnalyses ::EventFilter
