import importlib
from os.path import dirname, basename, isfile
import glob

metricCollection = {}

def getPythonFiles():
	files = glob.glob(dirname(__file__)+"/*.py")
	return [f for f in files if isfile(f)]
	
def importFiles(files):
	for f in files:
		importlib.import_module(basename(f)[:-3])
		# try:
		# 	print('imported', f)
		# except Exception as e:
		# 	print('error while importing', f, ':', e)

pythonFiles = getPythonFiles()
filteredPythonFiles = [f for f in pythonFiles if not 'metrics.py' in f]
filteredPythonFiles = [f for f in filteredPythonFiles if not 'caching.py' in f]

importFiles(filteredPythonFiles)