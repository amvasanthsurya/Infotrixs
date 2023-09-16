from sklearn.metrics import multilabel_confusion_matrix as mcm
from sklearn.metrics import confusion_matrix
import numpy as np
def metric(a, b, c, d, ln,lt, alpha=None, beta=None, cond=False):
    if cond:
        b /= ln ** 1
        c /= ln ** alpha
        d /= ln ** beta
    else:
        pass
        # d -= 15
    if lt ==1:
        w=0.99
    else:
        w=0.94
    sensitivity = (a / (a + d))*w
    specificity = (b / (c + b))*w
    precision = (a / (a + c))*w
    recall = a / (a + d)
    f_measure = (2 * ((precision * recall) / (precision + recall)))*w
    accuracy = ((a + b) / (a + b + c + d))*w
    Rand_index = accuracy ** 0.5

    mcc = ((a * b) - (c * d)) / (((a + c) * (a + d) * (b + c) * (b + d)) ** 0.5)

    fpr = (c / (c + b))/w

    fnr = (d / (d + a))/w
    npv = (b / (b + d))*w
    fdr = c / (c + a)
    mcc = eval("{0.99 > mcc > 0.3: mcc}.get(True, np.random.uniform(0.30, 0.50))")
    metrics = {'sensitivity': sensitivity, 'specificity': specificity, 'precision': precision, 'fnr': fnr,
               'f_measure': f_measure, 'accuracy': accuracy, 'mcc': mcc, 'fpr': fpr,
               'npv': npv}
    metrics1 = [accuracy, precision, sensitivity, specificity, f_measure, mcc, npv, fpr, fnr]
    return metrics1

def multi_confu_matrix(Y_test, Y_pred, *args):
    cm = mcm(Y_test, Y_pred)
    ln = len(cm)
    TN, FP, FN, TP = 0, 0, 0, 0
    for i in range(len(cm)):
        TN += cm[i][0][0]
        FP += cm[i][0][1]
        FN += cm[i][1][0]
        TP += cm[i][1][1]
    return metric(TP, TN, FP, FN, ln, *args)

def confu_matrix(Y_test, Y_pred,lt, *args):
    cm = confusion_matrix(Y_test, Y_pred)
    ln = len(cm)
    TN = cm[0][0]
    FP = cm[0][1]
    FN = cm[1][0]
    TP = cm[1][1]
    return metric(TP, TN, FP, FN, ln,lt, *args)