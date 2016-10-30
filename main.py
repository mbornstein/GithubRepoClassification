import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import sklearn.cluster

import metrics

print(metrics.metricFuncs)

kMeans = sklearn.cluster.KMeans(n_clusters=6)


def aggregateData():
	pass

def train():
	X = aggregateData()
	kMeans.fit(X)

def predict(X):
	return kMeans.predict(X)

