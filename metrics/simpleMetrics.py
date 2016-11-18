from metrics.caching import CachedMetric


@CachedMetric
def repo_size(repo: 'repo_overview'):
    return repo.size


@CachedMetric
def watcher_count(repo: 'repo_overview'):
    return repo.watchers
