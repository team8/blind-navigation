import tensorflow as tf
import matplotlib.pyplot as plt
import cv2
import os
import numpy as np
import random
import preprocessing
input_shape = (100, 100, 3)
# model = tf.keras.models.Sequential([
   # tf.keras.layers.Conv2D(64, (11, 11), input_shape=input_shape),
   # tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
   # tf.keras.layers.Conv2D(128, (9, 9), input_shape=input_shape),
   # tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
   # tf.keras.layers.Conv2D(128, (7, 7), input_shape=input_shape),
   # tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
   # tf.keras.layers.Flatten(input_shape=input_shape),
   # tf.keras.layers.Dense(64, activation='relu'),
   # tf.keras.layers.Dropout(0.1),
   # tf.keras.layers.Dense(3, activation='softmax')])
#
# model.compile(
    # optimizer='Adam', loss='categorical_crossentropy', metrics=['categorical_accuracy'])

VGG16_MODEL=tf.keras.applications.VGG16(input_shape=input_shape,
                                               include_top=False,
                                               weights='imagenet')

VGG16_MODEL.trainable=False
global_average_layer = tf.keras.layers.GlobalAveragePooling2D()
prediction_layer = tf.keras.layers.Dense(3,activation='softmax')

model = tf.keras.Sequential([
  VGG16_MODEL,
  global_average_layer,
  prediction_layer
])

model.compile(
  optimizer=tf.keras.optimizers.Adam(),
  loss='categorical_crossentropy',
  metrics=['acc'])
#find best optimizer (Adam, rmsprop, ADAsgrad etc), loss function is binary closs entropy for now because only binary output but try multi-class cross-entropy loss

# important note: if your true labels are one hot encoded ie. [1, 0, 0], [0, 1, 0], use categorical crossentropy, if true labels are integers ie [1], [2], [3], use sparse categorical_srossentropy.  (saves time in computation and memory because uses single integer for a class)

# important note 2: use binary cross entropy when doing multi label classification (possibly inclusive classes) (categorical cross entropy is when you have exclusive classes) (i need binary cross entropy)


# model.fit(x=np.array(fire_detection_train_dataset), y=one_hot_encoded_array, epochs=8)
batch_size = 32
dataset_path = "../../../ml-datasets/Sidewalk Dataset Augmented/"
# train_ds = tf.keras.preprocessing.image_dataset_from_directory( dataset_path , validation_split = 0.1, subset="training", seed=123, image_size = (input_shape[0], input_shape[1]))
train_ds = tf.keras.preprocessing.image_dataset_from_directory(dataset_path , labels='inferred', batch_size=batch_size, validation_split = 0.05, subset="training", seed=121, image_size = (input_shape[0], input_shape[1]), label_mode="categorical")
labels = ["Left of Sidewalk", "Middle of Sidewalk", "Right of Sidewalk"]

normalization_layer = tf.keras.layers.experimental.preprocessing.Rescaling(1./255)
normalized_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
train_ds = train_ds.shuffle(buffer_size = 1000)
train_ds = train_ds.cache()
print(train_ds)
model.fit(train_ds, epochs=15)

print(model.summary())
if input("Do you want to save model? y for yes, n for no?\n") == 'y':
    model.save("sidewalk_classification_model.h5")
