import os

from metrics.caching import CachedMetric


@CachedMetric
def file_count(repo_path: 'cloned_repo_path'):
    count = 0
    for directory, subdirectories, files in os.walk(repo_path):
        count += len(files)
    return count
