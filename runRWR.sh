#!/bin/bash
echo "This script is used for running the HyperGraph models"
echo "Please edit this file to switch between the 1k and 10k playlist sets"


export SPARK_MAJOR_VERSION=2

python3 get_hyperedge_data.py
echo "Finished making hypergraphs for both data sets."
echo "Please upload hypergraph files to HDFS"

# TODO: Edit this if you want to change data sources
test_dir=${PWD}/new_training_and_testing/testing_files_1000/
graph_file="user/siddvenk/spotify_hypergraph/track_hypergraph_1000.csv"

#test_dir=${PWD}/new_training_and_testing/testing_files_10000/
#graph_file="/user/siddvenk/spotify_hypergraph/track_hypergraph_10000.csv"

for filename in $test_dir*.seed; do
	echo "Starting RWR for playlist $filename"
	spark-submit --class umn.dcsg.examples.RandomWalkRunner \
	--master yarn \
	--num-executors 20 \
	--executor-memory 6g \
	--executor-cores 4 \
	/home/siddvenk/UMSpotifyChallenge/MESH/examples/target/examples-1.0-SNAPSHOT-jar-with-dependencies.jar \
	$graph_file $filename 0 "2D" 4 100 100 &> output.txt
	cat output.txt | grep "LOGGER" > $filename.log
	rm output.txt
	echo "Finished RWR for playlist $filename. Output located at $filename .log" 
done

echo "Finished RWR for all test files"
echo "Evaluating results"
python3 evaluate.py
echo "Plotting results"
python3 plot_results.py