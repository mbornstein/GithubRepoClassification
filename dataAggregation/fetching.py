
from github import Github

API_TOKEN = '0b8801a77eaea265f203f0a4b13d3d22739a6451'

githubClient = Github(API_TOKEN)

with open('../data/repoURLs.txt', 'w') as f:
	#i = 0
	for repo in githubClient.get_repos():
		f.write(repo.html_url + '\n')