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
#include <vector>
#include <cstddef>

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
// For each event, uses the weight-name list supplied by the DataSource to find
// the requested label's index, then returns the numerical weight at that index.

// Setup input supplied once when the functor object is created:
// requested weight name: std::string

// Inputs supplied by RDataFrame:
// eventHeaders: edm4hep::EventHeaderCollection
// weightNames: std::vector<std::string>
//              supplied through the _EventWeightNames DataSource column

// Output:
// double value or -1.0 if unavailable


// Create one GetWeightByName object and store the requested weight label.
// -> GetWeightByName selectedWeight("rwgt_4");                                                                            
                                                                            //object name: selectedweight
                                                                            //object type: GetWeightByName
                                                                            // selected weight's label: "rwgt_4"
                                                                            // The requested label "rwgt_4" is stored in the selectedWeight object.
                                                                            // The input file is not opened or accessed by this functor.
                                                                            // RDataFrame calls the object's operator() using the EventHeader collection
                                                                            // and the _EventWeightNames metadata column.
                                                                            // Conceptually, RDataFrame calls:
                                                                            // selectedWeight(EventHeader, _EventWeightNames);
                                                                            //
                                                                            // Here, EventHeader and _EventWeightNames are RDataFrame column names.
                                                                            // The EventHeader is supplied for each event, while _EventWeightNames supplies
                                                                            // the labels used to identify the requested numerical weight.
struct GetWeightByName {

    // Store the name of the requested weight.
    // For example, requestedWeightName may contain "rwgt_4".
    std::string requestedWeightName;
    // Constructor: runs when a GetWeightByName object is created.
    // It stores the requested label inside the object.
    // Example: GetWeightByName selectedWeight("rwgt_4");

    // The constructor allows the functor object to remember which label was requested.
    //The constructor defines what happens to that supplied value (requestedWeightName)
    // It stores the label, but it does not open the file or read metadata.
    GetWeightByName(const std::string& weightName)
        : requestedWeightName(weightName) {
    }   
    // operator() receives the label list from the DataSource and uses it to locate
    // the stored requestedWeightName.

    //Functor operator() that will be called for each event
    // Functor 2 returns only one weight value for each event, so the return type is double.

    // First input:
    // type: edm4hep::EventHeaderCollection
    // variable name: eventHeaders
    //
    // Second input:
    // type: std::vector<std::string>
    // variable name: weightNames
    double operator()(
        const edm4hep::EventHeaderCollection& eventHeaders,
        const std::vector<std::string>& weightNames
    ) const {
        // The const before each input type means operator() may read eventHeaders
        // and weightNames, but it may not modify either of them.
        // The final const means operator() does not modify the GetWeightByName object.
        // It only reads the stored requestedWeightName.
        // If there is no EventHeader for this event, there is no weight to return.
        if (eventHeaders.empty()) {
            return -1.0;
        }

        // Create a local variable to store the index of the requested label.
        // -1 means that the requested label has not been found.
        int weightIndex{-1};

        // Loop through all weight labels supplied by the DataSource.
        //
        // std::size_t is the unsigned integer type normally used for
        // vector sizes and vector positions.
        for (std::size_t i = 0; i < weightNames.size(); ++i) {

            // Compare the current label with the label stored in the functor object.
            if (weightNames[i] == requestedWeightName) {

                // Save the matching label's position.
                // This same position identifies the corresponding numerical weight
                // inside EventHeader.getWeights().
                weightIndex = static_cast<int>(i);

                // The requested label has been found, so the loop can stop.
                break;
            }
        }

        // If weightIndex is still -1 after the loop,
        // the requested label was not present in weightNames.
        if (weightIndex < 0) {
            return -1.0;
        }
        
        // Get the EventHeader from the EventHeader collection.
        // There is normally one EventHeader object per event, so its index is 0.
        const auto& eventHeader = eventHeaders.at(0);
        // Extract all numerical weights from this event's EventHeader.
        const auto eventWeights = eventHeader.getWeights();
        // getWeights() is an EDM4hep function that gets all weights stored in this EventHeader.
        

        // Convert the valid weightIndex from int to std::size_t because array positions and .size() use std::size_t, then store it in index. It was initially declared as int
        const auto index = static_cast<std::size_t>(weightIndex);


        // The label may exist, but the current event may contain fewer numerical
        // weights than expected. In that case, the index would be invalid.
        if (index >= eventWeights.size()) {
             return -1.0;
        }
        // Return the numerical event weight at the same index as the requested label.
        return eventWeights[index];
    }
    
          
};









#endif