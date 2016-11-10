import json
from github import Github

from metrics.metricsbla import metricCollection

API_TOKEN = '0b8801a77eaea265f203f0a4b13d3d22739a6451'
githubClient = Github(API_TOKEN)


class CachedMetric(object):

    def __init__(self, f):
        metricCollection[f.__name__] = f
        self.function = f

    def __call__(self, *args, **kwargs):
        result = cache_lookup(self.function.__name__, args[0])
        if result == None:
            result = self.function(*args, **kwargs)
            write_to_cache(self.function.__name__, result, args[0])
        return result


def get_filepath(repo_url):
    filename = get_full_name(repo_url).replace('/', '#') + '.json'
    return 'data/repoMetrics/' + filename


def cache_lookup(metric_name, repoURL):
    try:
        with open(get_filepath(repoURL), 'r') as data_file:
            data = json.load(data_file)
            return data[metric_name]
    except (KeyError, FileNotFoundError):
        return None


def write_to_cache(metric_name, result, repo_url):
    filename = get_filepath(repo_url)
    data = {}
    try:
        with open(filename, 'r') as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        # use empty dictionary
        pass
    data[metric_name] = result
    with open(filename, 'w') as data_file:
            json.dump(data, data_file)


def get_full_name(repo_url):
    tokens = repo_url.split('/')
    return tokens[-2] + '/' + tokens[-1]
