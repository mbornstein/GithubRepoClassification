import sklearn.cluster
import numpy as np
import pandas as pd

from metrics.githubMetrics import GithubMetrics, metricCollection
from data.given_repos import given_repos


kMeans = sklearn.cluster.KMeans(n_clusters=6)


def get_repo_links(amount=100):
    repo_links = open('data/repoURLs.txt', 'r').readlines()[:amount]
    return [link.strip() for link in repo_links]


def aggregate_data(data_size=100):
    given_repo_links, _ = given_repos
    repo_links = get_repo_links(data_size) + given_repo_links
    metric_list = list(metricCollection.keys())

    data = []
    for link in repo_links:
        github_metrics = GithubMetrics(link)
        data.append([link] + [github_metrics.get(m) for m in metric_list])

    return pd.DataFrame(data=data, columns=['repo'] + metric_list)


def train(data):
    X = data[metrics]
    kMeans.fit(X)
    print('summed error:', kMeans.score(X))


def predict(x):
    return kMeans.predict(x)


# metrics = GithubMetrics('https://github.com/marfarma/handsoap')
# print('Repo size:', metrics.get('repo_size'))
# print('Watcher count:', metrics.get('watcher_count'))

if __name__ == '__main__':
    metrics = list(metricCollection.keys())
    data = aggregate_data(data_size=100)
    print(data)

    train(data)
    Y_ = predict(data[metrics])
    print(Y_)

    _, known_Y = given_repos
    known_Y = np.array(known_Y)
    predicted_Y = Y_[:30]

    for cluster in np.unique(predicted_Y):
        positions_of_occurrence = np.argwhere(predicted_Y == cluster).transpose()[0]
        possible_classes = known_Y[positions_of_occurrence]
        print('cluster', cluster, 'has possible classes:', possible_classes)