#https://zvukipro.com/electronic/687-zvuki-kvadrokoptera-drona.html

from scipy.fft import rfft, rfftfreq 
import numpy as np
from matplotlib import pyplot as plt
from scipy.io.wavfile import read
import os

files = 0

for root, dirs, files in os.walk("."):  
    for filename in files:
        print(filename)

def show_info(aname, a):
    print("Array", aname)
    print("shape:", a.shape)
    print("dtype:", a.dtype)
    print("min, max:", a.min(), a.max())
    print


DURATION = 1
BEGIN = 5
cnt = 241
plt.figure()
for root, dirs, files in os.walk("."):  
    for i in files:
        if i[-1:] == "v":
            SAMPLE_RATE, data = read(i)
            data = data[BEGIN * SAMPLE_RATE : (BEGIN + DURATION) * SAMPLE_RATE]
            data = data.astype(np.int16)
            show_info("input",data)
            # обратите внимание на r в начале имён функций
            yf = rfft(data)
            xf = rfftfreq(DURATION * SAMPLE_RATE, 1/SAMPLE_RATE)
            plt.subplot(cnt)
            plt.xlabel('freq')
            plt.ylabel('power')
            cnt +=1
            plt.plot(xf, np.abs(yf))
            plt.title(i)
            plt.grid(True)
plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.25,
                    wspace=0.35)
plt.show()