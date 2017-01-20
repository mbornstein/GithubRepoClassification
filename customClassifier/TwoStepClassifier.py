import numpy as np


class TwoStepClassifier:

    def __init__(self, model1, model2):
        self.model1 = model1
        self.model2 = model2

    def fit(self, data, y):
        dev_or_empty = np.array(['NO-DEV', 'DEV'])[(y == 'DEV') * 1]
        self.model1.fit(data, dev_or_empty)
        self.model2.fit(data[y != 'DEV'], y[y != 'DEV'])

    def predict(self, data):
        y_pred1 = self.model1.predict(data)
        #print(y_pred1)
        y_pred2 = self.model2.predict(data[y_pred1 != 'DEV'])
        # print(y_pred2)
        y_pred1[y_pred1 != 'DEV'] = y_pred2
        # print(y_pred1)
        return y_pred1

    def score(self, data, y):
        return np.mean(self.predict(data) == y)

    def get_params(self, deep=True):
        return {'model1': self.model1, 'model2': self.model2}
