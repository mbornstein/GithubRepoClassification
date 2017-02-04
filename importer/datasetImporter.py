import numpy as np
import pandas as pd

from metrics.githubMetrics import GithubMetrics, metricCollection


class DatasetImporter:

    def __init__(self, filename, complete_set=False):
        if complete_set:
            df = pd.read_csv(filename)
            self.repos = df['repo']
            self.target = df['y']
            self.data = df.iloc[:,3:]
        else:
            content = open(filename, 'r').read().strip().split('\n')
            self.repos, self.target = zip(*[line.strip().split(',') for line in content])

            self.target = np.array(self.target)
            self.data = self.get_data(self.repos)

    @staticmethod
    def get_data(repo_links):
        metrics = list(metricCollection.keys())
        metrics_data = []
        for link in repo_links:
            githubMetrics = GithubMetrics(link)
            metrics_data.append([githubMetrics.get(m) for m in metrics])
        return pd.DataFrame(data=metrics_data, columns=metrics)
