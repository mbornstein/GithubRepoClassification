import re
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
    terms = ['documentation', 'docs', 'documents']
    return sum(repo.description.lower().count(term) for term in terms if repo.description) + \
           sum(repo.name.lower().count(term) for term in terms)


@CachedMetric
def intro_or_course_in_description_or_title(repo: 'repo_overview'):
    terms = ['intro', 'course']
    return sum(repo.description.lower().count(term) for term in terms if repo.description) + \
           sum(repo.name.lower().count(term) for term in terms)


@CachedMetric
def hw_in_description_or_title(repo: 'repo_overview'):
    terms = ['homework', 'assignment']
    return sum(repo.description.lower().count(term) for term in terms if repo.description) + \
           sum(repo.name.lower().count(term) for term in terms)


@CachedMetric
def is_link_in_description(repo: 'repo_overview'):
    regex = r'(ftp|https?)://[^\.]+\.[a-z]{2,4}'
    if repo.description and re.search(regex, repo.description.lower()):
        return 1
    else:
        return 0
