#!/bin/bash

export PATH=/usr/local/cuda/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH

CUDASAMPLES="/home/tusimple/HardwareTest/cudaSamples"
FILENAME="$CUDASAMPLES/7_CUDALibraries/batchCUBLAS/batchCUBLAS.cpp"

sed -i 's/^#define BENCH_MATRIX_M.*/#define BENCH_MATRIX_M  (4096)/g' $FILENAME
sed -i 's/^#define BENCH_MATRIX_K.*/#define BENCH_MATRIX_K  (4096)/g' $FILENAME
sed -i 's/^#define BENCH_MATRIX_N.*/#define BENCH_MATRIX_N  (4096)/g' $FILENAME

DEVICE_QUERY="$CUDASAMPLES/1_Utilities/deviceQuery/"
BANDWIDTH_TEST="$CUDASAMPLES/1_Utilities/bandwidthTest/"
FLOPS_TEST="$CUDASAMPLES/7_CUDALibraries/batchCUBLAS/"
cd $DEVICE_QUERY;make
cd $BANDWIDTH_TEST;make
cd $FLOPS_TEST;make

cd /home/tusimple/HardwareTest
python gototest.py

