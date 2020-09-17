g++ -c -fPIC mt2.cpp -o mt2.o
g++ -shared -Wl,-soname,libmt2.so -o libmt2.so  mt2.o


