#https://tfhub.dev/google/lite-model/yamnet/classification/tflite/1
import tensorflow as tf
import numpy as np
import zipfile
import tensorflow_hub as hub
import tensorflow_io as tfio

from scipy.io.wavfile import read

#SAMPLE_RATE, data = read("./drone_detect_audio/drone.wav")
SAMPLE_RATE, data = read("./dataset/train/no_drone/3b63eee1330a4707.wav")
mass = np.zeros(15600)
data = data[2 * 15600 : 3 * 15600]
for num in range(0000, 7800):
    mass[num] = data[num]
data = mass.astype(np.float32)
data /= 32768.0
# Download the model to yamnet-classification.tflite
interpreter = tf.lite.Interpreter('model.tflite')

input_details = interpreter.get_input_details()
waveform_input_index = input_details[0]['index']
output_details = interpreter.get_output_details()
scores_output_index = output_details[0]['index']

# Input: 0.975 seconds of silence as mono 16 kHz waveform samples.
waveform = np.ones(int(round(0.975 * 16000)), dtype=np.float32)
print(waveform.shape)  # Should print (15600,)

interpreter.resize_tensor_input(waveform_input_index, [data.size], strict=True)
interpreter.allocate_tensors()
interpreter.set_tensor(waveform_input_index, data)
interpreter.invoke()
scores = interpreter.get_tensor(scores_output_index)
print(scores)  # Should print (1, 521)

top_class_index = scores.argmax()
'''
labels_file = zipfile.ZipFile('model.tflite').open('my_labels.txt')
labels = [l.decode('utf-8').strip() for l in labels_file.readlines()]
'''
labels = ['drone', 'no_drone']
print(labels[top_class_index])  # Should print 'Silence'.
