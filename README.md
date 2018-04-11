# HardwareTest

###部分测试项目解释

Serial number:主板编码 sudo dmidecode -s baseboard-serial-number 可得到

CPU physical number:有几个CPU

GPU device number:有几个GPU

CPU core ： 有几个CPU核

###CPU压力测试

./test-cpu-temperature.sh

CPU满载且较高温度下（建议能达到80度左右时）每5秒检测是否降频，持续100次.

使用2w × 2w的矩阵乘积为负载，可在脚本中修改计算几次来调节测试时长


###查询各种序列号的命令

1.CPU ： sudo dmidecode -t processor | grep ID

2.memory : sudo dmidecode -t memory | grep "Serial Number"

3.GPU : nvidia-smi -q | grep "Serial Number"
        nvidia-smi -q | grep "GPU UUID"
        cat /proc/driver/nvidia/version(查NVIDIA驱动版本)
        
4.disk : sudo hdparm -t /dev/sda
         sudo hdparm -i /dev/sda | grep SerialNo(查硬盘ID)

