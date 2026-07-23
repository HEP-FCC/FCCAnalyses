#ifndef DEFINITIONS_H
#define DEFINITIONS_H

// podio::DataSource reconstructs the logical EDM4hep EventHeader collection
// from the split ROOT branches. This header defines the input type:
// edm4hep::EventHeaderCollection
#include "edm4hep/EventHeaderCollection.h"

// This header defines ROOT::VecOps::RVec,
// which we will use as the variable-length array of double weights.
#include <ROOT/RVec.hxx>

#include <string>
#include "podio/Reader.h"
#include <vector>

//input: EventHeader
//output: weights array
// However, eventheader is split across branches and the weights array is in : "_EventHeader_weights"
//its type: ROOT::VecOps::RVec<double> and I cannot use that as an input, so ->


// This is because eventheader data has a fixed size and cannot hold variable length arrays.
//eventheader column type: ROOT::VecOps::RVec<edm4hep::EventHeaderData>

// Enabling podio::DataSource reconstructs the logical
// edm4hep::EventHeaderCollection from the split ROOT branches.
//
// Therefore:
// input type  = edm4hep::EventHeaderCollection
// output type = ROOT::VecOps::RVec<double> 
// which is array of double values (weights) 




//functor 1 : GetAllWeights

struct GetAllWeights {
    //return type: (array of double values (weights) )
    ROOT::VecOps::RVec<double>



    // creating the function:
    //operator() makes struct behave like a function
    // first paranthesis is the input, (input type)
    // const inside the paranthesis means -> 
    // const inside the paranthesis means -> This function may read eventHeaders, but it may not modify it.
    // const{ } specifies that calling this functor will not modify the functor object itself: (functor object is defined while calling the functor ex: GetAllWeights A; -> A is the object)
    operator()(const edm4hep::EventHeaderCollection& eventHeaders)const{
        //to prevent errors when trying to reach the elements, if empty -> error
        // to prevent errors when trying to reach the elements, if empty -> error
        if (eventHeaders.empty()) {
            return {};
        }
            
        //from the event header collection for an event we need to take the event header. 
        // With podio::DataSource, EventHeader becomes an edm4hep::EventHeaderCollection; EDM4hep stores objects in collections by default, even if there is normally only one EventHeader per event.
    
        const auto& eventHeader = eventHeaders.at(0);
        //eventHeaders.at(0) -> gets the first element (event header is the only object in the collection, so first element is the header for the current event.)
        //const since
        // auto lets C++ use the type returned by eventHeaders.at(0).
    

        // Create an empty array where the event weights will be stored.
        ROOT::VecOps::RVec<double> weights;
        //output type = ROOT::VecOps::RVec<double>      (a variable-length array whose elements are doubles) (weights -> variable name)

        //Now we need to extract the weights from the single eventHeader
        const auto eventWeights = eventHeader.getWeights();
        //// getWeights() is an EDM4hep function that gets all weights stored in this EventHeader.


        //Now copy each value from eventWeights into the output array weights




        for (const auto weight : eventWeights) {
            // Automatically iterates over all elements without needing the array/vector size.
            //For each iteration, the current value is temporarily called weight 
            
            weights.push_back(weight);
            //push_back() adds the current weight in the iteration to the end of the weights output array.
        }

        return weights;
    }

};





// FUNCTOR 2 : GetWeightByName
//
//Finds a weight by name and returns its value for each event, or -1 if unavailable.
// Finds the weight's index by name once, since the index is the same for all events, then returns that weight's value for each event.

// Setup inputs (asked once):
// requested weight name: std::string
// input file path: std::string

//// Event input: event header
// edm4hep::EventHeaderCollection

// Output:
// double value or -1.0 if unavailable


// Create one GetWeightByName object and find the requested label's index once. -> GetWeightByName selectedWeight("rwgt_4", inputFile);
// Then call the same object for each event to return that event's selected weight. -> selectedWeight(EventHeader);

// evetheader is passed for each event, and the functor returns the weight value for that event.

struct GetWeightByName {

    // create a variable to store the index of the requested label
    // -1 means not found, so if the weight is not found, the functor will return -1 for each event.
    int weightIndex{-1};

