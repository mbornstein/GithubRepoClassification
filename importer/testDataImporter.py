
class TestDataImporter:

    def __init__(self, filename):
        content = open(filename, 'r').readlines()
        self.entries = [line.strip().split(',') for line in content]
        self.repos, self.classification = zip(*self.entries)
