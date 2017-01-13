import numpy as np


class CustomKMeans:

    def __init__(self, model):
        assert(type(model).__name__ == 'KMeans')
        self.model = model
        self.cluster_classes = None

    def fit(self, data, y):
        self.model.fit(data, y)
        self._assign_cluster_classes(self.model.predict(data), y)

    def predict(self, data):
        predicted_cluster = self.model.predict(data)
        return [self.cluster_classes[x] for x in predicted_cluster]

    def score(self, data, y):
        return np.mean(self.predict(data) == y)

    def _assign_cluster_classes(self, predictions, expected):
        cluster_count = self.model.cluster_centers_.shape[0]

        cluster_class_distribution = [dict() for i in range(cluster_count)]
        for index in range(len(predictions)):
            cluster = predictions[index]
            category = expected[index]
            dictionary = cluster_class_distribution[cluster]
            dictionary[category] = dictionary.get(category, 0) + 1

        self.cluster_classes = []
        for dictionary in cluster_class_distribution:
            maximum = 0
            category = None
            for key, value in dictionary.items():
                if value > maximum:
                    maximum = value
                    category = key
            self.cluster_classes.append(category)

        if len(set(self.cluster_classes)) < len(np.unique(expected)):
            print("KMeans Warning: for some categories are no clusters available")
