import statistics
import numpy as np
import pandas as pd
from PSO import BasePSO
from load_save import *
from objective_function import obj_fun1
from sklearn.model_selection import train_test_split


def feat_extract(data):
    feat = np.empty([data.shape[0], data.shape[1] + 3])
    feat[0:data.shape[0], 0:data.shape[1]] = data
    # Data Cleaning and dummy variable for nan
    data = np.nan_to_num(data)
    for i in range(data.shape[1]):
        # Standard Deviation
        feat[i, data.shape[1]] = statistics.stdev(data[i, :])
        feat[i, data.shape[1] + 1] = statistics.mean(data[i, :])
        feat[i, data.shape[1] + 2] = statistics.mode(data[i, :])

    # Normalization
    feat = feat / np.max(feat, axis=0)
    # Data Cleaning and dummy variable for nan
    feat = np.nan_to_num(feat)
    return feat


def datagen():
    feat, label = [],[]
    # Datasei 1
    data = pd.read_excel('./Dataset/dataset1.xlsx')
    data=data.replace('BENIGN',0)
    data = data.replace('DDoS LOIT', 1)
    data = pd.DataFrame.to_numpy(data)
    label.append(data[:,-1].astype('int16'))
    data = np.delete(data, 111, axis=1)


    feat.append(feat_extract(data))

    # Dataset 2
    data = pd.read_excel('./Dataset/dataset2.xlsx').drop('Timestamp', axis=1)
    data = data.replace('Benign', 0)
    data = data.replace('FTP-BruteForce', 1)
    data = pd.DataFrame.to_numpy(data)
    label.append(data[:, -1].astype('int16'))
    data = np.delete(data, 78, axis=1)
    feat.append(feat_extract(data))

    # Datasei 3
    data = pd.read_excel('./Dataset/dataset3.xlsx').drop(['Flow ID', ' Source IP', ' Destination IP',' Timestamp'], axis=1)
    data = data.replace('BENIGN', 0)
    data = data.replace('TFTP', 1)
    data = pd.DataFrame.to_numpy(data)
    label.append(data[:, -1].astype('int16'))
    data = np.delete(data, 82, axis=1)
    feat.append(feat_extract(data))


    # Train and test data split
    # split into train test sets
    feat_sel_best_pos, train_data, test_data, train_lab, test_lab=[],[],[],[],[]
    for i in range(3):

        X_train, X_test, y_train, y_test = train_test_split(feat[i], label[i], test_size=0.3)

        save('feat_sel_X_train', X_train)
        save('feat_sel_X_test', X_test)
        save('cur_y_train', y_train)
        save('cur_y_test', y_test)


        # feature Selection using Qpso
        lb=(np.zeros([1, X_train.shape[1]]).astype('int16')).tolist()[0]
        ub=(np.ones([1, X_train.shape[1]]).astype('int16')).tolist()[0]
        problem_dict1 = {"fit_func": obj_fun1,
        "lb": lb,
        "ub": ub,
        "minmax": "min"}
        epoch = 2
        pop_size = 10
        model = BasePSO(problem_dict1, epoch, pop_size)
        best_position, best_fitness = model.solve()
        feat_sel_best_pos.append(best_position)

        ## Feature selection data
        best_position = np.round(best_position)
        X_train = X_train[:, np.where(best_position == 1)[0]]
        X_test = X_test[:, np.where(best_position == 1)[0]]

        train_data.append(X_train)
        test_data.append(X_test)
        train_lab.append(y_train)
        test_lab.append(y_test)
    save('X_train', train_data)
    save('X_test', test_data)
    save('y_train', train_lab)
    save('y_test', test_lab)
    save('feat_sel_best_pos', feat_sel_best_pos)

datagen()