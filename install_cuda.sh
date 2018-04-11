#!/bin/sh
#Pre-installation
lspci | grep -i nvidia
uname -m && cat /etc/*release
gcc --version
apt-get install linux-headers-$(uname -r)

#install CUDA
#dpkg -i cuda-repo-<distro>_<version>_<architecture>.deb
dpkg -i cuda-repo-ubuntu1604-9-0-local_9.0.176-1_amd64.deb
#apt-key add /var/cuda-repo-<version>/7fa2af80.pub
apt-key add /var/cuda-repo-9-0-local/7fa2af80.pub
apt-get update
apt-get install cuda

#Post-installation
export PATH=/usr/local/cuda-9.0/bin${PATH:+:${PATH}} >>~/.bashrc
export LD_LIBRARY_PATH=/usr/local/cuda-9.0/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}} >>~/.bashrc
cp -r /usr/local/cuda-9.0/samples/ ./cudaSamples
