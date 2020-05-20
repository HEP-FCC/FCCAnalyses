
source setup.sh
mkdir build install
cd build
cmake -DCMAKE_INSTALL_PREFIX=../install -DCMAKE_CXX_STANDARD=17 -G Ninja -DCMAKE_CXX_FLAGS=" -fdiagnostics-color=always " .. && \
    ninja -k0 && \
    ninja install