    //creating a constructor (sets up the object for the struct when it's created) - must be the same name as the struct [ex:GetWeightByName A ("label", input file) -> A is the object]
    // We specifically need a constructor because Functor 2 must remember setup information -> requested label and its index
    //Without a constructor, the functor would have to search the label list every time operator() runs and operator() is called once for every event

    GetWeightByName(

        //inputs to the constructor: input file to find the labels, and the requested label to find its index
        //constructor runs whenever a new GetWeightByName object is created
        const std::string& requestedWeightName,
        // type of the file is string since inputFile is not the file’s contents. It is the path/name used to locate the file. Then PODIO uses that string path to open the actual EDM4hep ROOT file
        const std::string& inputFile)
    {
        // Create the appropriate PODIO reader for the input file format.
        // Reader implementation:
        // https://github.com/AIDASoft/podio/blob/master/src/Reader.cc
        //
        // reader is a PODIO object that opens the input file
        // and allows us to read its PODIO frames.
        // In this project, those frames contain EDM4hep data,
        // including the weight labels we want to find.
        auto reader = podio::makeReader(inputFile);


        // Use the reader for the opened input file, select the "metadata" frame category,

        // and read entry 0, which is the first and only metadata entry and contains the weight labels.

        auto metadataFrame = reader.readFrame("metadata", 0);
        //podio::Frame readFrame(std::string_view name, size_t index, const std::vector<std::string>& collsToRead = {}
        // @param name The category name = "metadata"
        // @param index The entry number to read -> podio-dump showed metadata 1 so its index is 0
        // metadataFrame holds the file’s first metadata frame, which contains the EventWeightNames parameter.



        //get the list of labels from metadataFrame
        auto weightNames =
             metadataFrame.getParameter<std::vector<std::string>>("EventWeightNames");
        // Extract the EventWeightNames parameter from metadataFrame as an optional vector of strings and store it in weightNames.     
        //PODIO’s getParameter() function returns an optional because the metadata parameter "EventWeightNames" might not exist,
        // so auto determines weightnames to have the type std::optional<std::vector<std::string>>.  


            // Loop through all weight names, compare each one with the requested name, and store its index when a match is found.
            //std::size_t is an unsigned integer type
                               

     //we cannot do .size or [i] on an optional so 
     //first check weight Names has a vector inside
     if (!weightNames.has_value()) {
        return;
    }
    //then access the vector inside the optional
    for (std::size_t i = 0; i < weightNames->size(); ++i) {
        if ((*weightNames)[i] == requestedWeightName) {
            weightIndex = static_cast<int>(i);
            break;
        }
    }


    } //constructor ends here

    //Functor operator() that will be called for each event
    // Functor 2 returns only one weight value for each event, so the return type is double.

    //input type: edm4hep::EventHeaderCollection
    //input variable name: eventHeaders 
    double operator()(const edm4hep::EventHeaderCollection& eventHeaders) const {
        //first const  → do not modify the input EventHeader collection
        //second const → do not modify the GetWeightByName object since operator() only needs to read the saved weightIndex (variable stored in GetWeightByName object), not change it
         // If there is no EventHeader for this event, there is no weight to return.
        if (eventHeaders.empty()) {
            return -1.0;
        }

        // If weightIndex is still -1, the requested label was not found.
        if (weightIndex < 0) {
            return -1.0;
        }
        //getting the eventheader from the eventheaders collection (one event header per event so index 0)
        const auto& eventHeader = eventHeaders.at(0);
         //Now we need to extract the weights from the single eventHeader
        const auto eventWeights = eventHeader.getWeights();
        // getWeights() is an EDM4hep function that gets all weights stored in this EventHeader.
        

        // Convert the valid weightIndex from int to std::size_t because array positions and .size() use std::size_t, then store it in index. It was initially declared as int
        const auto index = static_cast<std::size_t>(weightIndex);


        //if the label was found, but the current event does not contain enough numerical weights then return -1.0. 
        if (index >= eventWeights.size()) {
             return -1.0;
        }
    // Return the numerical weight that corresponds to the requested label.
        return eventWeights[index];
    }
    
          
};









#endif