import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sklearn
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor 
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_squared_error
from sklearn.datasets import make_classification, make_regression
import random
num = random.randint(1, 150)


class Model:
    def __init__(self, model_name, model_type, problem, *arg):
        self.name = model_name
        self.problem = problem
        if model_type == 'RandomForest' and problem == 'Classification':
            self.model = RandomForestClassifier(n_estimators=arg[0], max_depth=arg[1], n_jobs=-1)
        elif model_type == 'RandomForest' and problem == 'Regression':
            self.model = RandomForestRegressor(n_estimators=arg[0], max_depth=arg[1], n_jobs=-1)
        elif model_type == 'KNN':
            if problem == 'Regression':
                self.model = KNeighborsRegressor(n_neighbors=arg[2])
            else:
                self.model = KNeighborsClassifier(n_neighbors=arg[2])
        elif model_type == 'Linear':
            if problem == 'Regression':
                self.model = LinearRegression()
            else:
                self.model = LogisticRegression()
        elif model_type == 'Tree':
            if problem == 'Regression':
                self.model = DecisionTreeRegressor(max_depth=arg[1])
            else:
                self.model = DecisionTreeClassifier(max_depth=arg[1])
        else:
            print('Неправильное имя класса')

    def fit(self, X, y):
        self.model.fit(X, y)

    def predict(self, X):
        return self.model.predict(X)

    def evaluate(self, problem, X, y):
        if problem == 'Classification':
            return accuracy_score(y, self.model.predict(X))
        else:
            return mean_squared_error(y, self.model.predict(X))

class Dataset:
    def __init__(self, problem, samples=5000, classes=0):
        self.problem = problem
        if problem == 'Regression':
            self.dataX, self.dataY = make_regression(n_samples=samples, n_features=2, random_state=42)
            self.dataY = self.dataY[:np.newaxis]
        else:
            self.dataX, self.dataY = make_classification(n_classes=2, n_features=2, n_samples=samples, random_state=42, n_redundant=0, n_repeated=0)
            self.dataY = self.dataY[:np.newaxis]
            
    def split(self, test_siz):
        return train_test_split(self.dataX, self.dataY, test_size=test_siz, random_state=42)

class FittingAndEvaluating:
    global num
    def __init__(self, model, dataset, test_siz):
        self.model = model
        self.model_name = model.name
        self.X_train, self.X_test, self.Y_train, self.Y_test = dataset.split(test_siz)

    def fitting(self):
        self.model.fit(self.X_train, self.Y_train)

    def evaluating(self):
        return self.model.evaluate(self.model.problem, self.X_test, self.Y_test)

    def pict(self):
        global num
        num += 1
        plt.scatter(self.X_train[:, 0], self.X_train[:, 1], c=self.Y_train)
        plt.savefig(f'static\img\pic{num}.png')

def all_(name, model_type, problem, tree_counts, deep, neighbours, sampless, size='0.2'):
    model = Model(name, model_type, problem, int(tree_counts), int(deep), int(neighbours))
    data = Dataset(problem, samples=int(sampless))
    result = FittingAndEvaluating(model, data, float(size))
    return result

def numzn():
    global num
    return num
