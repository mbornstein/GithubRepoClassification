
class Dataset:

    def __init__(self, repos, classifications):
        assert len(repos) == len(classifications)
        self.repos = repos
        self.classification = classifications


    def __len__(self):
        return len(self.repos)
