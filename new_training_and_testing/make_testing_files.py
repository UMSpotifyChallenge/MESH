#!/usr/bin/python

import os
import json
import pickle

input_file = os.getcwd() + '/hon_testing_10000.json'

with open(input_file, 'r') as json_data:
	data = json.load(json_data)

json_data.close()

node_translation_dict = pickle.load(open(os.getcwd() + '/translation.pickle', 'rb'))


output_directory = os.getcwd() + '/testing_files_10000/'

count = 0
for d in data:
	seed_file = open(output_directory + str(count) + '.seed', 'w+')
	hidden_file = open(output_directory + str(count) + '.hidden', 'w+')
	seed_tracks = d["seed"]
	seed_tracks_new = [node_translation_dict[i] for i in seed_tracks]
	hidden_tracks = d["hidden"]
	hidden_tracks_new = [node_translation_dict[i] for i in hidden_tracks]
	for track in seed_tracks_new:
		seed_file.write("{0}\n".format(track))
	seed_file.close()
	for track in hidden_tracks_new:
		hidden_file.write("{0}\n".format(track))
	hidden_file.close()
	count += 1