from sklearn.metrics import confusion_matrix
from sklearn.svm import SVC
from sklearn.utils import resample
import numpy as np
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import GridSearchCV

import os
import glob

import DataSetup

def start():
    train_xyz, train_label, test_xyz, test_label = DataSetup.read_ceps()

    parameters = [
    {'C': [0.001, 0.01, 0.1, 1, 10, 100, 1000], 'kernel': ['linear'], 'cache_size':[3, 10, 50, 100, 200, 400, 1000]},
    {'C': [0.001, 0.01, 0.1, 1, 10, 100, 1000], 'kernel': ['rbf'], 'gamma': [1.0, 0.1, 0.01, 0.001, 0.0001], 'cache_size':[10, 50, 100, 200, 400, 1000]},
    {'C': [0.001, 0.01, 0.1, 1, 10, 100, 1000], 'kernel': ['poly'], 'degree': [2, 3, 4], 'gamma': [1.0, 0.1, 0.01, 0.001, 0.0001], 'cache_size':[10, 50, 100, 200, 400, 1000]},
    {'C': [0.001, 0.01, 0.1, 1, 10, 100, 1000], 'kernel': ['sigmoid'], 'gamma': [1.0, 0.1, 0.01, 0.001, 0.0001], 'cache_size':[10, 50, 100, 200, 400, 1000]}
    ]
    svc = GridSearchCV(SVC(), parameters)
    svc.fit(train_xyz, train_label)
    sorted(svc.cv_results_.keys())
    print("finished!", svc.best_estimator_)

if __name__ == '__main__':
    start()
