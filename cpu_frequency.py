#coding=utf-8
import os,commands,time,threading,argparse,re
out_filename = './result/cpu_stress_test_{}.txt'.format(time.strftime('%Y-%m-%d_%H-%M-%S',time.localtime(time.time())))

def get_cpu_frequency():
    command = 'cpufreq-info | grep "current CPU frequency"'
    raw_frequency = commands.getoutput(command).split("\n")
    frequency = []
    for i in raw_frequency:
        tmp = i.split(" ")
        f = tmp[-2].strip()
        unit = tmp[-1].strip()
        if(unit[0] == 'G'):
            frequency.append(float(f))
        else:
            frequency.append(round(float(f)/1000,4))
    t = 0
    for j in frequency:
        t += j
    return round(t/len(frequency),4)


def get_cpu_temperature():
    command = "sensors | grep Core"
    raw_temperature = commands.getoutput(command).split('\n')
    sum = 0
    count = 0
    for t in raw_temperature:
        sum += int(re.split(r"\+|\(",t)[1][:2])
        count += 1
    return sum/count

for i in range(60):
    frequency = get_cpu_frequency()
    temperature = get_cpu_temperature()
    print("CPU frequency(GHz) : {} , temperature(Celsius) : {}\n ".format(frequency,temperature))
    os.system("echo \"CPU fre quency(MHz) : {} , temperature(Celsius) : {}\n\" >> ./result/cpu_stress_test_log.txt".format(frequency,temperature))
    time.sleep(1)


