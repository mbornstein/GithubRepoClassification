import numpy as np

import autosklearn.classification
import sklearn.metrics
from sklearn.externals import joblib

from main import get_data, normalize_data
from importer.testDataImporter import TestDataImporter


def main():
    importer = TestDataImporter('data/testset.csv')

    # Train Data
    X_train = get_data(importer.trainset.repos)
    X_train = normalize_data(X_train)
    y_train = np.array(importer.trainset.classification)

    # Test Data
    X_test = get_data(importer.testset.repos)
    X_test = normalize_data(X_test)
    y_test = np.array(importer.testset.classification)

    automl = autosklearn.classification.AutoSklearnClassifier()
    automl.fit(X_train, y_train)
    y_hat = automl.predict(X_test)
    print("Accuracy score", sklearn.metrics.accuracy_score(y_test, y_hat))

    joblib.dump(automl, 'auto_learn.pkl')
    # clf = joblib.load('auto_learn.pkl')


if __name__ == '__main__':
    main()
