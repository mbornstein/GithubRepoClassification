from caching import CachedMetric, getFullName, githubClient

@CachedMetric
def getRepoSize(repoURL):
	print('This is actually executed')
	repo = githubClient.get_repo(getFullName(repoURL))
	return repo.size

@CachedMetric
def getWatcherCount(repoURL):
	print('This (watcher) is actually executed')
	repo = githubClient.get_repo(getFullName(repoURL))
	return repo.watchers

if __name__ == '__main__':
	repoURL = 'https://github.com/marfarma/handsoap'
	print('Repo size:', getRepoSize(repoURL))
	#print('Repo watchers:', getWatcherCount(repoURL))