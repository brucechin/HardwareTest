#coding=utf-8
################################################################################
# This script is created by Guancheng Wang, HPC department of Tusimple.
# If any problem occurs, please be free to contact guancheng.wang@tusimple.com
################################################################################
import commands
import os
from sets import Set
import sys,commands,decimal,time

out_filename = './result/result_{}.csv'.format(time.strftime('%Y-%m-%d_%H-%M-%S',time.localtime(time.time())))
password = ''
def profile_bioslog(filename):
    fopen = open(filename, 'r')
    lines = fopen.readlines()
    for cnt in range(len(lines)):
        if "Version" in lines[cnt]:
            biosinfo_list.append(lines[cnt].split(":")[-1].strip())#第一个检测到
        if "Release Date" in lines[cnt]:
            biosinfo_list.append(lines[cnt].split(":")[-1].strip())#第二个检测到



def profile_gpulog(filename):
    fopen = open(filename, 'r')
    lines = fopen.readlines()
    for cnt in range(len(lines)):
        if "CUDA Driver Version / Runtime Version" in lines[cnt]:
            driver_runtime_version.append(lines[cnt].split("Version")[-1].strip()[6:])
        # if "CUDA Capability Major" in lines[cnt]:
        #     capability_M_version.append(lines[cnt].split(":")[-1].strip())
        if "Total amount of global memory" in lines[cnt]:
            memory_size.append(str(round(float(lines[cnt].split(":")[-1].strip().split(" ")[0]) / 1000.0,0)))
        if "Multiprocessors," in lines[cnt] and "CUDA Cores/MP" in lines[cnt]:
            cuda_cores.append(lines[cnt].split(":")[-1].strip()[0:4])
        if "GPU Max Clock rate" in lines[cnt]:
            gpu_mainclock.append(str(round(float(lines[cnt].split(":")[-1].strip()[0:4]) / 1024.0,1)))
        # if "Memory Bus Width" in lines[cnt]:
        #     memory_bus_w.append(lines[cnt].split(":")[-1].strip())

    fopen.close()

def check_gpulog(filename):
    fopen = open(filename, 'r')
    lines = fopen.readlines()
    global std_device_number
    for cnt in range(len(lines)):
        if "CUDA Driver Version / Runtime Version" in lines[cnt]:
            check_driver_runtime_version.append(lines[cnt].split("Version")[-1].strip()[6:])
        # if "CUDA Capability Major" in lines[cnt]:
        #     check_capability_M_version.append(lines[cnt].split(":")[-1].strip())
        if "Total amount of global memory" in lines[cnt]:
            check_memory_size.append(str(round(float(lines[cnt].split(":")[-1].strip().split(" ")[0]) / 1000.0,0)))
        if "Multiprocessors," in lines[cnt] and "CUDA Cores/MP" in lines[cnt]:
            check_cuda_cores.append(lines[cnt].split(":")[-1].strip()[0:4])
        if "GPU Max Clock rate" in lines[cnt]:
            check_gpu_mainclock.append(str(round(float(lines[cnt].split(":")[-1].strip()[0:4]) / 1024.0,1)))
        if "GPU Device Number" in lines[cnt]:
            std_device_number = int(lines[cnt].split(":")[-1].strip())
        # if "Memory Bus Width" in lines[cnt]:
        #     check_memory_bus_w.append(lines[cnt].split(":")[-1].strip())
    fopen.close()


def profile_bandwidthlog(filename):
    fopen = open(filename, 'r')
    lines = fopen.readlines()
    for cnt in range(len(lines)):
        if "Host to Device" in lines[cnt]:
            h2d.append(str(round(float(lines[cnt + 3].split()[-1].strip()) / 1024.0, 2)))
        if "Device to Host" in lines[cnt]:
            d2h.append(str(round(float(lines[cnt + 3].split()[-1].strip()) / 1024.0, 2)))
        if "Device to Device" in lines[cnt]:
            d2d.append(str(round(float(lines[cnt + 3].split()[-1].strip()) / 1024.0, 2)))
    fopen.close()
