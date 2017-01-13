import numpy as np


class TwoStepClassifier:

    def __init__(self, model1, model2):
        self.model1 = model1
        self.model2 = model2

    def fit(self, data, y):
        dev_or_empty = np.array(['      ', 'DEV'])[(y == 'DEV') * 1]
        self.model1.fit(data, dev_or_empty)
        print(self.model1.score(data, y))
        self.model2.fit(data[y != 'DEV'], y[y != 'DEV'])
        print(self.model2.score(data[y != 'DEV'], y[y != 'DEV']))

    def predict(self, data):
        y_pred1 = self.model1.predict(data)
        print(y_pred1)
        y_pred2 = self.model2.predict(data)
        print(y_pred2)
        y_pred1[y_pred1 != 'DEV'] = y_pred2[y_pred1 != 'DEV']
        print(y_pred1)
        return y_pred1

    def score(self, data, y):
        return np.mean(self.predict(data) == y)
