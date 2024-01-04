# -*- coding: utf-8 -*-
"""Copy of Cancer_Prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/167o0R93HSN1FD6WZNIqP5ED3jVd2I_uH

# **CANCER PREDICTION MODEL**

**Aditya Shrivastava**


This is an ML-based aproach to perform detect Malignant or Benign cancer and finding out the accuracy of the model.
"""



import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np

#uploading the dataset
from google.colab import files
uploaded = files.upload()

#reading the dataset as a pandas dataframe
df = pd.read_csv("data.csv")

#checking for null values
print(df.isnull().sum())

print(df.describe)

#renaming dataset to label
df = df.rename(columns = {'diagnosis':'label'})
print(df.dtypes)

#a deeper look into data
sns.countplot(x="label", data=df) #where M is malignant and B is benign

#replacing categorical values with numbers
print("distribution of data: ", df['label'].value_counts())

#defining the dependant variable that needs to be predicted (labels)
y = df["label"].values
print("Labels before encoding: ", np.unique(y))

#encoding categorical data from text (B and M) to integers (0 and 1)
from sklearn.preprocessing import LabelEncoder
labelencoder = LabelEncoder()
Y = labelencoder.fit_transform(y) #here M is 1 and B is 0
print("Labels after encoding are: ", np.unique(Y))

#defining x and normalizing / scaling values
#defining the independant variables
#dropping label and ID, and normalize other data
X = df.drop(labels = ["label", "id"], axis = 1)
print(X.describe().T) #unscaled

#scaling/normalizing the values to bring them to similar range
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
scaler.fit(X)
X = scaler.transform(X)
print(X) #scaled

#splitting data into train and test
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.25, random_state=42)
print("Shape of training data is: ", X_train.shape)
print("Shape of testing data is: ", X_test.shape)

from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout

model = Sequential()
model.add(Dense(16, input_dim=30, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(1))
model.add(Activation('sigmoid'))
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
print(model.summary())

#fitting with no early stopping or other callbacks
history = model.fit(X_train, y_train, verbose=1, epochs=100, batch_size=64,
                    validation_data=(X_test, y_test))

#plotting the training and validation accuracy and loss at each epoch
loss = history.history['loss']
val_loss = history.history['val_loss']
epochs = range(1, len(loss) + 1)
plt.plot(epochs, loss, 'y', label='Training loss')
plt.plot(epochs, val_loss, 'r', label='Validation loss')
plt.title('Training and validation loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()


acc = history.history['accuracy']  #Use accuracy if acc doesn't work
val_acc = history.history['val_accuracy']  #Use val_accuracy if acc doesn't work
plt.plot(epochs, acc, 'y', label='Training acc')
plt.plot(epochs, val_acc, 'r', label='Validation acc')
plt.title('Training and validation accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.show()

#predicting the Test set results
y_pred = model.predict(X_test)
y_pred = (y_pred > 0.5)

#making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)

sns.heatmap(cm, annot=True)