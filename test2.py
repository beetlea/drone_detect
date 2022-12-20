import matplotlib.pyplot as plt
import numpy as np
from scipy.io.wavfile import read
SAMPLE_RATE, data = read("right_constant_mkh8040.wav")
data = data[2 * 15600 : 3 * 15600]
cycles = 100 # how many sine cycles
resolution = 44100 # how many datapoints to generate

length = np.pi * 2 * cycles
data2 = np.sin(np.arange(0, length, length / resolution))
sp = np.fft.rfft(data2)
sp =  np.abs(sp)
print(sp.argmax(axis=0))
'''
freq = np.fft.rfftfreq(44100, 1/44100)
plt.plot(freq, sp)
plt.show()
'''