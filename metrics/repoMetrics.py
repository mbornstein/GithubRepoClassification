import os
import entropy

from metrics.caching import CachedMetric

import subprocess
from .edu_mails import is_edu_mail

# like os.walk but ignores .git directory
def walk(path):
    for directory, subdirectories, files in os.walk(path):
        if not directory.startswith(path + '/.git'):
            yield directory, subdirectories, files


@CachedMetric
def file_count(repo_path: 'cloned_repo_path'):
    count = 0
    for directory, subdirectories, files in walk(repo_path):
        count += len(files)
    return count


@CachedMetric
def file_folder_ratio(repo_path: 'cloned_repo_path'):
    folder_count = 1
    files_count = 0
    for directory, subdirectories, files in walk(repo_path):
        files_count += len(files)
        folder_count += len(subdirectories)
    return files_count / folder_count


@CachedMetric
def avg_folder_depth(repo_path: 'cloned_repo_path'):
    class DirNode:
        def __init__(self, parent=None):
            self.depth = 0
            self.is_leaf = True
            if parent:
                self.depth = parent.depth + 1
                parent.is_leaf = False

    # Build Directory Tree
    dir_nodes = {}
    for directory, subdirectories, files in walk(repo_path):
        if directory in dir_nodes:
            parent_node = dir_nodes[directory]
        else:
            parent_node = DirNode()
            dir_nodes[directory] = parent_node

        for subdir in subdirectories:
            subdir = os.path.join(directory, subdir)
            if subdir not in dir_nodes:
                dir_nodes[subdir] = DirNode(parent=parent_node)

    # Iterate over all leaves (leaf is a folder with no folders) and calculate average depth
    leaves = [d.depth for d in dir_nodes.values() if d.is_leaf]
    return sum(leaves) / len(leaves)


@CachedMetric
def avg_entropy(repo_path: 'cloned_repo_path'):
    read_max_bytes = 2 ** 13  # 8192
    count = 0
    sum_entropy = 0

    for directory, subdirectories, files in walk(repo_path):
        for filename in files:
            try:
                file_bytes = open(os.path.join(directory, filename), 'rb').read(read_max_bytes)
                sum_entropy += entropy.shannon_entropy(file_bytes)
                count += 1
            except FileNotFoundError:
                # symbolic links to non existing files throw errors
                pass
            except OSError:
                # ignore Too many levels of symbolic links error
                pass

    if count == 0:
        return 0.0
    return sum_entropy / count


@CachedMetric
def is_io_page(repo: 'repo_overview'):
    if repo.name.endswith('github.io'):
        return 1
    else:
        return 0


def execute_in_dir(func, dir):
    old_pwd = os.getcwd()
    os.chdir(dir)
    result = func()
    os.chdir(old_pwd)
    return result


@CachedMetric
def edu_mail_ratio(repo_path: 'cloned_repo_path'):
    """
    checking for edu mails using the domains from:
    https://github.com/leereilly/swot
    :param repo_path:
    :return:
    """
    def git_list_contributor_mails():
        return subprocess.check_output('git log --format="%ae" | sort | uniq', shell=True).decode('utf-8', errors='ignore')

    result = execute_in_dir(git_list_contributor_mails, repo_path)
    mails = [line for line in result.split('\n') if line != '']
    return sum(is_edu_mail(mail) for mail in mails) / len(mails) if mails else 0.0


@CachedMetric
def hw_terminology_commits(repo_path: 'cloned_repo_path'):
    common_terms = ['exercise', 'assignment', 'question', 'task', 'course', 'homework', 'student']

    def git_list_commit_messages():
        return subprocess.check_output('git log --format="%s" | tee', shell=True).decode('utf-8', errors='ignore')

    commit_messages = execute_in_dir(git_list_commit_messages, repo_path)
    commit_messages = commit_messages.lower()
    return sum(commit_messages.count(term) for term in common_terms)


@CachedMetric
def hw_terminology_files(repo_path: 'cloned_repo_path'):
    common_terms = ['exercise', 'assignment', 'question', 'task', 'course', 'homework', 'student']
    count = 0
    for _, _, files in walk(repo_path):
        for file in files:
            file = file.lower()
            if any(common_term in file for common_term in common_terms):
                count += 1
    return count


@CachedMetric
def doc_terms_in_readme(repo_path: 'cloned_repo_path'):
    readme_files = [e.lower() for e in ['README.md', 'Readme.org', 'readme.txt', 'README', 'README.mkd']]
    common_terms = ['documentation', 'usage', 'guide', 'installation', 'getting started', 'quickstart', 'tutorial', 'setup']
    count = 0
    for directory, _, files in walk(repo_path):
        for file in files:
            if file.lower() in readme_files:
                try:
                    file_content = open(os.path.join(directory, file), 'rb').read().decode('utf-8', errors='ignore')
                    count += sum(file_content.count(term) for term in common_terms)
                except FileNotFoundError:
                    # happens on sym links
                    pass

    return count


def count_file_with_ending(repo_path, ending, absolute=False):
    file_count = 0
    count = 0
    for _, _, files in walk(repo_path):
        for file in files:
            file_count += 1
            if file.endswith(ending):
                count += 1
    if absolute:
        file_count = 1
    return count / file_count if file_count != 0 else 0.0


@CachedMetric
def html_count(repo_path: 'cloned_repo_path'):
    return count_file_with_ending(repo_path, '.html')


@CachedMetric
def png_count(repo_path: 'cloned_repo_path'):
    return count_file_with_ending(repo_path, '.png')


@CachedMetric
def md_count(repo_path: 'cloned_repo_path'):
    return count_file_with_ending(repo_path, '.md', absolute=True)


@CachedMetric
def pdf_count(repo_path: 'cloned_repo_path'):
    return count_file_with_ending(repo_path, '.pdf')
