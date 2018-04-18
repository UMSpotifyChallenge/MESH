#!/usr/bin/python

import os
import numpy as np
import pickle
import matplotlib.pyplot as plt

def R_Precision(remainders, candidates):
	count = 0
	for (nodeID, value) in candidates:
		if nodeID in remainders:
			count += 1

	return float(count) / float(len(remainders))

def nDCG(remainders, candidates):
	dcg = 0.0
	matches = 0
	for i in range(len(candidates)):
		node, value = candidates[i]
		dcg += value / np.log2(i)
		if node in remainders:
			matches += 1

	idcg = 1.0
	for i in range(matches):
		idcg += 1 / np.log2(i)

	return dcg / idcg


def extract_scores_from_log(hidden_file, rating_results):
	interest_nodes = []
	rwr_scores = []
	hidden_tracks = []
	with open(hidden_file, 'r') as f:
		for line in f:
			hidden_tracks.append(int(line))
	f.close()
	with open(rating_results, 'r') as f:
		for line in f:
			# Now need to get the scores of all nodes in the graph
			if "compute,Final state - ID:" in line:
				relevant_information = line.split("ID:", 1)[1].split()
				# Format is now ID, attr, value
				try:
					nodeID = int(relevant_information[0])
				except ValueError:
					nodeID = int(relevant_information[0][:-1])

				if "HyperVertexAttr" in relevant_information[2]:
					value = line.split("HyperVertexAttr", 1)[1]
					for c in '(),':
						value = value.replace(c, '')

					rwr_scores.append((nodeID, float(value)))


	f.close()

	# Have all page rank scores
	sorted_rwr_scores = sorted(rwr_scores, key=lambda x:x[1], reverse=True)
	top500_rwr_scores = sorted_rwr_scores[0:499]
	rprec = R_Precision(hidden_tracks, top500_rwr_scores)
	return rprec

if __name__ == "__main__":
	R_Precision_dict = {}
	evaluation_dirs = [os.getcwd() + '/testing_files_1000/', os.getcwd() + '/testing_files_10000/']
	pickle_files = [os.getcwd() + '/rp_1000.pickle', os.getcwd() + '/rp_10000.pickle']
	for i in range(len(evaluation_dirs)):
		count = 0
		total = 0.0
		count_zero = 0
		all_rp_scores = []
		all_ndcg_scores = []
		for filename in os.listdir(evaluation_dir):
			if filename.endswith('.log'):
				results_file = evaluation_dir + filename
				hidden_track_file = evaluation_dir + filename[:-8] + 'hidden'
				R_Precision_dict[filename] = extract_scores_from_log(hidden_track_file, results_file)
				print("File: {0} has R-Precision of: {1}".format(results_file, R_Precision_dict[filename]))
				total += R_Precision_dict[filename]
				count += 1
				if R_Precision_dict[filename] == 0.0:
					count_zero += 1

				all_rp_scores.append(R_Precision_dict[filename])

		print("Average R-Precision: {0}".format(float(total / count)))


		sorted_rp_scores = sorted(all_rp_scores, reverse=True)
		length1 = len(sorted_rp_scores)

		pickle.dump(sorted_rp_scores, open(pickle_files[i], 'wb'))



			


