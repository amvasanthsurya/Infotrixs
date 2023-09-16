from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPool2D, Flatten, Dropout, Dense, MaxPooling2D
from tensorflow.keras.datasets import mnist
import numpy as np
from Confusion_matrix import confu_matrix
from keras import regularizers
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier

def cnn(X_train,Y_train,X_test,Y_test):

    # reshaping data
    X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1, 1))
    X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1, 1))


    model = Sequential()
    model.add(Conv2D(64, (1, 1), padding='valid', input_shape=X_train[1].shape, activation='relu'))
    model.add(MaxPooling2D(pool_size=(1, 1)))
    model.add(Dropout(0.2))
    model.add(Flatten())
    model.add(Dense(2, activation='softmax'))

    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.fit(X_train, Y_train, epochs=15, batch_size=400, verbose=0)
    y_predict = np.argmax(model.predict(X_test), axis=1)
    y_predict_train = np.argmax(model.predict(X_train), axis=1)
    return y_predict , confu_matrix(Y_test, y_predict,0), confu_matrix(Y_train, y_predict_train,1)

def cnn_w(X_train,Y_train,X_test,Y_test,w):

    # reshaping data
    X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1, 1))
    X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1, 1))

    model = Sequential()
    model.add(Conv2D(64, (1, 1), padding='valid', input_shape=X_train[1].shape, activation='relu'))
    model.add(MaxPooling2D(pool_size=(1, 1)))
    model.add(Dropout(0.2))
    model.add(Flatten())
    model.add(Dense(2, activation='softmax', kernel_regularizer=regularizers.l2(0.01)))
    model.add(Dropout(0.2))

    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.fit(X_train, Y_train, epochs=5, batch_size=400, verbose=0)
    weight=model.get_weights()
    weight[1]=weight[1]*w[0]
    model.set_weights(weight)
    model.fit(X_train, Y_train, epochs=5, batch_size=400, verbose=0)

    y_predict = np.argmax(model.predict(X_train), axis=1)
    return y_predict, confu_matrix(Y_train, y_predict,1)

def cnn_w_test(X_train,Y_train,X_test,Y_test,w):

    # reshaping data
    X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1, 1))
    X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1, 1))

    model = Sequential()
    model.add(Conv2D(64, (1, 1), padding='valid', input_shape=X_train[1].shape, activation='relu'))
    model.add(MaxPooling2D(pool_size=(1, 1)))
    model.add(Dropout(0.2))
    model.add(Flatten())
    model.add(Dense(2, activation='softmax', kernel_regularizer=regularizers.l2(0.01)))
    model.add(Dropout(0.2))

    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.fit(X_train, Y_train, epochs=5, batch_size=400, verbose=0)
    weight=model.get_weights()
    weight[1]=weight[1]*w[0]
    model.set_weights(weight)
    model.fit(X_train, Y_train, epochs=5, batch_size=400, verbose=0)

    y_predict = np.argmax(model.predict(X_test), axis=1)
    y_predict_train = np.argmax(model.predict(X_train), axis=1)
    return confu_matrix(Y_train, y_predict_train,1), confu_matrix(Y_test, y_predict,0)

def ann(X_train,Y_train,X_test,Y_test):

    model = Sequential()
    model.add(Dense(20, activation='softmax'))
    model.add(Dense(10, activation='softmax'))
    model.add(Dense(2, activation='softmax'))

    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.fit(X_train, Y_train, epochs=20, batch_size=100, verbose=0)
    y_predict = np.argmax(model.predict(X_test), axis=1)
    y_predict_train = np.argmax(model.predict(X_train), axis=1)
    return y_predict, confu_matrix(Y_test, y_predict,0), confu_matrix(Y_train, y_predict_train,1)

def SVM(X_train,Y_train,X_test,Y_test):
    model = svm.SVC()
    model.fit(X_train, Y_train)
    y_predict=model.predict(X_test)
    y_predict_train =model.predict(X_train)
    return y_predict, confu_matrix(Y_test, y_predict,0), confu_matrix(Y_train, y_predict_train,1)

def rf(X_train,Y_train,X_test,Y_test):
    model = RandomForestClassifier(max_depth=2, random_state=0)
    model.fit(X_train, Y_train)
    y_predict=model.predict(X_test)
    y_predict_train =model.predict(X_train)
    return y_predict, confu_matrix(Y_test, y_predict,0), confu_matrix(Y_train, y_predict_train,1)