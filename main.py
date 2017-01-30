import sys

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, StandardScaler, minmax_scale
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

from customClassifier.TwoStepClassifier import TwoStepClassifier
from importer.datasetImporter import DatasetImporter

# We get a deadlock with the VotingClassifier when running multiple threads under mac os
if sys.platform == "darwin":
    N_JOBS = 1
else:
    N_JOBS = -1


def normalize_data(data):
    skip_log = ['avg_entropy', 'up_to_dateness', 'edu_mail_ratio']
    X_log = np.log(data + 1.0)
    X_log[skip_log] = data[skip_log]
    return pd.DataFrame(minmax_scale(X_log), columns=data.columns)


def logarithmitize(X):
    skip_log = ['avg_entropy', 'up_to_dateness', 'edu_mail_ratio']
    X_log = np.log(X + 1.0)
    X_log[skip_log] = X[skip_log]
    return X_log


def train_and_test_multiple(algos, X, y):
    print('Null accuracy', max([len(y[y == element]) for element in np.unique(y)]) / len(y))
    print('Accuracies:')

    skip_log = ['avg_entropy', 'up_to_dateness', 'edu_mail_ratio']
    X_log = np.log(X + 1.0)
    X_log[skip_log] = X[skip_log]

    for algo in algos:
        accuracy = cross_val_score(algo, X_log, y)
        if type(algo) == TwoStepClassifier:
            print(type(algo.model1).__name__, '+', type(algo.model2).__name__ + ':\t', end='')
        elif type(algo) == Pipeline:
            print(type(algo.named_steps['algo']).__name__ + ':\t', end='')
        else:
            print(type(algo).__name__ + ':\t', end='')
        print('%0.3f +/- %0.2f' % (accuracy.mean(), accuracy.std() * 2))


def learn_full(algos, importer):
    train_and_test_multiple(algos, importer.data, importer.target)


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


def test():
    print('Enter test mode: testing different learning models...')

    std_logreg = Pipeline([
        ('std', StandardScaler()),
        ('log_reg', LogisticRegression(C=1.0, max_iter=1000, solver='lbfgs', multi_class='ovr', random_state=1337))
    ])

    algorithms = [
        DecisionTreeClassifier(random_state=1337),
        # LogisticRegression(C=1.0, max_iter=1000, solver='lbfgs', multi_class='ovr', random_state=1337),
        # LogisticRegression(C=1.0, max_iter=100, n_jobs=2, random_state=1337),
        std_logreg,
        SVC(C=20.0, random_state=1337),
        RandomForestClassifier(n_estimators=100, random_state=1337),
        MLPClassifier(max_iter=20000, hidden_layer_sizes=(100,), random_state=1337, shuffle=False,
                      learning_rate='adaptive'),
        MLPClassifier(max_iter=20000, hidden_layer_sizes=(50, 20), random_state=1337, shuffle=False,
                      learning_rate='adaptive'),
        # CustomKMeans(KMeans(n_clusters=15, random_state=1337)),
        # CustomKMeans(KMeans(n_clusters=8, random_state=1337)),
        GradientBoostingClassifier(learning_rate=0.15, random_state=1337),
        VotingClassifier([('log', std_logreg),
                          ('svc', SVC(C=20.0, random_state=1337)),
                          ('rf', RandomForestClassifier(n_estimators=100, random_state=1337)),
                          ('mlp',
                           MLPClassifier(max_iter=20000, hidden_layer_sizes=(50, 20), random_state=1337, shuffle=False,
                                         learning_rate='adaptive')),
                          ('mlp2',
                           MLPClassifier(max_iter=20000, hidden_layer_sizes=(100,), random_state=1337, shuffle=False,
                                         learning_rate='adaptive')),
                          ('gb', GradientBoostingClassifier(learning_rate=0.15, random_state=1337)),
                          ], n_jobs=N_JOBS)
    ]

    algorithms = [Pipeline([
        ('range_scale', MinMaxScaler()),
        ('algo', algo)
    ]) for algo in algorithms]

    importer = DatasetImporter('data/testset_orig.csv')
    #importer = DatasetImporter('data/testset.csv')
    #bla = DatasetImporter('data/valset.csv')

    #print('\nStep 1 learning')
    # learn_step_one(algorithms, importer)
    #print('\nStep 2 learning')
    # learn_step_two(algorithms, importer)
    #print('\nFull learning without normalization')
    # learn_full_unnormalized(algorithms, importer)
    print('\nFull learning')
    learn_full(algorithms, importer)

    # use only combinations of best N if runtime is too high
    # print('\nTwo step classification:')
    # two_step_algos = [TwoStepClassifier(algo_a, algo_b) for algo_a, algo_b in itertools.product(algorithms, copy.deepcopy(algorithms))]
    # learn_full(two_step_algos, importer)

def trainAndPredict(repos):
    #print('Enter train and predict mode. It trains the model and predicts categories of the given repositories')

    std_logreg = Pipeline([
        ('std', StandardScaler()),
        ('log_reg', LogisticRegression(C=1.0, max_iter=1000, solver='lbfgs', multi_class='ovr', random_state=1337))
    ])

    #this is our final model
    vc = VotingClassifier([('log', std_logreg),
                      ('svc', SVC(C=20.0, random_state=1337)),
                      ('rf', RandomForestClassifier(n_estimators=100, random_state=1337)),
                      ('mlp',
                       MLPClassifier(max_iter=20000, hidden_layer_sizes=(50, 20), random_state=1337, shuffle=False,
                                     learning_rate='adaptive')),
                      ('mlp2',
                       MLPClassifier(max_iter=20000, hidden_layer_sizes=(100,), random_state=1337, shuffle=False,
                                     learning_rate='adaptive', warm_start=True)),
                      ('gb', GradientBoostingClassifier(learning_rate=0.15, random_state=1337, warm_start=True)),
                      ], n_jobs=N_JOBS)

    classifier = Pipeline([
        ('range_scale', MinMaxScaler()),
        ('model', vc)
    ])

    #train the classifier
    #importer = DatasetImporter('data/testset.csv')
    importer = DatasetImporter('enriched_data.csv', complete_set=True)
    classifier.fit(logarithmitize(importer.data), importer.target)

    # predict gives repositories
    repos = [repo.strip() for repo in repos if repo.strip() != '']
    prediction = classifier.predict(logarithmitize(DatasetImporter.get_data(repos)))
    for repo, category in zip(repos, prediction):
        print(repo + ', ' + category)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        test()
    else:
        repos = open(sys.argv[1], 'r').read().split('\n')
        trainAndPredict(repos)
