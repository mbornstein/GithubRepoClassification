from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB

from metrics.githubMetrics import GithubMetrics, metricCollection
from importer.testDataImporter import TestDataImporter

metrics = list(metricCollection.keys())


def train(log_reg, data, expected_values):
    log_reg.fit(data, expected_values)


def predict(clf, x):
    return clf.predict(x)


def getReadmeContent(repo_url):
    path = GithubMetrics(repo_url).get_cloned_repo_path()
    content = ''
    for filename in ['REAMDME.md', 'Readme.org', 'readme.txt', 'README', 'README.mkd']:
        try:
            content = open(path + '/' + filename, 'r').read()
            return content
        except FileNotFoundError:
            continue
    return content

if __name__ == '__main__':
    importer = TestDataImporter('data/testset.csv')

    train_texts = [getReadmeContent(repo_url) for repo_url in importer.trainset.repos]
    print(importer.trainset.classification)

    count_vect = CountVectorizer()
    X_train_counts = count_vect.fit_transform(train_texts)
    print('Shape:', X_train_counts.shape)

    #print(count_vect.vocabulary_.get('algorithm'))

    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

    # Train
    clf = MultinomialNB().fit(X_train_tfidf, importer.trainset.classification)

    test_texts = [getReadmeContent(repo_url) for repo_url in importer.testset.repos]
    X_new_counts = count_vect.transform(test_texts)
    X_new_tfidf = tfidf_transformer.transform(X_new_counts)

    predicted = predict(clf, X_new_tfidf)

    #for doc, category in zip(test_texts, predicted):
    #    print(doc, '=>', category)

    correct = 0
    for i in range(len(predicted)):
        if importer.testset.classification[i] == predicted[i]:
            correct += 1
    print('Accuracy:', correct / len(predicted))

    print(predicted)
