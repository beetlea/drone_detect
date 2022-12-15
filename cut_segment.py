import numpy as np
from matplotlib import pyplot as plt
from scipy.io.wavfile import read
import os
import subprocess


path = "./no_detect_copter/audio_mono_level/"
for root, dirs, files in os.walk(path):  
    for filename in files:
        print(filename)

def show_info(aname, a):
    print("Array", aname)
    print("shape:", a.shape)
    print("dtype:", a.dtype)
    print("min, max:", a.min(), a.max())
    print


for root, dirs, files in os.walk(path):  
    for i in files:
        if i[-1:] == "v":
            SAMPLE_RATE, data = read(path + i)
            length = len(data) / SAMPLE_RATE
            begin = 0
            while length:
                if begin + 5 > length:
                    end = (length - begin)
                    length = 0
                else:
                    end = 5
                name_out = "./no_detect_copter/audio/" + i[:-4] + str(begin) + i[-5:]
                command_cut = "ffmpeg -ss {0} -i {1} -t {2} -c copy {3}".format(str(begin), path + i, str(end), name_out)
                print(command_cut)
                subprocess.call(command_cut, shell=True)
                begin += 5