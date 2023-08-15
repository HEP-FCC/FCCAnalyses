#ifndef EDM4HEP_DATASOURCE_H__
#define EDM4HEP_DATASOURCE_H__

// STL
#include <memory>
#include <vector>
#include <string>
#include <functional>

// ROOT
#include <ROOT/RDataFrame.hxx>
#include <ROOT/RDataSource.hxx>

// Podio
#include <podio/Frame.h>
#include <podio/ROOTFrameReader.h>
#include <podio/CollectionBase.h>

bool loadEDM4hepDataSource();

namespace FCCAnalyses {
  using Record_t = std::vector<void*>;

  class EDM4hepDataSource final : public ROOT::RDF::RDataSource {
    public:
      EDM4hepDataSource(const std::string& filePath, int nEvents = -1);
      EDM4hepDataSource(const std::vector<std::string>& filePathList,
                        int nEvents = -1);

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
      std::vector<std::string> m_filePathList;
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
      /// Root podio readers
      std::vector<std::unique_ptr<podio::ROOTFrameReader>> m_podioReaders;
      /// Podio frames
      std::vector<std::unique_ptr<podio::Frame>> m_frames;
      /// Setup input
      void SetupInput(int nEvents);
  };


  /**
   * \brief Retrieve from EDM4hepDataSource per-thread readers for the
   *        desired columns.
   */
  template<typename T>
  std::vector<T**>
  EDM4hepDataSource::GetColumnReaders(std::string_view columnName) {
    std::cout << "EDM4hepDataSource: Getting column readers for column: "
              << columnName << std::endl;

    std::vector<T**> readers;

    return readers;
  }

  ROOT::RDataFrame FromEDM4hep(const std::vector<std::string>& filePathList);
}

#endif /* EDM4HEP_DATASOURCE_H__ */
