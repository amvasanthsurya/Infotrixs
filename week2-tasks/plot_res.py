import numpy as np
import pandas as pd
from load_save import *
import matplotlib.pyplot as plt
from classifier import cnn_w_test
from sklearn import metrics

def bar_plot(label, data1, data2, data3, metric):

    # create data
    df = pd.DataFrame([data1, data2, data3],
                      columns=label)
    df1 = pd.DataFrame()
    df1['Dataset'] = [1, 2, 3]
    df = pd.concat((df1, df), axis=1)
    # plot grouped bar chart
    df.plot(x='Dataset',
            kind='bar',
            stacked=False)

    plt.ylabel(metric)
    plt.legend(loc='lower right')
    plt.savefig('./Results/'+metric+'.png', dpi=400)
    plt.show(block=False)




def evaluate(X_train, y_train, X_test, y_test,soln):
    met_train, met_test = cnn_w_test(X_train, y_train, X_test, y_test, soln)
    return np.array(met_train), np.array(met_test)

def plot_res():


    X_train = load('X_train')
    X_test = load('X_test')
    y_train = load('y_train')
    y_test = load('y_test')

    metrices=load('metrices')
    print(metrices)
    metrices_train = load('metrices_train')
    mthod=['ANN', 'CNN', 'RF', 'BWO-ANN']
    metrices_plot=['Accuracy', 'Precision', 'Sensitivity', 'Specificity', 'F-Measure', 'MCC', 'NPV', 'FPR', 'FNR']

    # Bar plot
    for i in range(len(metrices_plot)):
        bar_plot(mthod, metrices[0][i,:], metrices[1][i,:], metrices[2][i,:], metrices_plot[i])

    for i in range(3):
        # Table
        print('Testing Metrices-Dataset '+ str(i+1))
        tab=pd.DataFrame(metrices[i], index=metrices_plot, columns=mthod)
        print(tab)

        # Table
        print('Training Metrices-Dataset '+ str(i+1))
        tab = pd.DataFrame(metrices_train[i], index=metrices_plot, columns=mthod)
        print(tab)

    y_pred = load('y_pred')
    auc = metrics.roc_auc_score(y_test[0], y_pred)

    false_positive_rate, true_positive_rate, thresolds = metrics.roc_curve(y_test[0], y_pred)

    plt.figure(figsize=(10, 8), dpi=100)
    plt.axis('scaled')
    plt.xlim([0, 1])
    plt.ylim([0, 1])
    plt.title("AUC & ROC Curve")
    plt.plot(false_positive_rate, true_positive_rate, 'g')
    plt.fill_between(false_positive_rate, true_positive_rate, facecolor='lightgreen', alpha=0.7)
    plt.text(0.95, 0.05, 'AUC = %0.4f' % auc, ha='right', fontsize=12, weight='bold', color='blue')
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.savefig('./Results/roc.png', dpi=400)

    plt.show()

plot_res()
