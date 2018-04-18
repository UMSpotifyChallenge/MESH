#!/usr/bin/python

import os
import pickle
import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":
	cwd = os.getcwd()
	rp_scores_1000 = pickle.load(open(cwd + '/rp_1000.pickle', 'rb'))
	rp_scores_10000 = pickle.load(open(cwd + '/rp_10000.pickle', 'rb'))

	length1 = [i for i in range(len(rp_scores_1000))]
	length2 = [i for i in range(len(rp_scores_10000))]
	mean1 = np.mean(rp_scores_1000)
	print(mean1)
	mean2 = np.mean(rp_scores_10000)
	print(mean2)

	plt.figure(1)
	plt.plot(length1, rp_scores_1000, color='k', markersize=2)
	plt.plot(length1, [mean1 for i in length1], color='r')
	plt.title("R-Precision | Hypergraph | 1k Rand")
	plt.ylabel("R-Precision Score")
	plt.figure(2)
	plt.plot(length2, rp_scores_10000, color='k', markersize=2)
	plt.plot(length2, [mean2 for i in length2], color='r')
	plt.title("R-Precision | Hypergraph | 10k Rand")
	plt.ylabel("R-Precision Score")
	plt.show()