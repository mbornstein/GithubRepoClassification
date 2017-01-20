import numpy as np
import pandas as pd
import itertools
import copy

# learning algorithms
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingClassifier
from customClassifier.kmeans import CustomKMeans
from customClassifier.TwoStepClassifier import TwoStepClassifier
from sklearn.model_selection import cross_val_score

from importer.datasetImporter import DatasetImporter
from metrics.githubMetrics import GithubMetrics, metricCollection

metrics = list(metricCollection.keys())


def aggregate_data(repo_links):
    metrics_data = []
    for link in repo_links:
        github_metrics = GithubMetrics(link)
        metrics_data.append([link] + [github_metrics.get(m) for m in metrics])

    return pd.DataFrame(data=metrics_data, columns=['repo'] + metrics)


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


def train_and_test_multiple(algos, X, y):
    print('Null accuracy', max([len(y[y == element]) for element in np.unique(y)]) / len(y))
    print('Accuracies:')
    for algo in algos:
        accuracy = cross_val_score(algo, X, y)
        if type(algo) == TwoStepClassifier:
            print(type(algo.model1).__name__, '+', type(algo.model2).__name__ + ':\t', end='')
        else:
            print(type(algo).__name__ + ':\t', end='')
        print('%0.3f +/- %0.2f' % (accuracy.mean(), accuracy.std() * 2))


def learn_full(algos, importer):
    train_and_test_multiple(algos, normalize_data(importer.data), importer.target)


def learn_full_unnormalized(algos, importer):
    train_and_test_multiple(algos, importer.data, importer.target)


def learn_step_one(algos, importer):
    X = normalize_data(importer.data)
    y = np.array(['NO-DEV', 'DEV'])[(importer.target == 'DEV') * 1]
    train_and_test_multiple(algos, X, y)


def learn_step_two(algos, importer):
    y = importer.target[importer.target != 'DEV']
    X = normalize_data(importer.data)[importer.target != 'DEV']
    train_and_test_multiple(algos, X, y)


def main():

    algorithms = [
        DecisionTreeClassifier(random_state=1337),
        LogisticRegression(C=1.0, max_iter=1000, solver='lbfgs', multi_class='ovr', random_state=1337),
        LogisticRegression(C=1.0, max_iter=100, n_jobs=2, random_state=1337),
        SVC(C=20.0, random_state=1337),
        RandomForestClassifier(n_estimators=100, random_state=1337),
        MLPClassifier(max_iter=20000, hidden_layer_sizes=(100,), random_state=1337, shuffle=False, learning_rate='adaptive'),
        MLPClassifier(max_iter=20000, hidden_layer_sizes=(50,20), random_state=1337, shuffle=False, learning_rate='adaptive'),
        CustomKMeans(KMeans(n_clusters=15, random_state=1337)),
        CustomKMeans(KMeans(n_clusters=8, random_state=1337)),
        GradientBoostingClassifier(learning_rate=0.15, random_state=1337),
    ]

    importer = DatasetImporter('data/testset.csv')

    print('\nStep 1 learning')
    learn_step_one(algorithms, importer)
    print('\nStep 2 learning')
    learn_step_two(algorithms, importer)
    print('\nFull learning without normalization')
    learn_full_unnormalized(algorithms, importer)
    print('\nFull learning')
    learn_full(algorithms, importer)

    # use only combinations of best N if runtime is too high
    #print('\nTwo step classification:')
    #two_step_algos = [TwoStepClassifier(algo_a, algo_b) for algo_a, algo_b in itertools.product(algorithms, copy.deepcopy(algorithms))]
    #learn_full(two_step_algos, importer)


if __name__ == '__main__':
    main()
