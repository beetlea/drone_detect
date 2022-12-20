#https://github.com/tensorflow/docs/blob/master/site/en/tutorials/audio/transfer_learning_audio.ipynb
import os

from IPython import display
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_io as tfio

my_classes = 2

yamnet_model_handle = 'https://tfhub.dev/google/yamnet/1'
yamnet_model = hub.load(yamnet_model_handle)

'''
class_map_path = yamnet_model.class_map_path().numpy().decode('utf-8')
class_names =list(pd.read_csv(class_map_path)['display_name'])


for name in class_names[:20]:
    print(name)
print('...')
'''

@tf.function
def load_wav_16k_mono(filename):
    """ Load a WAV file, convert it to a float tensor, resample to 16 kHz single-channel audio. """
    file_contents = tf.io.read_file(filename)
    wav, sample_rate = tf.audio.decode_wav(
          file_contents,
          desired_channels=1)
    wav = tf.squeeze(wav, axis=-1)
    sample_rate = tf.cast(sample_rate, dtype=tf.int64)
    wav = tfio.audio.resample(wav, rate_in=sample_rate, rate_out=16000)
    return wav




'''
def test_model_custom():
    testing_wav_file_name = tf.keras.utils.get_file('miaow_16k.wav',
                                                    'https://storage.googleapis.com/audioset/miaow_16k.wav',
                                                    cache_dir='./',
                                                    cache_subdir='test_data')

    print(testing_wav_file_name)



    testing_wav_data = load_wav_16k_mono(testing_wav_file_name)

    _ = plt.plot(testing_wav_data)

    # Play the audio file.
    display.Audio(testing_wav_data, rate=16000)


    class_map_path = yamnet_model.class_map_path().numpy().decode('utf-8')
    class_names =list(pd.read_csv(class_map_path)['display_name'])

    for name in class_names[:20]:
        print(name)
    print('...')


    scores, embeddings, spectrogram = yamnet_model(testing_wav_data)
    class_scores = tf.reduce_mean(scores, axis=0)
    top_class = tf.argmax(class_scores)
    inferred_class = class_names[top_class]

    print(f'The main sound is: {inferred_class}')
    print(f'The embeddings shape: {embeddings.shape}')

_ = tf.keras.utils.get_file('esc-50.zip',
                        'https://github.com/karoldvl/ESC-50/archive/master.zip',
                        cache_dir='./',
                        cache_subdir='datasets',
                        extract=True)
'''
esc50_csv = './dataset.csv'
base_data_path = 'C:/Users/user/Documents/test/audio_detect_NN/datasets/ESC-50-master/audio/'

pd_data = pd.read_csv(esc50_csv)
pd_data.head()



filenames = pd_data['filename']
targets = pd_data['target']
folds = pd_data['fold']

main_ds = tf.data.Dataset.from_tensor_slices(( filenames, targets, folds))
main_ds.element_spec

def load_wav_for_map(filename, label, fold):
  return load_wav_16k_mono(filename), label, fold

main_ds =  .map(load_wav_for_map)
main_ds.element_spec


def extract_embedding(wav_data, label, fold):
  ''' run YAMNet to extract embedding from the wav data '''
  scores, embeddings, spectrogram = yamnet_model(wav_data)
  num_embeddings = tf.shape(embeddings)[0]
  return (embeddings,
            tf.repeat(label, num_embeddings),
            tf.repeat(fold, num_embeddings))

# extract embedding
main_ds = main_ds.map(extract_embedding).unbatch()
main_ds.element_spec


cached_ds = main_ds.cache()
train_ds = cached_ds.filter(lambda embedding, label, fold: fold < 4)
val_ds = cached_ds.filter(lambda embedding, label, fold: fold == 4)
test_ds = cached_ds.filter(lambda embedding, label, fold: fold == 5)

# remove the folds column now that it's not needed anymore
remove_fold_column = lambda embedding, label, fold: (embedding, label)

train_ds = train_ds.map(remove_fold_column)
val_ds = val_ds.map(remove_fold_column)
test_ds = test_ds.map(remove_fold_column)

train_ds = train_ds.cache().shuffle(1000).batch(32).prefetch(tf.data.AUTOTUNE)
val_ds = val_ds.cache().batch(32).prefetch(tf.data.AUTOTUNE)
test_ds = test_ds.cache().batch(32).prefetch(tf.data.AUTOTUNE)


my_model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(1024), dtype=tf.float32,
                          name='input_embedding'),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
], name='my_model')

my_model.summary()



my_model.compile(loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
                 optimizer="adam",
                 metrics=['accuracy'])

callback = tf.keras.callbacks.EarlyStopping(monitor='loss',
                                            patience=3,
                                            restore_best_weights=True)


history = my_model.fit(train_ds,
                       epochs=1,
                       validation_data=val_ds,
                       callbacks=callback)



loss, accuracy = my_model.evaluate(test_ds)

print("Loss: ", loss)
print("Accuracy: ", accuracy)

'''
scores, embeddings, spectrogram = yamnet_model(testing_wav_data)
result = my_model(embeddings).numpy()

inferred_class = my_classes[result.mean(axis=0).argmax()]
print(f'The main sound is: {inferred_class}')
'''


class ReduceMeanLayer(tf.keras.layers.Layer):
  def __init__(self, axis=0, **kwargs):
    super(ReduceMeanLayer, self).__init__(**kwargs)
    self.axis = axis

  def call(self, input):
    return tf.math.reduce_mean(input, axis=self.axis)

saved_model_path = './drone_detect_audio'

input_segment = tf.keras.layers.Input(shape=(), dtype=tf.float32, name='audio')
embedding_extraction_layer = hub.KerasLayer(yamnet_model_handle,
                                            trainable=False, name='yamnet')
_, embeddings_output, _ = embedding_extraction_layer(input_segment)
serving_outputs = my_model(embeddings_output)
serving_outputs = ReduceMeanLayer(axis=0, name='classifier')(serving_outputs)
serving_model = tf.keras.Model(input_segment, serving_outputs)
serving_model.save('/tmp/model.ckpt')

SAVED_MODEL_DIR = '/tmp/model.ckpt'

tf.saved_model.save(
    serving_model,
    SAVED_MODEL_DIR,
    signatures={
        'train':
            serving_model.train.get_concrete_function(),
        'infer':
            serving_model.infer.get_concrete_function(),
        'save':
            serving_model.save.get_concrete_function(),
        'restore':
            serving_model.restore.get_concrete_function(),
    })
#converter = tf.lite.TFLiteConverter.from_keras_model(serving_model)
converter = tf.lite.TFLiteConverter.from_saved_model(SAVED_MODEL_DIR)
converter.target_spec.supported_ops = [
    tf.lite.OpsSet.TFLITE_BUILTINS,  # enable TensorFlow Lite ops.
    tf.lite.OpsSet.SELECT_TF_OPS  # enable TensorFlow ops.
]
#converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.experimental_enable_resource_variables = True
tflite_model = converter.convert()
with open('model_15_12_22.tflite', 'wb') as f:
    f.write(tflite_model)

#serving_model.save(saved_model_path, include_optimizer=False)

tf.keras.utils.plot_model(serving_model)

reloaded_model = tf.saved_model.load(saved_model_path)
