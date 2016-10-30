import os
import json
from github import Github


API_TOKEN = '0b8801a77eaea265f203f0a4b13d3d22739a6451'
githubClient = Github(API_TOKEN)

def getRepoSize(repoURL) -> 'metric':
	fullname = getFullName(repoURL)
	filename = '../data/repoMetrics/' + str(getId(fullname)) + '.json'
	key = 'repoSize'
	data = None
	if os.path.isfile(filename):
		with open(filename) as data_file:
			data = json.load(data_file)
		if key not in data:
			data[key] = fetchRepoSize(fullname)
	else:
		data = {key: fetchRepoSize(fullname)}

	with open(filename, 'w') as outfile:
		json.dump(data, outfile)

	return data[key]

def fetchRepoSize(repoFullName):
	repo = githubClient.get_repo(repoFullName)
	return repo.size

def getFullName(repoURL):
	tokens = repoURL.split('/')
	return tokens[-2] + '/' + tokens[-1]

def getId(fullname):
	repo = githubClient.get_repo(fullname)
	return repo.id

if __name__ == '__main__':
	repoURL = 'https://github.com/marfarma/handsoap'
	print('Repo size:', getRepoSize(repoURL))