
from github import Github

from config import API_TOKEN
from utility import conversion

githubClient = Github(API_TOKEN)
filename = 'data/repoURLs.txt'


def get_start_id():
    lines = open(filename, 'r').readlines()
    last_url = lines[-1].strip()
    fullname = conversion.url_to_full_name(last_url)
    return githubClient.get_repo(fullname).id

startId = get_start_id()

with open(filename, 'a') as file:
    # get_repos starts with repos after this id
    # So the last repo won't be added twice
    for repo in githubClient.get_repos(startId):
        file.write(repo.html_url + '\n')
