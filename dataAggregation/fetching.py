
from github import Github

githubClient = Github()
print(dir(githubClient))
for repo in githubClient.get_repos():
	print(repo.name)
	break