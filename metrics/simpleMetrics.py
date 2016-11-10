from metrics.caching import CachedMetric, getFullName, githubClient


@CachedMetric
def repo_size(repo_url):
    print('This is actually executed')
    repo = githubClient.get_repo(getFullName(repo_url))
    return repo.size


@CachedMetric
def watcher_count(repo_url):
    print('This (watcher) is actually executed')
    repo = githubClient.get_repo(getFullName(repo_url))
    return repo.watchers
