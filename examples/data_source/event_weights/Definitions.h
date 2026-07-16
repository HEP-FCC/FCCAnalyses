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
// available weight names: std::vector<std::string>

//// Event input: event header
// edm4hep::EventHeaderCollection

// Output:
// double value or -1.0 if unavailable
            //GetWeightByName("PDF_12")(EventHeader)
            //"PDF_12" configures the functor once.
            //EventHeader is passed for each event.

struct GetWeightByName {

    


};








#endif




