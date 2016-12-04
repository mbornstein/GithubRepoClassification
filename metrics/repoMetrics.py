import os

from metrics.caching import CachedMetric


@CachedMetric
def file_count(repo_path: 'cloned_repo_path'):
    count = 0
    for directory, subdirectories, files in os.walk(repo_path):
        count += len(files)
    return count


@CachedMetric
def file_folder_ratio(repo_path: 'cloned_repo_path'):
    folder_count = 1
    files_count = 0
    for directory, subdirectories, files in os.walk(repo_path):
        files_count += len(files)
        folder_count += len(subdirectories)
    return files_count / folder_count

