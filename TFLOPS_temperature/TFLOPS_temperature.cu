#include <curand.h>
#include <cuda_runtime.h>
#include <cublas_v2.h>
#include <iostream>
#include <chrono>
#include <nvml.h>
#include <cstdio>
#include <cstdlib>
#include <string>

static int deviceID = 0;

FILE* test_result;
std::string file_name;

int gpu_blas_mmul(const float *A, const float *B, float *C, const int m, const int k, const int n) 
{
    nvmlReturn_t result;
    unsigned int temp = 0;
    unsigned int clock_freq = 0;

    result = nvmlInit();
    if (NVML_SUCCESS != result)
    { 
        printf("Failed to initialize NVML: %s\n", nvmlErrorString(result));
        printf("Press ENTER to continue...\n");
        getchar();
        return 1;
    }

    nvmlDevice_t device;

    result = nvmlDeviceGetHandleByIndex(deviceID, &device);
    if (NVML_SUCCESS != result)
    { 
        printf("Failed to get handle for device %i: %s\n", deviceID, nvmlErrorString(result));
        result = nvmlShutdown();
        if (NVML_SUCCESS != result)
            printf("Failed to shutdown NVML: %s\n", nvmlErrorString(result));
        printf("Press ENTER to continue...\n");
        getchar();
        return 1;
    }

    int lda=m,ldb=k,ldc=m;
    const float alf = 1;
    const float bet = 0;
    const float *alpha = &alf;
    const float *beta = &bet;
    const double G_operations = 2*double(m)/1000*double(k)/1000*double(n)/1000;

    cublasHandle_t handle;
    cublasCreate(&handle);
    cudaEvent_t start, stop;
    cudaEventCreate(&start);
    cudaEventCreate(&stop);

    test_result = fopen(file_name.c_str(), "a");
    fprintf(test_result,"Temperature\t TFLOPS\t CLOCKS\t \n");
    fclose(test_result);

    while(temp < 95)
    {   
        cudaEventRecord(start);
        cublasSgemm(handle, CUBLAS_OP_N, CUBLAS_OP_N, m, n, k, alpha, A, lda, B, ldb, beta, C, ldc);    
        cudaEventRecord(stop);
        cudaEventSynchronize(stop);
        float milliseconds = 0;
        cudaEventElapsedTime(&milliseconds, start, stop);

        result = nvmlDeviceGetTemperature(device, NVML_TEMPERATURE_GPU, &temp);
        if (NVML_SUCCESS != result) {
            printf("Failed to get temperature of device %i: %s\n", 0, nvmlErrorString(result));
        }

        result = nvmlDeviceGetClockInfo(device, NVML_CLOCK_SM , &clock_freq);
        if (NVML_SUCCESS != result) {
            printf("Failed to get clock frequency of device %i: %s\n", 0, nvmlErrorString(result));
        }
        std::cout << "Temperature," << temp << ",";
        std::cout << "TFLOPS," << G_operations/milliseconds << ",";          
        std::cout << "CLOCKS," << clock_freq << "\n";

        test_result = fopen(file_name.c_str(),"w");
        fprintf(test_result,"%d\t %f\t %d\t \n", temp, G_operations/milliseconds, clock_freq);
        fclose(test_result);
    }

    cublasDestroy(handle);

    result = nvmlShutdown();
    if (NVML_SUCCESS != result)
        printf("Failed to shutdown NVML: %s\n", nvmlErrorString(result));
    return 0;
}

void GPU_fill_rand(float *A, int nr_rows_A, int nr_cols_A) 
{
    curandGenerator_t prng;
    curandCreateGenerator(&prng, CURAND_RNG_PSEUDO_DEFAULT);
    curandSetPseudoRandomGeneratorSeed(prng, (unsigned long long) clock());
    curandGenerateUniform(prng, A, nr_rows_A * nr_cols_A);
}

int main(const int argc, const char *argv[])
{
    if(strcmp(argv[1], "-device") == 0)
    {
        deviceID = (int)atoi(argv[2]);

    }
    printf("Using device %d\n",deviceID);
    file_name ="../temperature_" + std::to_string(deviceID) + ".csv";
    cudaSetDevice(deviceID);

    int nr_rows_A, nr_cols_A, nr_rows_B, nr_cols_B, nr_rows_C, nr_cols_C;
    // int m = 28*28, n = 8*128, k = 96;
    int m = 16000, n = 16000, k = 16000;

    nr_rows_A = m;
    nr_rows_C = m;
    nr_cols_A = n;
    nr_rows_B = n;
    nr_cols_B = k;
    nr_cols_C = k;

    float *h_A = (float *)malloc(nr_rows_A * nr_cols_A * sizeof(float));
    float *h_B = (float *)malloc(nr_rows_B * nr_cols_B * sizeof(float));
    float *h_C = (float *)malloc(nr_rows_C * nr_cols_C * sizeof(float));

    float *d_A, *d_B, *d_C;
    cudaMalloc(&d_A,nr_rows_A * nr_cols_A * sizeof(float));
    cudaMalloc(&d_B,nr_rows_B * nr_cols_B * sizeof(float));
    cudaMalloc(&d_C,nr_rows_C * nr_cols_C * sizeof(float));

    GPU_fill_rand(d_A, nr_rows_A, nr_cols_A);
    GPU_fill_rand(d_B, nr_rows_B, nr_cols_B);

    cudaMemcpy(h_A,d_A,nr_rows_A * nr_cols_A * sizeof(float),cudaMemcpyDeviceToHost);
    cudaMemcpy(h_B,d_B,nr_rows_B * nr_cols_B * sizeof(float),cudaMemcpyDeviceToHost);
        
    gpu_blas_mmul(d_A, d_B, d_C, nr_rows_A, nr_cols_A, nr_cols_B);      

    // cudaMemcpy(h_C,d_C,nr_rows_C * nr_cols_C * sizeof(float),cudaMemcpyDeviceToHost);

    cudaFree(d_A);
    cudaFree(d_B);
    cudaFree(d_C);  

    free(h_A);
    free(h_B);
    free(h_C); 

    return 0;
}
