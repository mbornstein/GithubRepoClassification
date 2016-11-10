import sklearn.cluster

from metrics import metricsbla
print("main", metricsbla.metricCollection)
repoURL = 'https://github.com/marfarma/handsoap'
print('Repo size:', metricsbla.metricCollection['repo_size'](repoURL))

kMeans = sklearn.cluster.KMeans(n_clusters=6)


def aggregate_data():
    return 0


def train():
    x = aggregate_data()
    kMeans.fit(x)


def predict(x):
    return kMeans.predict(x)
