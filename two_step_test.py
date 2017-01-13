import numpy as np
import sklearn
from sklearn.ensemble import RandomForestClassifier

import TwoStepClassifier

from main import aggregate_data, normalize_data
from metrics.githubMetrics import metricCollection
from importer.testDataImporter import TestDataImporter

importer = TestDataImporter('data/testset.csv')

y_train = np.array(importer.trainset.classification)
y_test = np.array(importer.testset.classification)

metrics = np.array(list(metricCollection.keys()))

data_train = aggregate_data(importer.trainset.repos)
data_train = data_train[metrics]
data_train = normalize_data(data_train)

data_test = aggregate_data(importer.testset.repos)
data_test = data_test[metrics]
data_test = normalize_data(data_test)


tsc = TwoStepClassifier.TwoStepClassifier(
    sklearn.linear_model.LogisticRegression(C=1.0, max_iter=100, n_jobs=2),
    RandomForestClassifier(n_estimators=100, random_state=1337)
)
tsc.fit(data_train, y_train)
print(tsc.score(data_test, y_test))
print(y_test)
