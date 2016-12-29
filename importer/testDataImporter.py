from importer.dataset import Dataset


class TestDataImporter:

    def __init__(self, filename, ratio=0.65):
        content = open(filename, 'r').readlines()
        entries = [line.strip().split(',') for line in content]
        splitpoint = int(len(entries) * ratio)
        self.trainset = Dataset(*zip(*entries[:splitpoint]))
        self.testset = Dataset(*zip(*entries[splitpoint:]))
