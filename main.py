import sklearn.cluster

from metrics.githubMetrics import GithubMetrics

metrics = GithubMetrics('https://github.com/marfarma/handsoap')
print('Repo size:', metrics.get('repo_size'))
print('Watcher count:', metrics.get('watcher_count'))

kMeans = sklearn.cluster.KMeans(n_clusters=6)


def aggregate_data():
    return 0


def train():
    x = aggregate_data()
    kMeans.fit(x)


def predict(x):
    return kMeans.predict(x)