#之前是标准值上下浮动一个百分比，现在改成写死一个标准范围，考虑到不同的参数浮动范围可能不一样.本函数导入硬盘IO和GPU-CPU带宽标准范围
def check_bandwidthlog(filename):
    fopen = open(filename, 'r')
    lines = fopen.readlines()
    for cnt in range(len(lines)):
        if "Host to Device" in lines[cnt]:
            left = str(round(float(lines[cnt + 3].split()[-1].strip().split("-")[0]) / 1024.0 , 1))
            right = str(round(float(lines[cnt + 3].split()[-1].strip().split("-")[1]) / 1024.0 , 1))
            check_h2d.append(left)
            check_h2d.append(right)
        if "Device to Host" in lines[cnt]:
            left = str(round(float(lines[cnt + 3].split()[-1].strip().split("-")[0]) / 1024.0, 1))
            right = str(round(float(lines[cnt + 3].split()[-1].strip().split("-")[1]) / 1024.0, 1))
            check_d2h.append(left)
            check_d2h.append(right)
        if "Device to Device" in lines[cnt]:
            left = str(round(float(lines[cnt + 3].split()[-1].strip().split("-")[0]) / 1024.0, 1))
            right = str(round(float(lines[cnt + 3].split()[-1].strip().split("-")[1]) / 1024.0, 1))
            check_d2d.append(left)
            check_d2d.append(right)
        if "seq read" in lines[cnt]:
            left = lines[cnt].split(":")[-1].strip().split("-")[0]
            right = lines[cnt].split(":")[-1].strip().split("-")[1]
            seq_read.append(left)
            seq_read.append(right)
        if "seq write" in lines[cnt]:
            left = lines[cnt].split(":")[-1].strip().split("-")[0]
            right = lines[cnt].split(":")[-1].strip().split("-")[1]
            seq_write.append(left)
            seq_write.append(right)
        if "rand read" in lines[cnt]:
            left = lines[cnt].split(":")[-1].strip().split("-")[0]
            right = lines[cnt].split(":")[-1].strip().split("-")[1]
            rand_read.append(left)
            rand_read.append(right)
        if "rand write" in lines[cnt]:
            left = lines[cnt].split(":")[-1].strip().split("-")[0]
            right = lines[cnt].split(":")[-1].strip().split("-")[1]
            rand_write.append(left)
            rand_write.append(right)
    fopen.close()

def profile_flopslog(filename):
    fopen = open(filename, 'r')
    lines = fopen.readlines()
    for cnt in range(len(lines)):
        if "Running N=10 batched" in lines[cnt]:
            single_f.append(str(round(float(lines[cnt+5].split("=")[-1].strip().split("-")[0].strip()) / 1000.0,1)))
            # double_f.append(str(round(float(lines[cnt+10].split("=")[-1].strip()) / 1000.0,3)))
    fopen.close()

def check_flopslog(filename):
    fopen = open(filename, 'r')
    lines = fopen.readlines()
    for cnt in range(len(lines)):
        if "GFLOPS" in lines[cnt]:
            left = lines[cnt].split(":")[-1].strip().split("-")[0].strip()
            right = lines[cnt].split(":")[-1].strip().split("-")[1].strip()
            check_single_f.append(left)
            check_single_f.append(right)
            # check_double_f.append(str(round(float(lines[cnt+2].split("=")[-1].strip()) / 1000.0,3)))
    fopen.close()


def profile_cpulog(filename):
    fopen = open(filename, 'r')
    lines = fopen.readlines()
    for cnt in range(len(lines)):
        if "Model name" in lines[cnt]:
            cpuinfo_list.append(lines[cnt].split(":")[-1].strip())#第三个
        if "CPU(s):" in lines[cnt]:
            cpuinfo_list.append(lines[cnt].split(":")[-1].strip())#第一个
        if "Thread(s) per core" in lines[cnt]:
            cpuinfo_list.append(lines[cnt].split(":")[-1].strip())#第二个
        if "L1d cache" in lines[cnt]:
            local_cache_size.append(lines[cnt].split(":")[-1].strip()[:-1])
        if "L2 cache" in lines[cnt]:
            local_cache_size.append(lines[cnt].split(":")[-1].strip()[:-1])
        if "L3 cache" in lines[cnt]:
            local_cache_size.append(lines[cnt].split(":")[-1].strip()[:-1])

    fopen.close()

