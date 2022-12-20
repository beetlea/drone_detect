import serial
import math
import numpy as np
from scipy.io.wavfile import read
import matplotlib.pyplot as plt
"""
ser = serial.Serial ("COM6")    #Open named port 
ser.baudrate = 9600                     #Set baud rate to 9600
data = ser.read(10)                     #Read ten characters from serial port to data
ser.write(data)                         #Send back the received data
ser.close() 
"""

SAMPLE_RATE, data = read("right_constant_mkh8040.wav")
mass = np.zeros(15600)
data = data[2 * 15600 : 3 * 15600]
cycles = 1000 # how many sine cycles
resolution = 44100 # how many datapoints to generate

length = np.pi * 2 * cycles
data2 = np.sin(np.arange(0, length, length / resolution))
data2 *= 32768

print(math.sin(math.pi/2))

def cos(index, freq, sample_rate):
    return math.cos((2 * math.pi * freq * index)/ sample_rate)

def sin(index, freq, sample_rate):
    return math.sin((2 * math.pi * freq * index)/ sample_rate)

def dft(frame, sample_rate, begin, result_size, length):
    result = np.zeros(result_size * 2)
    freq = 0
    for i in range(begin, int(result_size / 2)):
        freq = i
        for j in range(length):
            result[2 * i] += frame[j] * cos(j, freq, sample_rate)
            result[2 * i + 1] += frame[j] * sin(j, freq, sample_rate)
    result /= result_size
    return result


def getFFT(frame, sample_rate, begin, end, length):
    result = dft(frame, sample_rate, begin, end, length)
    amplitude = np.zeros(int(sample_rate / 2))
    for i in range(int(len(result) /2)):
        amplitude[i] = int(math.sqrt(result[2*i]*result[2*i] + result[2*i+1]*result[2*i+1]))
    return amplitude


cycles = 1000 # how many sine cycles
resolution = 20000 # how many datapoints to generate

length = np.pi * 2 * cycles
my_wave = np.sin(np.arange(0, length, length / resolution))

data = getFFT(data, SAMPLE_RATE, 0, 1100, 4000)
print(data)

plt.plot( range(0,22050), data)
#plt.plot( range(0,44100), data2)
plt.show()