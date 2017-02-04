import random
import platform
import sys
from subprocess import call

import github

explanation = """DEV​: a repository primarily used for development of a tool, component, application, app, or
API
HW​ repo: a repository primarily used for homework, assignments and other course-related
work and code
EDU​: a repository primarily used to host tutorials, lectures, educational information and
code related to teaching
DOCS: a repository primarily used for tracking and storage of non-educational documents
WEB: a repository primarily used to host static personal websites or blogs
OTHER​: use this category only if there is no strong correlation to any other repository
category, for example, empty repositories
"""

githubClient = github.Github()
FILENAME = 'data/testset.csv'
MAX_REPO_ID = 76000000
SEPARATOR = ','

if platform.system() == 'Darwin':
    command = 'open'
elif platform.system() == 'Linux':
    command = 'xdg-open'
else:
    raise NotImplementedError("Not implemented for Windows")


def read_visited_repos():
    visited_repos = set()
    try:
        with open(FILENAME, 'r') as file:
            for line in file:
                visited_repos.add(line.split(SEPARATOR)[0])
    except FileNotFoundError:
        pass
    finally:
        return set()


def tag_repo(url):
    tags = {"DEV", "HW", "EDU", "DOCS", "WEB", "DATA", "OTHER"}
    call([command, url])
    print(explanation)
    user_input = input("Classify:")
    if user_input.upper() in tags:
        return user_input.upper()
    elif user_input.upper() == 'EXIT':
        sys.exit()
    else:
        return None

if __name__ == '__main__':
    visited_repos = read_visited_repos()

    with open(FILENAME, 'a') as file:
        while True:
            try:
                repo = githubClient.get_repo(random.randrange(MAX_REPO_ID))
                url = repo.html_url
            except github.GithubException:
                # try different id
                continue
            if url in visited_repos:
                continue
            tag = tag_repo(url)
            if tag is not None:
                file.write(repo.html_url + SEPARATOR + tag + '\n')
                visited_repos.add(id)
