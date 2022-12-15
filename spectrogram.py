# for data transformation
import numpy as np
# for visualizing the data
import matplotlib.pyplot as plt
# for opening the media file
import scipy.io.wavfile as wavfile
from scipy.fft import rfft, rfftfreq 
import cv2

Fs, aud1 = wavfile.read("slow_not_lifting_off_then_stop_syma_x5sw.wav")#('audio2549552_mono2352160040.wav')
# select left channel only
first = aud1[: Fs * 5]

Fs2, aud = wavfile.read('close_syma_x5sw_001.wav')
two = aud[: Fs2 * 5 ]

Fs3, aud = wavfile.read('audio43060o_monoo.wav')
three = aud[Fs3 * 40: Fs3 * 45]

Fs4, aud = wavfile.read('drone.wav')
four = aud[:]


yf = rfft(aud1)/ len(aud1)
xf = rfftfreq(5 * Fs3, 1/Fs3)
width = 1000
freq = 20000
step = freq / width
max_scale = np.max(yf)
pic = np.zeros((width, 1000))

step_ = int(Fs / 10)
col = 0
row = 0
data = 0
for time in range(0,4999, step_):
    cnt = 0
    pix = 0
    data = np.fft.fft(aud1[time: time + step_])/ step_
    freq = np.fft.fftfreq(aud1[time: time + step_].shape[-1])
    row = 0
    for i in data:
       
        if cnt < step:
            pix =+ i
            
        else:
            pix = (pix / max_scale) * 255
            pic[col, row] = int(pix)
            row += 1
            cnt = 0
        cnt += 1
    col += 1
cv2.imshow("frame", pic)



# trim the first 125 seconds
#first = aud[:int(Fs*125)]
'''
plt.figure(200)
powerSpectrum, frequenciesFound, time, imageAxis = plt.specgram(first, Fs=Fs)
powerSpectrum, frequenciesFound, time, imageAxis = plt.specgram(two, Fs=Fs2)
plt.show()
'''

fig, (ax1, ax2, ax3, ax4) = plt.subplots(nrows=4)
data, freqs, bins, im = ax1.specgram(aud1[time: time + step_], Fs=Fs)
ax1.axis('tight')

data, freqs, bins, im = ax2.specgram(two, Fs=Fs2 )
ax2.axis('tight')

data, freqs, bins, im = ax3.specgram(three, Fs=Fs3)
ax3.axis('tight')

data, freqs, bins, im = ax4.specgram(four, Fs=Fs4)
ax4.axis('tight')
plt.show()
#waits for user to press any key 
#(this is necessary to avoid Python kernel form crashing)
cv2.waitKey(0) 
  
#closing all open windows 
cv2.destroyAllWindows() 