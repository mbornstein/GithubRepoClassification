from datetime import datetime

from metrics.caching import CachedMetric


@CachedMetric
def repo_size(repo: 'repo_overview'):
    return repo.size


@CachedMetric
def watcher_count(repo: 'repo_overview'):
    return repo.watchers


@CachedMetric
def forks_count(repo: 'repo_overview'):
    return repo.forks_count


@CachedMetric
def open_issue_count(repo: 'repo_overview'):
    return repo.open_issues


@CachedMetric
def up_to_dateness(repo: 'repo_overview'):
    return (datetime.now() - repo.pushed_at).total_seconds()

@CachedMetric
def doc_in_description_or_title(repo: 'repo_overview'):
    terms = ['documentation', 'docs']
    return sum(repo.description.lower().count(term) for term in terms if repo.description) + \
           sum(repo.name.lower().count(term) for term in terms)
