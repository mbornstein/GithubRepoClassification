import sklearn.cluster
import numpy as np
import pandas as pd

from metrics.githubMetrics import GithubMetrics, metricCollection
from importer.testDataImporter import TestDataImporter

CLUSTERS = 6

metrics = list(metricCollection.keys())
kMeans = sklearn.cluster.KMeans(n_clusters=CLUSTERS)


def get_repo_links(amount=100):
    repo_links = open('data/repoURLs.txt', 'r').readlines()[:amount]
    return [link.strip() for link in repo_links]


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
    print('summed error:', kMeans.score(X))


def predict(x):
    return kMeans.predict(x)


if __name__ == '__main__':
    importer = TestDataImporter('data/testset.csv')
    data = aggregate_data(importer.repos)
    #print(data)
    data = normalize_data(data)
    print(data)

    train(data)
    prediction = predict(data[metrics])

    for cluster in range(CLUSTERS):
        positions_of_occurrence = np.argwhere(prediction == cluster).transpose()[0]
        possible_classes = [importer.classification[position] for position in positions_of_occurrence]
        print('Cluster', cluster, 'has possible classes:', possible_classes)
