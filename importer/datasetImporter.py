import numpy as np
import pandas as pd

from metrics.githubMetrics import GithubMetrics, metricCollection
from github import GithubException


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
            self.repos = list(self.repos)

            self.target = np.array(self.target)
            self.data = self.get_data_internal()

    def get_data_internal(self):
        metrics = list(metricCollection.keys())
        metrics_data = []
        repo_links = self.repos[:]
        for link in repo_links:
            try:
                githubMetrics = GithubMetrics(link)
                metrics_data.append([githubMetrics.get(m) for m in metrics])
            except GithubException:
                print("Warning: could not load:", link)
                # remove repo from repo list and target
                index = self.repos.index(link)
                self.repos.pop(index)
                mask = np.ones(self.target.shape)
                self.target = self.target[np.arange(len(self.target)) != index]
        return pd.DataFrame(data=metrics_data, columns=metrics)

    @staticmethod
    def get_data(repo_links):
        metrics = list(metricCollection.keys())
        metrics_data = []
        for link in repo_links:
            try:
                githubMetrics = GithubMetrics(link)
                metrics_data.append([githubMetrics.get(m) for m in metrics])
            except GithubException:
                print("Warning: could not load:", link)
                # remove repo from repo list
                self.repos.remove(link)
        return pd.DataFrame(data=metrics_data, columns=metrics)
