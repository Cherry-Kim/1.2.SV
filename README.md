# Installing Delly
https://github.com/dellytools/delly/archive/refs/tags/v1.1.6.tar.gz

# Installing manta
wget https://github.com/Illumina/manta/releases/download/v1.6.0/manta-1.6.0.release_src.tar.bz2
tar -xjf manta-1.6.0.release_src.tar.bz2
cd manta-1.6.0.release_src/
mkdir build
cd build
cmake ..
sudo make install
make test

