import sklearn.cluster
from sklearn.linear_model import LogisticRegression
import numpy as np
import pandas as pd

from main import aggregate_data, normalize_data
from metrics.githubMetrics import GithubMetrics, metricCollection
from importer.testDataImporter import TestDataImporter

metrics = list(metricCollection.keys())


def train(log_reg, data, expected_values):
    log_reg.fit(data, expected_values)


def predict(log_reg, x):
    return log_reg.predict(x)


if __name__ == '__main__':
    importer = TestDataImporter('data/testset.csv')
    log_reg = LogisticRegression(C=1.0, max_iter=100, solver='lbfgs', multi_class='multinomial', n_jobs=2)

    # Train
    data = aggregate_data(importer.trainset.repos)
    # data = normalize_data(data)
    train(log_reg, data[metrics], importer.trainset.classification)
    prediction = predict(log_reg, data[metrics])

    # Test
    data = aggregate_data(importer.testset.repos)
    data = normalize_data(data)
    prediction = predict(log_reg, data[metrics])

    correct = 0
    for i in range(len(prediction)):
        if importer.testset.classification[i] == prediction[i]:
            correct += 1
    print('Accuracy:', correct / len(prediction))
    print('Null Accuracy:', len([x for x in importer.testset.classification if x == 'DEV']) / len(importer.testset.classification))

    #print(log_reg.coef_)
    #print(log_reg.predict_proba(data[metrics][:5]))

    #for cat in np.unique(importer.testset.classification):
    #    print(cat, importer.testset.classification.count(cat))
