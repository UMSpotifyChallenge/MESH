#!/usr/bin/python
import os
from sklearn.cluster import KMeans
import numpy as np
import pickle

def make_track_feature_matrix(filename, playlist_file, size, num_playlists):
	# Input File Scheme Presented Below
	# id,album_id,acousticness,danceability,duration_ms,energy,instrumentalness,key,liveness,loudness,mode,speechiness,tempo,time_signature,valence
	# Our matrix will be Ntracks x Nfeatures
	# For 1000 playlist set: 35661 x 10
	# For 10000 playlist set: 170272 x 10

	# Do clustering for k=4,16,64 classes
	node_translation_dict = {}
	node_count = 0
	track_feature_matrix = np.zeros([size, 12])
	album_translation_dict = {}
	hyper_edge_count = 0
	all_hyper_edges = []
	with open(filename, 'r') as f:
		for line in f:
			vals = line.split(',')
			try:
				track_id = int(vals[0])
			except ValueError:
				continue
			# Remove time_duration from the features
			album_id = int(vals[1])
			vals = np.delete(vals, [0,1,4])
			features = np.zeros(12)
			for i in range(12):
				try:
					features[i] = float(vals[i])
				except ValueError:
					features[i] = 0.0

			if track_id not in node_translation_dict:
				node_translation_dict[track_id] = node_count
				node_count += 1
			if album_id not in album_translation_dict:
				album_translation_dict[album_id] = hyper_edge_count
				hyper_edge_count += 1
			edge_pair = (album_translation_dict[album_id], node_translation_dict[track_id])
			all_hyper_edges.append(edge_pair)
			track_feature_matrix[node_translation_dict[track_id], :] = features.T

	node_translation_file = open(os.getcwd() + '/translation.pickle_' + str(num_playlists), 'wb')
	pickle.dump(node_translation_dict, node_translation_file)
	node_translation_file.close()


	f.close()
	print("Finished hyperedges for albums")

	for num_clusters in [4,16,64]:
		labels = KMeans(n_clusters=num_clusters).fit_predict(track_feature_matrix)
		current_hyper_edge_mapping = {}
		for i in range(track_feature_matrix.shape[0]):
			hypedge = int(labels[i])
			if hypedge not in current_hyper_edge_mapping:
				current_hyper_edge_mapping[hypedge] = hyper_edge_count
				hyper_edge_count += 1
			edge_pair = (current_hyper_edge_mapping[hypedge], i)
			all_hyper_edges.append(edge_pair)
		print("Finished hyperedges for clusters={0}".format(num_clusters))
	# Now need to do it for the training playlists
	with open(playlist_file, 'r') as f:
		current_hyper_edge_mapping = {}
		for line in f:
			vals = line.split()
			pid = int(vals[0])
			tracks = [int(i) for i in vals[1:]]
			for track in tracks:
				if pid not in current_hyper_edge_mapping:
					current_hyper_edge_mapping[pid] = hyper_edge_count
					hyper_edge_count += 1
				edge_pair = (current_hyper_edge_mapping[pid], node_translation_dict[track])
				all_hyper_edges.append(edge_pair)

	f.close()
	print("Finished hyperedges for training playlists")

	output_file = os.getcwd() + '/track_hypergraph_' + str(num_playlists) + '.csv'
	ou = open(output_file, 'w+')
	for ep in all_hyper_edges:
		ou.write("{0},{1}\n".format(ep[0], ep[1]))
	ou.close()
	print("Finished making hypergraph file")



if __name__ == "__main__":
	track_files = [os.getcwd() + '/tracks_1000(35661).csv', os.getcwd() + '/tracks_10000(170272).csv']
	playlist_file = [os.getcwd() + '/hon_training_1000.txt', os.getcwd() + '/hon_training_10000.txt']
	size = [35661, 170272]
	for i in range(len(track_files)):
		make_track_feature_matrix(track_file[i], playlist_file[i], size[i])