def check_cpulog(filename):
    fopen = open(filename, 'r')
    lines = fopen.readlines()
    global cpu_model_name
    global std_os_version
    global std_cpu_number
    global password
    for cnt in range(len(lines)):
        if "Model name" in lines[cnt]:
            cpu_model_name = lines[cnt].split(":")[-1].strip().split(" ")[3]
        if "CPU(s):" in lines[cnt]:
            check_cpuinfo_list.append(lines[cnt].split(":")[-1].strip())
        if "Thread(s) per core" in lines[cnt]:
            check_cpuinfo_list.append(lines[cnt].split(":")[-1].strip())
        if "CPU physical number" in lines[cnt]:
            std_cpu_number = int(lines[cnt].split(":")[-1].strip())
        if "OS Version" in lines[cnt]:
            std_os_version = lines[cnt].split(":")[-1].strip().split(" ")[1]
        if "L1d cache" in lines[cnt]:
            std_cache_size.append(lines[cnt].split(":")[-1].strip()[:-1])
        if "L2 cache" in lines[cnt]:
            std_cache_size.append(lines[cnt].split(":")[-1].strip()[:-1])
        if "L3 cache" in lines[cnt]:
            std_cache_size.append(lines[cnt].split(":")[-1].strip()[:-1])
        if "system root password" in lines[cnt]:
            password = lines[cnt].split(":")[-1].strip()
    fopen.close()


def concatelist(sample):
    res = ""
    for cnt in range(len(sample)-1):
        res = res + sample[cnt] + ","
    res = res + sample[-1] + "\n"
    return res

def check(sample,standard):#传入的sample是数组，standard只有一个item
    res = ""
    flag = True
    if(len(sample) > 0):
        if(sample[0] == standard[0]):
            res = res + str(sample[0])+",    ,"+str(standard[0])+",    ,Pass,"
        else:
            res = res + str(sample[0])+",    ,"+str(standard[0])+",    ,Failed,"
            flag = False

        del sample[0]
    res = res + "\n"
    return res

def check_one(sample,standard):
    res = ""
    flag = True

    if (sample == standard):
        res = res + str(sample) + ",    ," + str(standard) + ",    ,Pass,"
    else:
        res = res + str(sample) + ",    ," + str(standard) + ",    ,Failed,"
        flag = False

    res = res + "\n"
    return res

#仅用于check CPU cache size
def check_parallel(sample,standard):
    res = ""
    flag = True
    if(len(sample) > 0):
        if(sample[0] == standard[0]):
            res = res + sample[0]+",    ,"+standard[0]+",    ,Pass,"
        else:
            res = res + sample[0]+",    ,"+standard[0]+",    ,Failed,"
            flag = False

        del sample[0]
        del standard[0]
    res = res + "\n"
    return res

#standard格式是[left,right],表示标准范围的上下限
def check_bw_flops(sample,standard):
    res = ""
    if(len(sample) > 0 ):
        if(float(standard[0]) < float(sample[0]) and float(standard[1]) > float(sample[0])):
            res = res + str(sample[0]) + ",    ," + str(standard[0]) +"~"+str(standard[1])+ ",    ,Pass,"
        else:
            res = res + str(sample[0]) + ",    ," + str(standard[0]) +"~"+str(standard[1])+ ",    ,Failed,"

        del sample[0]
    res = res + "\n"
    return res

#因为gpu-cpu带宽前两个是×8，后两个是×16，该函数用来改此处的standard
def double_array(array):
    tmp = [str(float(i) * 2) for i in array]
    return tmp


def get_GPU_UUID():
    raw_UUID = commands.getoutput("nvidia-smi -q | grep \"GPU UUID\"").split("\n")
    UUID = []
    for i in raw_UUID:
        UUID.append(i.split(":")[-1].strip())
    return UUID

def get_GPU_name():
    raw_name = commands.getoutput("nvidia-smi -q | grep \"Product Name\"").split("\n")
    name = []
    for i in raw_name:
        name.append(i.split(":")[-1].strip())
    return name

#除去list中所有的空值，因为在parse shell命令输出结果split(" ")后会出现空值
def remove_null(list):
    ret = []
    for i in list:
        if(i != ''):
            ret.append(i)
    return ret

#返回本机硬盘大小，单位为GB
def get_disk_size():
    raw_disk = commands.getoutput("df -l | grep /dev/sda").split("\n")
    disk_list = []
    for i in raw_disk:
        t = remove_null(i.split(" "))
        disk_list.append(int(t[1]))
    return round(sum(disk_list)/1048576.0,2)


def base_info_print():
    fout = open(out_filename, 'w')
    fout.write("Testing Date , {}\n\n".format(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))))
    fout.write("System & Environment,\n\n")
    fout.write("Ubuntu Version," + op_release_info + ",\n")
    fout.write("BIOS Version, {}\n".format(biosinfo_list[0]))
    fout.write("BIOS Date, {}\n".format(biosinfo_list[1]))
    NVIDIA_driver_version = commands.getoutput("cat /proc/driver/nvidia/version | grep Module").split(" ")[8]
    fout.write("GPU Driver Version, {}\n".format(NVIDIA_driver_version))
    fout.write("CUDA Version," + driver_runtime_version[0] + ",\n\n")
