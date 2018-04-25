#!/usr/bin/env bash

cd result
touch gpu-stress-test.txt
cd ../gpu-burn
./gpu_burn 500  > ../result/gpu-stress-test.txt
