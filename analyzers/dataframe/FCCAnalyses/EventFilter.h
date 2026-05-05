#ifndef ANALYZERS_EVENT_FILTER_H
#define ANALYZERS_EVENT_FILTER_H

// ROOT
#include "Rtypes.h"

namespace FCCAnalyses ::EventFilter {
  /**
   * @brief Filters events based on their entry number with modulo operation.
   */
  struct stride {
  public:
    explicit stride(const ULong64_t stride);
    bool operator()(const ULong64_t rdfEntry);

  private:
    const ULong64_t m_stride;
  };

  /**
   * @brief Thread safe accumulation based filter on number of events.
   */
  struct nEvents {
  public:
    explicit nEvents(const ULong64_t nEventsMax);
    bool operator()();

  private:
    const ULong64_t m_nEventsMax;
    static std::atomic<ULong64_t> m_nEventsSeen;
  };

} // namespace FCCAnalyses ::EventFilter

#endif /* ANALYZERS_EVENT_FILTER_H */
