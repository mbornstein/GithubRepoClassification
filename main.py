import sklearn.cluster
import numpy as np
import pandas as pd

from metrics.githubMetrics import GithubMetrics, metricCollection
from importer.testDataImporter import TestDataImporter


'''
    Accuracy check for non DEV kMeans
    8 cluster = 0.4
    9,11,13 cluster = 0.34285
    17 cluster = 0.333333
'''
CLUSTERS = 15

metrics = list(metricCollection.keys())
kMeans = sklearn.cluster.KMeans(n_clusters=CLUSTERS)


def aggregate_data(repo_links):
    metrics_data = []
    for link in repo_links:
        github_metrics = GithubMetrics(link)
        metrics_data.append([link] + [github_metrics.get(m) for m in metrics])

    return pd.DataFrame(data=metrics_data, columns=['repo'] + metrics)


def normalize_data(data):
    metric_list = data.columns
    norm_data = pd.DataFrame({
        'avg_entropy': data['avg_entropy']
    })
    for metric in metric_list[1:]:
        norm_data[metric] = np.log(data[metric] + 1)
        norm_data[metric] = (norm_data[metric] - norm_data[metric].min()) / \
                            (norm_data[metric].max() - norm_data[metric].min())
    return norm_data


def train(data):
    X = data[metrics]
    kMeans.fit(X)
    # print('summed error:', kMeans.score(X))


def predict(x):
    return kMeans.predict(x)


def assign_cluster_classes(classification, predictions, cluster_count):
    cluster_class_distribution = [dict() for i in range(cluster_count)]
    for index in range(len(predictions)):
        cluster = predictions[index]
        category = classification[index]
        dictionary = cluster_class_distribution[cluster]
        dictionary[category] = dictionary.get(category, 0) + 1
    cluster_classes = []
    for dictionary in cluster_class_distribution:
        maximum = 0
        category = None
        for key, value in dictionary.items():
            if value > maximum:
                maximum = value
                category = key
        cluster_classes.append(category)
    return cluster_classes


class TwoStepClassifier:

    def __init__(self, model1, model2):
        self.model1 = model1
        self.model2 = model2

    def fit(self, data, y):
        dev_or_empty = np.array(['', 'DEV'])[(y == 'DEV') * 1]
        self.model1.fit(data, dev_or_empty)
        self.model2.fit(data[y != 'DEV'], y[y != 'DEV'])

    def predict(self, data):
        y_pred1 = self.model1.predict(data)
        y_pred2 = self.model2.predict(data)
        y_pred1[y_pred1 != 'DEV'] = y_pred2[y_pred1 != 'DEV']
        return y_pred1

    def score(self, data, y):
        return np.mean(self.predict(data) == y)


if __name__ == '__main__':
    importer = TestDataImporter('data/testset.csv')

    # Train
    data_train = aggregate_data(importer.trainset.repos)
    y_data_train = np.array(importer.trainset.classification)

    # filter DEV
    dev_filter_train = y_data_train != 'DEV'
    data_train = data_train[dev_filter_train]
    y_data_train = y_data_train[dev_filter_train]

    data_train = normalize_data(data_train)
    train(data_train)
    prediction = predict(data_train[metrics])

    cluster_classes = assign_cluster_classes(y_data_train, prediction, CLUSTERS)

    if len(set(cluster_classes)) < len(np.unique(y_data_train)):
        print("Warning: for some categories are no clusters available")

    for cluster in range(CLUSTERS):
        print('Cluster', cluster, 'is assigned to:', cluster_classes[cluster])

    # Test
    data_test = aggregate_data(importer.testset.repos)
    y_data_test = np.array(importer.testset.classification)

    # filter dev
    dev_filter_test = y_data_test != 'DEV'
    data_test = data_test[dev_filter_test]
    y_data_test = y_data_test[dev_filter_test]

    data_test = normalize_data(data_test)
    prediction = predict(data_test[metrics])

    correct = 0
    for i in range(len(prediction)):
        if y_data_test[i] == cluster_classes[prediction[i]]:
            correct += 1
    print('Precision:', correct / len(prediction))
    print('Null accuracy', max([len(y_data_test[y_data_test == x]) for x in np.unique(y_data_test)]) / len(y_data_test))


