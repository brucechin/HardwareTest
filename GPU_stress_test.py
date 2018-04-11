import os,time,argparse

parser = argparse.ArgumentParser()
parser.add_argument("d",help="gpu device number")
args = parser.parse_args()
device = args.d
out_filename = './result/gpu{}_stress_test_{}.txt'.format(device,time.strftime('%Y-%m-%d_%H-%M-%S',time.localtime(time.time())))
os.system("./TFLOPS_temperature/TFLOPS_temperature -device {} | tee {}".format(device,out_filename))