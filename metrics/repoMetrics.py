import os
import entropy

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
    for directory, subdirectories, files in os.walk(repo_path):
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
    read_max_bytes = 2**13  # 8192
    count = 0
    sum_entropy = 0

    for directory, subdirectories, files in os.walk(repo_path):
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

    return sum_entropy / count
