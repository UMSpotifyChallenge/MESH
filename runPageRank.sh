#!/bin/bash

export SPARK_MAJOR_VERSION=2
export PATH=$PATH:/home/siddvenk/apache-maven-3.3.9

spark-submit --class umn.dcsg.examples.PageRankRunner \
--master yarn \
--num-executors 20 \
--executor-memory 6g \
--executor-cores 4 \
/home/siddvenk/UMSpotifyChallenge/MESH/examples/target/examples-1.0-SNAPSHOT-jar-with-dependencies.jar \
"/user/siddvenk/MESH/track_hypergraph_all_features.csv" 0 50 &> output.txt