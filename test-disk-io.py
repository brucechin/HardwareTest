import os,time
password = "tusimple2017"
out_filename = './result/result_disk_io_{}.txt'.format(time.strftime('%Y-%m-%d_%H-%M-%S',time.localtime(time.time())))
os.system("touch test")
os.system("echo {} | sudo -S apt-get update > /dev/null".format(password))
os.system("echo {} | sudo -S apt-get install -y fio > /dev/null".format(password))
os.system("echo {} | sudo -S fio fio.conf > fio.log".format(password))
os.system("rm test")
fout = open(out_filename,"w")
disk_io = []
fopen = open('fio.log', 'r')
lines = fopen.readlines()
for cnt in range(len(lines)):
    if "status group" in lines[cnt]:
        disk_io.append(int(lines[cnt + 1].split(",")[1].split("=")[-1][:-4]) / 1024)
fout.write("Random read(MB/s),{}\n".format(disk_io[0]))
fout.write("Random write(MB/s),{}\n".format(disk_io[2]))
fout.write("Seq read(MB/s),{}\n".format(disk_io[1]))
fout.write("Seq write(MB/s),{}\n".format(disk_io[3]))
fout.write("\n")
