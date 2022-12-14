import tensorflow as tf
import numpy as np
import io
import csv

# Download the model to yamnet.tflite
interpreter = tf.lite.Interpreter('model.tflite')

input_details = interpreter.get_input_details()
waveform_input_index = input_details[0]['index']
output_details = interpreter.get_output_details()
scores_output_index = output_details[0]['index']
#embeddings_output_index = output_details[1]['index']
#spectrogram_output_index = output_details[2]['index']

# Input: 3 seconds of silence as mono 16 kHz waveform samples.
waveform = np.zeros( 16000, dtype=np.float32)

interpreter.resize_tensor_input(waveform_input_index, [len(waveform)], strict=True)
interpreter.allocate_tensors()
interpreter.set_tensor(waveform_input_index, waveform)
interpreter.invoke()

print(interpreter.get_tensor(scores_output_index))
"""
scores, embeddings, spectrogram = (
    interpreter.get_tensor(scores_output_index),
    interpreter.get_tensor(embeddings_output_index),
    interpreter.get_tensor(spectrogram_output_index))
print(scores.shape, embeddings.shape, spectrogram.shape)  # (N, 521) (N, 1024) (M, 64)

# Download the YAMNet class map (see main YAMNet model docs) to yamnet_class_map.csv
# See YAMNet TF2 usage sample for class_names_from_csv() definition.
class_names = class_names_from_csv(open('/path/to/yamnet_class_map.csv').read())
print(class_names[scores.mean(axis=0).argmax()])  # Should print 'Silence'.
"""