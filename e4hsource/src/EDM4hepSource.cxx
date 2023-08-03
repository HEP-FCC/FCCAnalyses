#include "EDM4hepSource/EDM4hepSource.hxx"

// STL
#include <cstddef>
#include <iostream>
#include <filesystem>

// ROOT
#include <TFile.h>
#include <podio/ROOTFrameReader.h>

bool loadEDM4hepSource() {
  return true;
}

namespace FCCAnalyses {
  /**
   * \brief Construct the EDM4hepSource from the provided file.
   */
  EDM4hepSource::EDM4hepSource(std::string_view fileName,
                               int nEvents) : m_nSlots{1},
                                              m_fileName{fileName}
  {
    std::cout << "EDM4hepSource: Constructing the source ..." << std::endl;

    // Check if file exists
    if (!std::filesystem::exists(m_fileName)) {
      std::cerr << "EDM4hepSource: Provided file does not exist!" << std::endl;
    }

    // Check if the provided file contains required metadata
    TFile infile = TFile(m_fileName.data(), "READ");
    auto metadata = infile.Get("podio_metadata");
    if (!metadata) {
      std::cerr << "EDM4hepSource: Provided file is missing podio metadata!"
                << std::endl;
      return;
    }
    infile.Close();

    // Open the input file
    podio::ROOTFrameReader podioReader;
    podioReader.openFile(m_fileName);

    unsigned int nEventsFromFile = podioReader.getEntries("events");
    if (nEventsFromFile > 0) {
      std::cout << "EDM4hepSource: Found " << nEventsFromFile
                << " events in file: \n"
                << "               " << m_fileName << std::endl;
    } else {
      std::cerr << "EDM4hepSource: No events found!" << std::endl;
      return;
    }

    if (nEvents < 0) {
      m_nEvents = nEventsFromFile;
    } else if (nEvents == 0) {
      std::cerr << "EDM4hepSource: Requested to run over zero events!"
                << std::endl;
      return;
    } else {
      m_nEvents = nEvents;
    }
    if (nEventsFromFile < m_nEvents) {
      m_nEvents = nEventsFromFile;
    }

    std::cout << "EDM4hepSource: Running over " << m_nEvents << " events."
              << std::endl;

    auto frame = podio::Frame(podioReader.readEntry("events", 0));

    std::vector<std::string> collNames = frame.getAvailableCollections();
    std::cout << "EDM4hepSource: Found following collections:\n";
    for (auto& collName: collNames) {
      const podio::CollectionBase* coll = frame.get(collName);
      if (coll->isValid()) {
        m_columnNames.emplace_back(collName);
        m_columnTypes.emplace_back(coll->getValueTypeName());
        std::cout << "                - " << collName << "\n";
      }
    }
  }


  /**
   * \brief Inform the EDM4hepSource of the desired level of parallelism.
   */
  void
  EDM4hepSource::SetNSlots(unsigned int nSlots) {
    std::cout << "EDM4hepSource: Setting num. of slots to: " << nSlots << std::endl;
    m_nSlots = nSlots;

    if (m_nSlots > m_nEvents) {
      std::cerr << "EDM4hepSource: Number of events too small!" << std::endl;
      return;
    }

    int eventsPerSlot = m_nEvents / m_nSlots;
    for (size_t i = 0; i < (m_nSlots - 1); ++i) {
      m_rangesAll.emplace_back(eventsPerSlot * i, eventsPerSlot * (i + 1));
    }
    m_rangesAll.emplace_back(eventsPerSlot * (m_nSlots - 1), m_nEvents);
    m_rangesAvailable = m_rangesAll;

    // Initialize the entire set of addresses
    m_Collections.resize(
      m_columnNames.size(),
      std::vector<const podio::CollectionBase*>(m_nSlots, nullptr));

    // Initialize podio readers
    for (size_t i = 0; i < m_nSlots; ++i) {
      m_podioReaders[i].openFile(m_fileName);
    }
  }


  /**
   * \brief Inform RDataSource that an event-loop is about to start.
   */
  void
  EDM4hepSource::Initialize() {
    std::cout << "EDM4hepSource: Initializing the source ..." << std::endl;

  }


  /**
   * \brief Retrieve from EDM4hepSource a set of ranges of entries that can be
   *        processed concurrently.
   */
  std::vector<std::pair<ULong64_t, ULong64_t>>
  EDM4hepSource::GetEntryRanges() {
    std::cout << "EDM4hepSource: Getting entry ranges ..." << std::endl;

    std::vector<std::pair<ULong64_t, ULong64_t>> rangesToBeProcessed;
    for (auto& range: m_rangesAvailable) {
      rangesToBeProcessed.emplace_back(
          std::pair<ULong64_t, ULong64_t>{range.first, range.second}
      );
      if (rangesToBeProcessed.size() >= m_nSlots) {
        break;
      }
    }

    if (m_rangesAvailable.size() > m_nSlots) {
      m_rangesAvailable.erase(m_rangesAvailable.begin(),
                              m_rangesAvailable.begin() + m_nSlots);
    } else {
      m_rangesAvailable.erase(m_rangesAvailable.begin(),
                              m_rangesAvailable.end());
    }


    std::cout << "EDM4hepSource: Ranges to be processed:\n";
    for (auto& range: rangesToBeProcessed) {
      std::cout << "               {" << range.first << ", " << range.second
                << "}\n";
    }

    if (m_rangesAvailable.size() > 0) {

      std::cout << "EDM4hepSource: Ranges remaining:\n";
      for (auto& range: m_rangesAvailable) {
        std::cout << "               {" << range.first << ", " << range.second
                  << "}\n";
      }
    } else {
      std::cout << "EDM4hepSource: No more remaining ranges.\n";
    }

    return rangesToBeProcessed;
  }


