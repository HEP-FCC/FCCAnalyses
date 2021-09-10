#%tensorflow_version 2.x
import tensorflow as tf
device_name = tf.test.gpu_device_name()
if device_name != '/device:GPU:0':
  raise SystemError('GPU device not found')
print('Found GPU at: {}'.format(device_name))

import numpy as np
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import h5py
from sparse_loader import sparse2dense

from tensorflow import keras

from tensorflow.keras.datasets import cifar10
from tensorflow.keras.applications.densenet import preprocess_input
from tensorflow.keras.preprocessing.image import ImageDataGenerator

#Here I will very simply load the data. Note that I should in theory also split a set for validation, and shuffle the data...
#Can write the decompressor here if I want

dense, pid = sparse2dense('Zuds_weighted_sparse.h5')
print(pid)
#f = h5py.File('Zuds_weighted_short.h5', 'r')
#y = np.array(f['pid'][:])
#X = np.array(f['histos'][:])
#f.close()

y = pid
X = dense
#Below statements not necessary as python only shares reference rather than copying... 
#del pid 
#del dense

print('PID')
print(np.unique(y))
X = X[y<4]
y = y[y<4]
print('finished loading h5 file...')
index = np.arange(len(y))
index = np.random.shuffle(index)
split_index = int(0.8*len(y))

X = np.squeeze(X[index])
y = np.squeeze(y[index])
del index

X_train_full = X[:split_index]
X_test = X[split_index:]
y_train_full = y[:split_index]
y_test = y[split_index:]

#freeing up memory cause massive arrays...
del X 
del y


'''
(X_train_full, y_train_full), (X_test, y_test) = cifar10.load_data()
'''

print('FIX ME!!!')
y_train_full = y_train_full-1
y_test = y_test-1
y_train_full = keras.utils.to_categorical(y_train_full, num_classes=3)
y_test = keras.utils.to_categorical(y_test, num_classes=3)
print('it works...')

'''
model = tf.keras.models.Sequential([
  tf.keras.layers.Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_uniform', padding='same', input_shape=(8, 29, 29), data_format='channels_first'),
  tf.keras.layers.Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_uniform', padding='same', data_format='channels_first'),
  tf.keras.layers.MaxPooling2D((2, 2)),
  tf.keras.layers.Conv2D(64, (3, 3), activation='relu', kernel_initializer='he_uniform', padding='same', data_format='channels_first'),
  tf.keras.layers.Conv2D(64, (3, 3), activation='relu', kernel_initializer='he_uniform', padding='same', data_format='channels_first'),
  tf.keras.layers.MaxPooling2D((2, 2)),
  #tf.keras.layers.Conv2D(128, (3, 3), activation='relu', kernel_initializer='he_uniform', padding='same', data_format='channels_first'),
  #tf.keras.layers.Conv2D(128, (3, 3), activation='relu', kernel_initializer='he_uniform', padding='same', data_format='channels_first'),
  #tf.keras.layers.MaxPooling2D((2, 2)),
  tf.keras.layers.Flatten(),
  tf.keras.layers.Dense(128, activation='relu', kernel_initializer='he_uniform'),
  tf.keras.layers.Dense(3, activation='softmax'),
])
'''

model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(16, 4, padding = 'same', activation= 'relu', input_shape=(8,29,29), data_format='channels_first'),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Conv2D(16, 4, padding = 'same', activation= 'relu', data_format='channels_first'),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Dropout(0.5),
    #tf.keras.layers.Conv2D(16, 3, padding = 'same', activation= 'relu'),
    #tf.keras.layers.MaxPooling2D(),
    #tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Conv2D(16, 3, padding = 'same', activation= 'relu', data_format='channels_first'),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Conv2D(16, 3, padding = 'same', activation= 'relu', data_format='channels_first'),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation ='relu'),
    tf.keras.layers.Dense(3, activation = 'softmax')
])




print(model.summary())
model.compile(optimizer=keras.optimizers.Adam(learning_rate=0.001), 
              loss='categorical_crossentropy', 
              metrics=['accuracy'])


early_stopping_cb = keras.callbacks.EarlyStopping(patience=5, restore_best_weights=True)
history = model.fit(X_train_full, y_train_full, steps_per_epoch = len(X_train_full) / 32, epochs=50, validation_data=(X_test, y_test), callbacks=[early_stopping_cb])


acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

loss = history.history['loss']
val_loss = history.history['val_loss']

initial_epochs = history.epoch[-1]+1
'''
plt.figure(figsize=(12, 8))
plt.plot(acc, label='Training Accuracy')
plt.plot(val_acc, label='Validation Accuracy')
plt.ylim([0, 1])
#plt.plot([initial_epochs-1,initial_epochs-1], plt.ylim(), label='Start Fine Tuning')
plt.title('Training and Validation Accuracy and Loss')
plt.plot(loss, label='Training Loss')
plt.plot(val_loss, label='Validation Loss')
plt.legend(loc='lower left')
plt.xlabel('epoch')
plt.grid(True)
plt.savefig('training.pdf')
'''

np.savez('train_results_LodeNet.npz', acc, val_acc, loss, val_loss, initial_epochs)
model.save('LodeNet.h5')
