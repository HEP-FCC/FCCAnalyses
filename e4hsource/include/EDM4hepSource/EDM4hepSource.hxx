#ifndef EDM4HEP_SOURCE_H__
#define EDM4HEP_SOURCE_H__

// STL
#include <vector>
#include <string>
#include <functional>
#include <mutex>

// ROOT
#include <ROOT/RDataSource.hxx>

// Podio
#include <podio/Frame.h>
#include <podio/ROOTFrameReader.h>
#include <podio/CollectionBase.h>

bool loadEDM4hepSource();

namespace FCCAnalyses {
  using Record_t = std::vector<void*>;

  class EDM4hepSource final : public ROOT::RDF::RDataSource {
    public:
      EDM4hepSource(std::string_view fileName, int nEvents = -1);

      void SetNSlots(unsigned int nSlots);

      template<typename T>
      std::vector<T**> GetColumnReaders(std::string_view columnName);

      void Initialize();

      std::vector<std::pair<ULong64_t, ULong64_t>> GetEntryRanges();

      void InitSlot(unsigned int slot, ULong64_t firstEntry);

      bool SetEntry(unsigned int slot, ULong64_t entry);

      void FinalizeSlot(unsigned int slot);

      void Finalize();

      const std::vector<std::string>& GetColumnNames() const;

      bool HasColumn(std::string_view columnName) const;

      std::string GetTypeName(std::string_view columnName) const;

    protected:
      Record_t GetColumnReadersImpl (std::string_view name,
                                     const std::type_info& typeInfo);

      std::string AsString() { return "Edm4hep data source"; };

    private:
      /// Number of slots/threads
      unsigned int m_nSlots;
      /// Input filename
      std::string m_fileName;
      /// Total number of events
      unsigned int m_nEvents;
      /// Ranges of events available to be processed
      std::vector<std::pair<ULong64_t, ULong64_t>> m_rangesAvailable;
      /// Ranges of events available ever created
      std::vector<std::pair<ULong64_t, ULong64_t>> m_rangesAll;
      /// Column names
      std::vector<std::string> m_columnNames;
      /// Column types
      std::vector<std::string> m_columnTypes;
      /// Collections, m_Collections[columnIndex][slotIndex]
      std::vector<std::vector<const podio::CollectionBase*>> m_Collections;
      /// Active collections
      std::vector<unsigned int> m_activeCollections;
      /// Root podio reader
      std::map<int, podio::ROOTFrameReader> m_podioReaders;
      /// Podio frames
      std::map<int, podio::Frame> m_frames;
  };


  /**
   * \brief Retrieve from EDM4hepSource per-thread readers for the desired columns.
   */
  template<typename T>
  std::vector<T**>
  EDM4hepSource::GetColumnReaders(std::string_view columnName) {
    std::cout << "EDM4hepSource: Getting column readers for column: " << columnName << std::endl;

    std::vector<T**> readers;

    return readers;
  }
}

#endif /* EDM4HEP_SOURCE_H__ */
