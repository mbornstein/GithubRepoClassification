import importlib
from os.path import dirname, basename, isfile
import glob

metricCollection = {}

#import simpleMetrics

print("metrics", metricCollection)

def getPythonFiles():
	files = glob.glob(dirname(__file__)+"/*.py")
	return [f for f in files if isfile(f)]
	
#def importFiles(files):
#	for f in files:
#		print("import", f)
#		importlib.import_module("metrics." + basename(f[:-3]))

def getMetric():
	return 3
#	pythonFiles = getPythonFiles()
#	filteredPythonFiles = [f for f in pythonFiles if not 'metrics.py' in f]
#	filteredPythonFiles = [f for f in filteredPythonFiles if not 'caching.py' in f]
#	importFiles(filteredPythonFiles)