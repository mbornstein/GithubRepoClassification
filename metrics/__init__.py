import importlib
from os.path import dirname, basename, isfile
import glob

def getModules():
	files = glob.glob(dirname(__file__)+"/*.py")
	modules = [importlib.import_module(basename(f)[:-3]) for f in files if isfile(f) and not '__init__' in f]
	return modules

metricFunctions = []

for module in getModules():
	for name, val in module.__dict__.items():
		if callable(val):
			annotations = val.__annotations__
			if 'return' in annotations and annotations['return'] == 'metric':
				metricFunctions.append(val)


