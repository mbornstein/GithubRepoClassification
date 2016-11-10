from metrics.caching import CachedMetric, get_full_name, githubClient


@CachedMetric
def repo_size(repo_url):
    print('This is actually executed')
    repo = githubClient.get_repo(get_full_name(repo_url))
    return repo.size


@CachedMetric
def watcher_count(repo_url):
    print('This (watcher) is actually executed')
    repo = githubClient.get_repo(get_full_name(repo_url))
    return repo.watchers
