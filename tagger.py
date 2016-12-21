import random
import platform
from subprocess import call

import github

from config import API_TOKEN

explanation = """DEV: Repositories für die Entwicklung eines Tools, einer Softwareanwendung, einer App, einer Bibliothek, einer API, oder ähnliche Softwareentwicklungsprojekte

HW: Repositories mit Lösungen und Quelltexten für Hausaufgaben und Übungsblätter

EDU: Repositories mit didaktischen Inhalten und Quelltexten für Vorlesungen und Tutorien

DOCS: Repositories für die Verwaltung und Speicherung von nicht-didaktischen (d.h. nicht EDU) Inhalten und Quelltexten

WEB: Repositories für das Hosting persönlicher Web-Seiten oder Blogs

DATA: Repositories für die Speicherung von Datensätzen

OTHER: Repositories, die sich nicht in die anderen Kategorien einordnen lassen"""

githubClient = github.Github(API_TOKEN)
filename = 'data/testset.csv'
MAX_REPO_ID = 76000000

if platform.system() == 'Darwin':
    command = 'open'
elif platform.system() == 'Linux':
    command = 'xdg-open'
else:
    # throw error
    pass


def read_visited_repos():
    try:
        with open(filename, 'r') as file:
            for line in file:
                print(line)
    except FileNotFoundError:
        return set()


def tag_repo(url):
    tags = set(["DEV", "HW", "EDU", "DOCS", "WEB", "DATA", "OTHER"])
    call([command, url])
    print(explanation)
    user_input = input("Classify:")
    if user_input.upper() in tags:
        return user_input.upper()
    else:
        return None


visited_repos = read_visited_repos()

with open(filename, 'a') as file:
    while True:
        try:
            repo = githubClient.get_repo(random.randrange(MAX_REPO_ID))
        except github.GithubException:
            # try different id
            continue
        url = repo.html_url
        if url in visited_repos:
            continue
        tag = tag_repo(url)
        if tag is not None:
            file.write(repo.html_url + ',' + tag + '\n')
            visited_repos.add(id)
