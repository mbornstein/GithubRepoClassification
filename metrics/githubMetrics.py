import os
import subprocess

from github import Github

API_TOKEN = '0b8801a77eaea265f203f0a4b13d3d22739a6451'
githubClient = Github(API_TOKEN)
metricCollection = {}


class GithubMetrics:

    def __init__(self, repo_url):
        self.repo_url = repo_url
        self.full_name = None
        self.repo_overview = None

    def get(self, metric):
        return metricCollection[metric](self)

    def get_repo_overview(self):
        if self.repo_overview is None:
            print('request to server')
            self.repo_overview = githubClient.get_repo(self.get_full_name())
        return self.repo_overview

    def get_full_name(self):
        if self.full_name is None:
            tokens = self.repo_url.split('/')
            self.full_name = tokens[-2] + '/' + tokens[-1]
        return self.full_name

    def get_escaped_full_name(self):
        return self.get_full_name().replace('/', '#')

    def get_cloned_repo_path(self):
        path = self._get_cloned_repo_path_name()
        if not os.path.isdir(path):
            subprocess.run(['git', 'clone', self.repo_url, path])
        return path

    def _get_cloned_repo_path_name(self):
        return 'data/repos/' + self.get_escaped_full_name()
