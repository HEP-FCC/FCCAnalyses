Basic examples
=============

write here basic examples..

Table of contents
=================
  * [RootDataFrame](#rootdataframe)
  * [Writing your own function](#writing-your-own-function)
    *[Inline](#inline)
    *[Using ROOT GInterpreter](#using-root-ginterpreter)
    *[Writing your own class](#writing-your-own-class)
  * [Base collection](#base-collection)
 

<!--
======================================================

GUIDELINES and REQUEST  for new instructions to be added 


FACT: The general newcomer planning to do a  "case study" needs first to have instruction about how to unpack the variable he/she needs from the EDM4HEP into the flat ntuple. 
Very likely he/she has no idea about what the analysis will look like yet.  

More details about how this can be organizes: 

-- introduce links to  the manual for the "data frame" framework from root. 
Since there is a large amount of information and it is easy to get lost please add pointers to specific pages/examples. 

-- have simple examples on how to extract the variables from the edm4hep and add them to the branch in the analysis.py routine: 
    * in the case of a simple basic objects (i.e. jets, electrons, muons...) 
    * in the case of derived objects that need to be calculated: like jet pt
    * where do we find the functions needed already available for a specific object 

-- where in the code do we add NEW functions to obtain new variables/corrections  to be used in analysis.py to create our variables 
    * for instance a recent one: vertexing and new vertices information 
    * invariant masses 
    * etc ...
-- some of this exist but it is buried in the different places, I would suggest to streamlined it in a "fake" example that contains a bit of everything in the same place. 

-- explain more clearly the interplay of the "analysis.py" code and the "FinalSel.py" code in terms of the possibility of having 
calculations done in one or the other. With a couple of concrete examples. 

-- explain which files need to be modified, in case someone wants to use a personal "source file" not in the official repository.  
      * For example, you may need some code that is not generic at all, but very just used by your analysis. 
      So, instead of polluting the existing files MCParticle.cc etc, you may want to
      put this code into some MyStuff.cc.
      * explain how to compile it to use it into the analysis (add it into  the CmakeLists.txt for instance. Not obvious for everyone)

-->