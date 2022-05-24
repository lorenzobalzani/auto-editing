import numpy as np
import tensorflow as tf
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report
from hand_detection.model_config import *

class Classifier:
    def __init__(self, model_save_path, random_state, num_classes, num_features):
        self.model_save_path = model_save_path
        self.random_state = random_state
        self.num_classes = num_classes
        self.num_features = num_features
        
    def prepare_dataset(self, path):
        X_dataset = np.loadtxt(path, delimiter=',', dtype='float32', usecols=list(range(1, self.num_features + 1)))
        y_dataset = np.loadtxt(path, delimiter=',', dtype='int32', usecols=(0))
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X_dataset, y_dataset, train_size=train_size, random_state=self.random_state)

    def define_model(self, loss, optimizer='adam', metrics=['accuracy'], activations='relu', last_layer_activation='softmax'):
        self.model = tf.keras.models.Sequential([
            tf.keras.layers.Input((self.num_features, )),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(20, activation=activations),
            tf.keras.layers.Dropout(0.4),
            tf.keras.layers.Dense(10, activation=activations),
            tf.keras.layers.Dense(self.num_classes, activation=last_layer_activation)
        ])
        self.model.summary()
        self.model.compile(optimizer=optimizer, loss=loss, metrics=metrics) 

    def plot_model(self):
        tf.keras.utils.plot_model(self.model, show_shapes=True)

    def fit(self, epochs, batch_size, es_patience=20):
        cp_callback = tf.keras.callbacks.ModelCheckpoint(self.model_save_path, verbose=1, save_weights_only=False)
        es_callback = tf.keras.callbacks.EarlyStopping(patience=es_patience, verbose=1)
        self.model.fit(
            self.X_train,
            self.y_train,
            epochs=epochs,
            batch_size=batch_size,
            validation_data=(self.X_test, self.y_test),
            callbacks=[cp_callback] # INSERT ES
        )
    
    def evaluate(self, batch_size):
        model = tf.keras.models.load_model(self.model_save_path)
        val_loss, val_acc = model.evaluate(self.X_test, self.y_test, batch_size=batch_size)
        return val_loss, val_acc

    def confusion_matrix(self, report=True):
        y_pred = np.argmax(self.model.predict(self.X_test), axis=1)
        labels = sorted(list(set(self.y_test)))
        cmx_data = confusion_matrix(self.y_test, y_pred, labels=labels)
        df_cmx = pd.DataFrame(cmx_data, index=labels, columns=labels)
        fig, ax = plt.subplots(figsize=(7, 6))
        sns.heatmap(df_cmx, annot=True, fmt='g', square=False)
        ax.set_ylim(len(set(self.y_test)), 0)
        plt.show()
        if report:
            print('Classification Report')
            print(classification_report(self.y_test, y_pred))

if __name__ == '__main__':
    classifier = Classifier(model_save_path = '../../assets/models/keypoints_classifier.hdf5', random_state = random_state, num_classes = num_classes, num_features = num_features)
    classifier.prepare_dataset(path = '../../assets/dataset/keypoints.csv')
    classifier.define_model(loss='sparse_categorical_crossentropy')
    classifier.fit(epochs = epochs, batch_size = batch_size)
    classifier.evaluate(batch_size = batch_size)
    classifier.confusion_matrix(report=True)