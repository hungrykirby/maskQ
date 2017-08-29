from sklearn.metrics import confusion_matrix
from sklearn.svm import SVC
from sklearn.utils import resample
import numpy as np
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import GridSearchCV

import os
import glob

import DataSetup

def setup():
    train_xyz, train_label, test_xyz, test_label = DataSetup.read_ceps()
    svc = SVC(kernel="linear",
        C=0.001,
        degree=3,
        gamma='auto',
        cache_size=3,
        class_weight=None,
        coef0=0.0,
        decision_function_shape=None,
        max_iter=-1,
        probability=False,
        random_state=None,
        shrinking=True,
        tol=0.001,
        verbose=False) #linear, rbf, poly

    svc.fit(train_xyz, train_label)
    prediction_label = svc.predict(test_xyz)
    cm = confusion_matrix(test_label, prediction_label)

    acc_parcent = accuracy_score(test_label, prediction_label)
    print(acc_parcent)
    print(cm)
    '''
    parameters = [{'kernel':('rbf', 'poly', 'linear'), 'C':np.logspace(-4, 4, 9), 'gamma':np.logspace(-4, 4, 9)},
              {'kearnel':('rbf', 'poly', 'linear'), 'C':np.logspace(-4, 4, 9)} ]
    svc2 = GridSearchCV(SVC(), parameters, n_jobs = -1)
    svc2.fit(train_xyz, train_label)
    '''
    return svc

def stream(svc, xyz):
    predict = svc.predict(xyz)
    #predict = len(x)
    print("predict", predict[0])
    return predict[0]
