import json

from metrics.githubMetrics import metricCollection


class CachedMetric(object):

    def __init__(self, f):
        metricCollection[f.__name__] = self.__call__
        self.function = f

    def __call__(self, github_metrics):
        result = cache_lookup(self.function.__name__, github_metrics)
        if result is None:
            kwargs = self.generate_arguments(github_metrics)
            result = self.function(**kwargs)
            write_to_cache(self.function.__name__, result, github_metrics)
        return result

    def generate_arguments(self, github_metrics):
        keyword_arguments = {}
        for argument, annotation in self.function.__annotations__.items():
            if annotation == 'repo_overview':
                keyword_arguments[argument] = github_metrics.get_repo_overview()
            elif annotation == 'cloned_repo_path':
                keyword_arguments[argument] = github_metrics.get_cloned_repo_path()
            else:
                raise NameError('Unknown annotation {:s} in function {:s}'.format(annotation, self.function.__name__))
        return keyword_arguments


def get_file_path(github_metrics):
    filename = github_metrics.get_escaped_full_name() + '.json'
    return 'data/repoMetrics/' + filename


def cache_lookup(metric_name, github_metrics):
    try:
        with open(get_file_path(github_metrics), 'r') as data_file:
            data = json.load(data_file)
            return data[metric_name]
    except (KeyError, FileNotFoundError):
        return None


def write_to_cache(metric_name, result, github_metrics):
    filename = get_file_path(github_metrics)
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