#-------------------------------OUTPUT BASIC-------------------------------#
    command = 'echo ' + password + ' | sudo -S dmidecode -s baseboard-serial-number'
    serial_number = commands.getoutput(command).split("\n")[0].strip()
    fout.write("MotherBoard SN,"+serial_number+"\n")
    # CPU_id = commands.getoutput('echo ' + password + ' | sudo -S dmidecode -t processor | grep ID').split(":")[-1]
    # fout.write("CPU serial number,"+CPU_id+"\n")
    disk_id = commands.getoutput('echo ' + password + ' | sudo hdparm -i /dev/sda | grep SerialNo').split("=")[-1].strip()
    fout.write("Disk SN," + disk_id + '\n')
    fout.write("num of CPU," + str(cpu_number) + ",\n")
    fout.write("num of GPU," + str(device_number) + ",\n")
    memory = commands.getoutput("cat /proc/meminfo | grep MemTotal").split(":")[-1].strip().split(" ")[0]
    fout.write("Memory(GB)," + str(round(int(memory)/1048576.0,2)) +",\n" )
    disk = get_disk_size()
    fout.write("Disk(GB)," + str(disk) + ",\n")


    cpu_model = ""
    CPU_Version = commands.getoutput('echo ' + password + ' | sudo -S dmidecode -t processor | grep Version').split(
        "\n")
    for j in range(len(CPU_Version)):
        cpu_model += "CPU {} name,".format(j)
        cpu_tmp_info = CPU_Version[j].strip().split(" ")
        cpu_name = ""
        for i in cpu_tmp_info:
            if "-" in i:
                cpu_name = i
        cpu_model += cpu_name + ',\n'

    cpu_core = "CPU core(s)," + cpuinfo_list[0] + ",\n"

    cpu_threadpercore = "CPU hyperthreading,"
    if (cpuinfo_list[1] > 1):
        cpu_threadpercore += "True,\n"
    else:
        cpu_threadpercore += "False,\n"

    L1_cache = "L1 cache(KB) Private," + local_cache_size[0] + '\n'
    L2_cache = "L2 cache(KB) Private," + local_cache_size[1] + '\n'
    L3_cache = "L3 cache(KB) Shared," + local_cache_size[2] + '\n'

    fout.write(cpu_model)
    fout.write(cpu_core)
    fout.write(cpu_threadpercore)
    fout.write(L1_cache)
    fout.write(L2_cache)
    fout.write(L3_cache)
    fout.write("\n")

    fout.write("Items,Test result,    ,Standard result,    ,Pass/Fail\n\n")

#-------------------------------OUTPUT BASIC END-------------------------------#

def advanced_info_print(i):
    fout = open(out_filename, 'a')

#-------------------------------OUTPUT GPU-------------------------------#
    fout.write("GPU Device {}, {}\n".format(str(i),gpu_name[i]))
    fout.write("GPU UUID : {},\n".format(GPU_UUID[i]))
    # fout.write(gpu_name[i].split(':')[-1] + "\n")
    #gpu_bus_id = "bus_id," + concatelist(bus_id)
    #fout.write(gpu_bus_id)
#    gpu_version = "driver/runtime version," + concatelist(driver_runtime_version)

    # gpu_cap_version = "capability version," + \
    #                   check(capability_M_version, check_capability_M_version)
    # fout.write(gpu_cap_version)
    gpu_memory = "GPU memory(GB)," + \
                 check(memory_size, check_memory_size)
    fout.write(gpu_memory)
    gpu_clock = "Frequency(GHz)," + \
                check(gpu_mainclock, check_gpu_mainclock)
    fout.write(gpu_clock)
    # gpu_mem_bus = "Bus width," + \
    #     check(memory_bus_w,check_memory_bus_w)
    # fout.write(gpu_mem_bus)
    if(i == 0 or i == 1):
        gpu_h2d = "CPU to GPU(GB/s)," + \
                  check_bw_flops(h2d, check_h2d)
        fout.write(gpu_h2d)
        gpu_d2h = "GPU to CPU(GB/s)," + \
                  check_bw_flops(d2h, check_d2h)
        fout.write(gpu_d2h)
    else:
        gpu_h2d = "CPU to GPU(GB/s)," + \
                  check_bw_flops(h2d, double_array(check_h2d))
        fout.write(gpu_h2d)
        gpu_d2h = "GPU to CPU(GB/s)," + \
                  check_bw_flops(d2h, double_array(check_d2h))
        fout.write(gpu_d2h)
    gpu_d2d = "Memory bandwidth(GB/s)," + \
              check_bw_flops(d2d, check_d2d)
    fout.write(gpu_d2d)

    gpu_single_flops = "Single float(TFLOPS)," + \
        check_bw_flops(single_f,check_single_f)
    fout.write(gpu_single_flops)

    fout.write("\n")
