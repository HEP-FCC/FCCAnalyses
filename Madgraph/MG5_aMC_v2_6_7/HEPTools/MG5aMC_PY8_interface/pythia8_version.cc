// This is code snippet to retrieve the Pythia8 version number.

#include "Pythia8/Pythia.h"
#include <unistd.h>

int main(int argc, char* argv[]) {
std::cout << PYTHIA_VERSION << std::endl;
return 0;
}