  /**
   * \brief Inform EDM4hepSource that a certain thread is about to start working
   *        on a certain range of entries.
   */
  void
  EDM4hepSource::InitSlot(unsigned int slot, ULong64_t firstEntry) {
    std::cout << "EDM4hepSource: Initializing slot: " << slot
              << " with first entry " << firstEntry << std::endl;
  }


  /**
   * \brief Inform EDM4hepSource that a certain thread is about to start working
   *        on a certain entry.
   */
  bool
  EDM4hepSource::SetEntry(unsigned int slot, ULong64_t entry) {
    // std::cout << "EDM4hepSource: In slot: " << slot << ", setting entry: "
    //           << entry << std::endl;

    m_frames[slot] = podio::Frame(m_podioReaders[slot].readEntry("events", entry));
    for (auto& collectionIndex: m_activeCollections) {
      m_Collections[collectionIndex][slot] = m_frames[slot].get(m_columnNames.at(collectionIndex));
      // std::cout << "CollName: " << m_columnNames.at(collectionIndex) << "\n";
      // std::cout << "Address: " << m_Collections[collectionIndex][slot] << "\n";
      // std::cout << "Coll size: " << m_Collections[collectionIndex][slot]->size() << "\n";
      // if (m_Collections[collectionIndex][slot]->isValid()) {
      //   std::cout << "Collection valid\n";
      // }
    }

    return true;
  }


  /**
   * \brief Inform EDM4hepSource that a certain thread finished working on a
   *        certain range of entries.
   */
  void
  EDM4hepSource::FinalizeSlot(unsigned int slot) {
    std::cout << "EDM4hepSource: Finalizing slot: " << slot << std::endl;
  }


  /**
   * \brief Inform RDataSource that an event-loop finished.
   */
  void
  EDM4hepSource::Finalize() {
    std::cout << "EDM4hepSource: Finalizing ..." << std::endl;
  }


  /**
   * \brief Type-erased vector of pointers to pointers to column values --- one
   *        per slot 
   */
  Record_t
  EDM4hepSource::GetColumnReadersImpl(std::string_view columnName,
                                      const std::type_info& typeInfo) {
    std::cout << "EDM4hepSource: Getting column reader implementation for column:\n"
              << "               " << columnName
              << "\n               with type: " << typeInfo.name() << std::endl;

    auto itr = std::find(m_columnNames.begin(), m_columnNames.end(),
                         columnName);
    if (itr == m_columnNames.end()) {
      std::cerr << "EDM4hepSource: Can't find requested column" << std::endl;
    }
    auto columnIndex = std::distance(m_columnNames.begin(), itr);
    m_activeCollections.emplace_back(columnIndex);
    std::cout << "EDM4hepSource: Active collections so far:\n"
              << "               ";
    for (auto& i: m_activeCollections) {
      std::cout << i << ", ";
    }
    std::cout << std::endl;

    Record_t columnReaders(m_nSlots);
    for (size_t slotIndex = 0; slotIndex < m_nSlots; ++slotIndex) {
      // std::cout << "               Column index: " << columnIndex << "\n";
      // std::cout << "               Slot index: " << slotIndex << "\n";
      // std::cout << "               Address: "
      //         << &m_Collections[columnIndex][slotIndex]
      //         << std::endl;
      columnReaders[slotIndex] = (void*) &m_Collections[columnIndex][slotIndex];
    }

    return columnReaders;
  }


  /**
   * \brief Returns a reference to the collection of the dataset's column names 
   */
  const std::vector<std::string>&
  EDM4hepSource::GetColumnNames() const {
    std::cout << "EDM4hepSource: Looking for column names" << std::endl;

    return m_columnNames;
  }

  /**
   * \brief Checks if the dataset has a certain column.
   */
  bool
  EDM4hepSource::HasColumn(std::string_view columnName) const {
    std::cout << "EDM4hepSource: Looking for column: " << columnName
              << std::endl;

    if (std::find(m_columnNames.begin(),
                  m_columnNames.end(),
                  columnName) != m_columnNames.end()) {
      return true;
    }

    return false;
  }


  /**
   * \brief Type of a column as a string. Required for JITting.
   */
  std::string
  EDM4hepSource::GetTypeName(std::string_view columnName) const {
    std::cout << "EDM4hepSource: Looking for type name of column: "
              << columnName << std::endl;

    auto itr = std::find(m_columnNames.begin(), m_columnNames.end(),
                         columnName);
    if (itr != m_columnNames.end()) {
      auto i = std::distance(m_columnNames.begin(), itr);
      return m_columnTypes.at(i);
    }

    return "float";
  }
}
