metricCollection = {}


class GithubMetrics:

    def __init__(self, repo_url):
        self.repo_url = repo_url
        self.repo_overview = None
        self.cloned_repo_path = None

    def get(self, metric):
        return metricCollection[metric](self.repo_url)
