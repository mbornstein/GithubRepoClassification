from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split

from metrics.githubMetrics import GithubMetrics
from importer.datasetImporter import DatasetImporter


def getReadmeContent(repo_url):
    path = GithubMetrics(repo_url).get_cloned_repo_path()
    content = ''
    for filename in ['README.md', 'Readme.org', 'readme.txt', 'README', 'README.mkd']:
        try:
            content = open(path + '/' + filename, 'r').read()
            return content
        except FileNotFoundError:
            continue
    return content

if __name__ == '__main__':
    importer = DatasetImporter('data/testset.csv')

    X = [getReadmeContent(repo_url) for repo_url in importer.repos]
    y = importer.target

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

    count_vect = CountVectorizer()
    X_train_counts = count_vect.fit_transform(X_train)
    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

    # Train
    clf = MultinomialNB().fit(X_train_tfidf, y_train)

    X_new_counts = count_vect.transform(X_test)
    X_new_tfidf = tfidf_transformer.transform(X_new_counts)

    accuracy = clf.score(X_new_tfidf, y_test)
    print('Accuracy:', accuracy)
    print('Predicted:\n', clf.predict(X_new_tfidf))
