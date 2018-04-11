all:TFLOPS_temperature

TFLOPS_temperature:TFLOPS_temperature.cu
	nvcc -arch=compute_61 -code=sm_61 -o TFLOPS_temperature TFLOPS_temperature.cu -lcurand -lcublas -lnvidia-ml -std=c++11

clean:
	rm TFLOPS_temperature
