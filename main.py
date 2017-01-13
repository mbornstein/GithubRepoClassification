import numpy as np
import pandas as pd

# Learning Algorithms
from TwoStepClassifier import TwoStepClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier

from metrics.githubMetrics import GithubMetrics, metricCollection
from importer.testDataImporter import TestDataImporter

metrics = list(metricCollection.keys())


def aggregate_data(repo_links):
    metrics_data = []
    for link in repo_links:
        github_metrics = GithubMetrics(link)
        metrics_data.append([link] + [github_metrics.get(m) for m in metrics])

    return pd.DataFrame(data=metrics_data, columns=['repo'] + metrics)


def get_data(repo_links):
    metrics_data = []
    for link in repo_links:
        github_metrics = GithubMetrics(link)
        metrics_data.append([github_metrics.get(m) for m in metrics])

    return pd.DataFrame(data=metrics_data, columns=metrics)


def normalize_data(data):
    metric_list = data.columns
    norm_data = pd.DataFrame({
        'avg_entropy': data['avg_entropy']
    })
    for metric in metric_list[1:]:
        norm_data[metric] = np.log(data[metric] + 1)
        norm_data[metric] = (norm_data[metric] - norm_data[metric].min()) / \
                            (norm_data[metric].max() - norm_data[metric].min())
    return norm_data


def get_accuracy(algo, train, y_train, test, y_test):
    algo.fit(train, y_train)
    return algo.score(test, y_test)


def main():
    algorithms = [
        DecisionTreeClassifier(random_state=1337),
        LogisticRegression(C=1.0, max_iter=1000, solver='lbfgs', multi_class='ovr'),
        LogisticRegression(C=1.0, max_iter=100, n_jobs=2),
        TwoStepClassifier(LogisticRegression(C=1.0, max_iter=100, n_jobs=2), RandomForestClassifier(n_estimators=100, random_state=1337)),
        SVC(C=20.0, random_state=1337),
        RandomForestClassifier(n_estimators=100, random_state=1337),
        MLPClassifier(max_iter=20000, hidden_layer_sizes=(100,), random_state=1337, shuffle=False, learning_rate='adaptive'),
        MLPClassifier(max_iter=20000, hidden_layer_sizes=(50,20), random_state=1337, shuffle=False, learning_rate='adaptive'),
    ]

    importer = TestDataImporter('data/testset.csv')

    # Train Data
    data_train = get_data(importer.trainset.repos)
    data_train = normalize_data(data_train)
    y_data_train = np.array(importer.trainset.classification)

    # Test Data
    data_test = get_data(importer.testset.repos)
    data_test = normalize_data(data_test)
    y_data_test = np.array(importer.testset.classification)

    print('Null accuracy', max([len(y_data_test[y_data_test == x]) for x in np.unique(y_data_test)]) / len(y_data_test))
    print('Accuracies:')
    for algo in algorithms:
        accuracy = get_accuracy(algo, data_train, y_data_train, data_test, y_data_test)
        print(type(algo).__name__ + ':\t', accuracy)


if __name__ == '__main__':
    main()