#-------------------------------OUTPUT GPU END-------------------------------#

    fout.close()



if __name__ == "__main__":
    CUDASAMPLES = "/home/tusimple/HardwareTest/cudaSamples"
    device_number = int(commands.getoutput('nvidia-smi -L | wc -l'))
    cpu_number = int(commands.getoutput("cat /proc/cpuinfo | grep \"physical id\" | sort | uniq | wc -l"))
    operation_info = commands.getoutput("lsb_release -a")
    op_release_info = operation_info.split("\n")[2].split(":")[-1].split(" ")[1]
# cpu and mainboard

    serial_number = {}#cpu,gpu,memory,disk等的ID
    cpuinfo_list = []
    biosinfo_list = []
    check_cpuinfo_list = []
    std_cache_size = []
    local_cache_size = []
    cpu_model_name = ""
    std_cpu_number = 0
    std_os_version = ""
    os.system("lscpu > log_cpu")
    os.system("cat /proc/cpuinfo > log_cpu_detail")
    os.system("echo tusimple2017 | sudo -S dmidecode -t bios > log_bios")
    #在test上测试硬盘读写，测完后删掉
    profile_cpulog("log_cpu")
    profile_bioslog("log_bios")
    check_cpulog('./standard_info')
# gpu
#------------------GPU:BASIC INFORMATION------------------#
    bus_id_str = commands.getoutput("nvidia-smi --query-gpu=pci.bus_id --format=csv")
    bus_id =  bus_id_str.split()[1:]
    driver_runtime_version = []
    check_driver_runtime_version = []
    # capability_M_version = []
    # check_capability_M_version = []
    memory_size = []
    check_memory_size = []
    cuda_cores = []
    check_cuda_cores = []
    gpu_mainclock = []
    check_gpu_mainclock = []
    memory_bus_w = []
    check_memory_bus_w = []
    gpu_name = get_GPU_name()
    std_device_number = 0
    os.system(CUDASAMPLES + "/1_Utilities/deviceQuery/deviceQuery > log_gpu")
    profile_gpulog("./log_gpu")
    check_gpulog("./standard_info")


#------------------BASIC INFORMATION END------------------#

#-----------------------GPU:BANDWIDTH-------------------------#
    h2d = []
    d2h = []
    d2d = []
    check_h2d = []
    check_d2h = []
    check_d2d = []
    # disk IO standard
    rand_write = []
    rand_read = []
    seq_write = []
    seq_read = []
    # for each device
    for n in range(device_number):
        os.system(CUDASAMPLES + "/1_Utilities/bandwidthTest/bandwidthTest -device=" + str(n) + " > log_bandwidth_"+str(n))
        profile_bandwidthlog("./log_bandwidth_"+str(n))
    # for all device
    os.system(CUDASAMPLES + "/1_Utilities/bandwidthTest/bandwidthTest -device=all > log_bandwidth_all")
    profile_bandwidthlog("./log_bandwidth_all")
    check_bandwidthlog("./standard_info")
    GPU_UUID = get_GPU_UUID()
#-----------------------BANDWIDTH END-------------------------#

#-----------------------GPU:GFLOPS------------------------#
    single_f = []
    double_f = []
    check_single_f = []
    check_double_f = []
    # for each device
    for n2 in range(device_number):
        os.system(CUDASAMPLES + "/7_CUDALibraries/batchCUBLAS/batchCUBLAS -device=" + str(n) + " > log_flops_"+str(n2))
        profile_flopslog("./log_flops_"+str(n2))
        check_flopslog("./standard_info")

#-----------------------GFLOPS END------------------------#



    base_info_print()
    for i in range(device_number):
        advanced_info_print(i)

    for i in range(device_number):
        os.system("nvidia-smi -q -i {} > ./result/gpu{}_detail_info.txt".format(i,i))

    print("--------SUCCESS-------")
