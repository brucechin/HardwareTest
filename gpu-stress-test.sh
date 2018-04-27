#!/usr/bin/env bash

cd result
touch gpu-stress-test.txt
cd ../gpu-stress-test
echo "Doing GPU stress test,result is stored in ./result/gpu-stress-test.txt"
./gpu_burn 500000  > ../result/gpu-stress-test.txt
echo "GPU stress test done"
