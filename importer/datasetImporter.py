import numpy as np
import pandas as pd

from metrics.githubMetrics import GithubMetrics, metricCollection


class DatasetImporter:

    def __init__(self, filename):
        content = open(filename, 'r').readlines()
        self.repos, self.target = zip(*[line.strip().split(',') for line in content])

        self.target = np.array(self.target)
        self.data = self._get_data(self.repos)

    @staticmethod
    def _get_data(repo_links):
        metrics = list(metricCollection.keys())
        metrics_data = []
        for link in repo_links:
            metrics_data.append([GithubMetrics(link).get(m) for m in metrics])
        return pd.DataFrame(data=metrics_data, columns=metrics)
