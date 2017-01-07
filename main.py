import sklearn.cluster
import numpy as np
import pandas as pd

from metrics.githubMetrics import GithubMetrics, metricCollection
from importer.testDataImporter import TestDataImporter

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


if __name__ == '__main__':
    importer = TestDataImporter('data/testset.csv')

    # Train
    data = aggregate_data(importer.trainset.repos)
    data = normalize_data(data)
    train(data)
    prediction = predict(data[metrics])

    cluster_classes = assign_cluster_classes(importer.trainset.classification, prediction, CLUSTERS)

    if len(set(cluster_classes)) < len(set(importer.trainset.classification)):
        print("Warning: for some categories are no clusters available")

    for cluster in range(CLUSTERS):
        print('Cluster', cluster, 'is assigned to:', cluster_classes[cluster])

    # Test
    data = aggregate_data(importer.testset.repos)
    data = normalize_data(data)
    prediction = predict(data[metrics])

    correct = 0
    for i in range(len(prediction)):
        if importer.testset.classification[i] == cluster_classes[prediction[i]]:
            correct += 1
    print('Precision:', correct / len(prediction))


