#!/bin/bash

# Set Hadoop variables
HADOOP_STREAMING_JAR="/home/waghib/hadoop-3.4.1/share/hadoop/tools/lib/hadoop-streaming-3.4.1.jar"
INPUT_FILE="soc-pokec-profiles.txt"
HDFS_INPUT_DIR="/user/pokec/input"
HDFS_OUTPUT_DIR="/user/pokec/output"

# Make scripts executable
chmod +x hadoop/demographic_mapper.py hadoop/demographic_reducer.py
chmod +x hadoop/correlation_mapper.py hadoop/correlation_reducer.py

# Create HDFS directories
echo "Creating HDFS directories..."
hadoop fs -mkdir -p $HDFS_INPUT_DIR

# Copy input file to HDFS if not exists
echo "Copying input file to HDFS..."
hadoop fs -test -e $HDFS_INPUT_DIR/$INPUT_FILE || hadoop fs -put $INPUT_FILE $HDFS_INPUT_DIR

# Remove existing output directories
echo "Removing existing output directories..."
hadoop fs -rm -r $HDFS_OUTPUT_DIR/demographics
hadoop fs -rm -r $HDFS_OUTPUT_DIR/correlations

# Run demographic analysis
echo "Running demographic analysis..."
hadoop jar $HADOOP_STREAMING_JAR \
    -input $HDFS_INPUT_DIR/$INPUT_FILE \
    -output $HDFS_OUTPUT_DIR/demographics \
    -mapper hadoop/demographic_mapper.py \
    -reducer hadoop/demographic_reducer.py \
    -file hadoop/demographic_mapper.py \
    -file hadoop/demographic_reducer.py

# Run correlation analysis
echo "Running correlation analysis..."
hadoop jar $HADOOP_STREAMING_JAR \
    -input $HDFS_INPUT_DIR/$INPUT_FILE \
    -output $HDFS_OUTPUT_DIR/correlations \
    -mapper hadoop/correlation_mapper.py \
    -reducer hadoop/correlation_reducer.py \
    -file hadoop/correlation_mapper.py \
    -file hadoop/correlation_reducer.py

# Collect and display results
echo "Analysis complete. Results are in HDFS at $HDFS_OUTPUT_DIR"
echo "Demographic analysis results:"
hadoop fs -cat $HDFS_OUTPUT_DIR/demographics/part-*

echo -e "\nCorrelation analysis results:"
hadoop fs -cat $HDFS_OUTPUT_DIR/correlations/part-*
