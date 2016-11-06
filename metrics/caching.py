import os
import json
from github import Github

API_TOKEN = '0b8801a77eaea265f203f0a4b13d3d22739a6451'
githubClient = Github(API_TOKEN)

class CachedMetric(object):

	def __init__(self, f):
		# TODO: add function to list here
		self.function = f

	def __call__(self, *args, **kwargs):
		result = cacheLookup(self.function.__name__, args[0])
		if result == None:
			result = self.function(*args, **kwargs)
			writeToCache(self.function.__name__, result, args[0])
		return result

def getFilename(repoURL):
	filename = getFullName(repoURL).replace('/', '#') + '.json'
	return '../data/repoMetrics/' + filename

def cacheLookup(metricName, repoURL):
	try:
		with open(getFilename(repoURL), 'r') as data_file:
			data = json.load(data_file)
			return data[metricName]
	except (KeyError, FileNotFoundError):
		return None

def writeToCache(metricName, result, repoURL):
	filename = getFilename(repoURL)
	data = {}
	try:
		with open(filename, 'r') as data_file:
			data = json.load(data_file)
	except FileNotFoundError:
		# use empty directory
		pass
	data[metricName] = result
	with open(filename, 'w') as data_file:
			json.dump(data, data_file)

def getFullName(repoURL):
	tokens = repoURL.split('/')
	return tokens[-2] + '/' + tokens[-1]