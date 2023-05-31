import tensorflow as tf
from tensorflow.keras import layers, models
import tensorflow_datasets as tfds
import time


@ray.remote
class Small_ML:
    def __init__(self):
        dataset, info = tfds.load('cifar10', shuffle_files=True, with_info=True, as_supervised=True)
        train_dataset = dataset['train']
        test_dataset = dataset['test']

        train_dataset = train_dataset.map(lambda image, label: (tf.image.resize(image, (32, 32)), label))
        test_dataset = test_dataset.map(lambda image, label: (tf.image.resize(image, (32, 32)), label))

        self.train_dataset = train_dataset.batch(32).prefetch(tf.data.AUTOTUNE)
        self.test_dataset = test_dataset.batch(32)

    def process(self):
        model = models.Sequential()
        model.add(layers.Conv2D(16, (3, 3), activation='relu', input_shape=(32, 32, 3)))
        model.add(layers.MaxPooling2D((2, 2)))
        model.add(layers.Flatten())
        model.add(layers.Dense(10))

        model.compile(optimizer='adam',
                      loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                      metrics=['accuracy'])

        start_time = time.time()
        with tf.device('/GPU:0'):
            model.fit(self.train_dataset, epochs=10, validation_data=self.test_dataset)
        end_time = time.time()
        gpu_training_time = end_time - start_time

        with tf.device('/GPU:0'):
            test_loss, test_acc = model.evaluate(self.test_dataset, verbose=2)
        print('Accuracy of the network on the test images (GPU):', test_acc)
        print('Training time on GPU:', gpu_training_time)