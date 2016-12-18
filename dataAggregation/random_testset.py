import random

import github

API_TOKEN = '0b8801a77eaea265f203f0a4b13d3d22739a6451'

githubClient = github.Github(API_TOKEN)
MAX_REPO_ID = 76000000

with open('../data/extendedTestSet.txt', 'w') as f:
	repo_count = 0
	used_repos = set()

	while repo_count < 100:
		id = random.randrange(MAX_REPO_ID)
		if id in used_repos:
			continue
		try:
			repo = githubClient.get_repo(id)
			#print(repo.html_url)
			f.write(repo.html_url + '\n')
			repo_count += 1
			used_repos.add(id)
		except github.GithubException:
			# ignore invalid repo
			pass