import tensorflow as tf
device_name = tf.test.gpu_device_name()
if device_name != '/device:GPU:0':
  raise SystemError('GPU device not found')
print('Found GPU at: {}'.format(device_name))


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import h5py
from sparse_loader import sparse2dense

from tensorflow import keras


dense, pid = sparse2dense('Zuds_weighted_sparse_eval.h5')


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

X_test = np.squeeze(X[index])
y_test = np.squeeze(y[index])
del index


#freeing up memory cause massive arrays...
del X
del y


'''
(X_train_full, y_train_full), (X_test, y_test) = cifar10.load_data()
'''

y_test = y_test-1
#y_test = keras.utils.to_categorical(y_test, num_classes=3)
print('it works...')

model = keras.models.load_model("LodeNet.h5")
predictions = model.predict(X_test)
print(predictions)
np.savez('eval_filesplitter.npz', predictions, y_test)




