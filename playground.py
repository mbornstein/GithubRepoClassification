from metrics.githubMetrics import githubClient

# get repo overview
repo = githubClient.get_repo('cginternals/gloperate')
#print(dir(repo))
print('size:', repo.size)

print(repo.permissions)
print(repo.description)


#print('\nShow assigness:')
#for assignee in repo.get_assignees():
#    print(assignee)

#print('\nShow contributors:')
#for contributor in repo.get_contributors():
#    print(contributor.name)

#print('\nShow branches:')
#for branch in repo.get_branches():
#    print(branch)

#print('\nShow comments:')
#for comment in repo.get_comments():
#    print(comment.body)

#print('\nShow repo content')
#for content in repo.get_contents('/'): # get_file_contents() get_dir_contents()
#    print(content)

#print('\nShow downloads:')
#for download in repo.get_downloads():
#    print(download)

#print('\nShow forks:')
#for fork in repo.get_forks():
#    print(fork)

#print('\nShow commits')
#for commit in repo.get_commits():
#    print(commit.commit.message)

#print('\nShow readme')
#print(repo.get_readme().content)

#print('\nShow contributor statistics:')
#for stat in repo.get_stats_contributors() or []:
#    print(stat.author.login, stat.total)

#print('\nShow commit activity')
#for stat in repo.get_stats_commit_activity() or []:
#    print(stat.days)

#print('\nShow code frequency:')
#for stat in repo.get_stats_code_frequency() or []:
#    print(stat.additions, stat.deletions)

#print('\nShow participation:')
#stat = repo.get_stats_participation()
#print(sum(stat.all), sum(stat.owner))

#print('\nShow punchcard:')
#print(repo.get_stats_punch_card().get(3, 13))

