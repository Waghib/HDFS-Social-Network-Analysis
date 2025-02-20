#!/bin/bash

# Set Hadoop variables
HADOOP_STREAMING_JAR="/home/waghib/hadoop-3.4.1/share/hadoop/tools/lib/hadoop-streaming-3.4.1.jar"
INPUT_FILE="soc-pokec-profiles.txt"
HDFS_INPUT_DIR="/user/pokec/input"
HDFS_OUTPUT_DIR="/user/pokec/output"
PYTHON_PATH=$(which python3)

# Enable debug mode
set -x

# Make scripts executable
chmod +x hadoop/demographic_mapper.py hadoop/demographic_reducer.py
chmod +x hadoop/correlation_mapper.py hadoop/correlation_reducer.py

# Create HDFS directories
echo "Creating HDFS directories..."
hadoop fs -mkdir -p $HDFS_INPUT_DIR

# Copy input file to HDFS if not exists
echo "Copying input file to HDFS..."
hadoop fs -test -e $HDFS_INPUT_DIR/$INPUT_FILE || hadoop fs -put data/$INPUT_FILE $HDFS_INPUT_DIR

# Remove existing output directories
echo "Removing existing output directories..."
hadoop fs -rm -r $HDFS_OUTPUT_DIR/demographics
hadoop fs -rm -r $HDFS_OUTPUT_DIR/correlations

# Run demographic analysis
echo "Running demographic analysis..."
hadoop jar $HADOOP_STREAMING_JAR \
    -D mapred.job.name="Demographic Analysis" \
    -D mapred.reduce.tasks=1 \
    -D mapred.child.java.opts="-Dpython.path=$PYTHON_PATH" \
    -input $HDFS_INPUT_DIR/$INPUT_FILE \
    -output $HDFS_OUTPUT_DIR/demographics \
    -mapper "$PYTHON_PATH hadoop/demographic_mapper.py" \
    -reducer "$PYTHON_PATH hadoop/demographic_reducer.py" \
    -file hadoop/demographic_mapper.py \
    -file hadoop/demographic_reducer.py

# Run correlation analysis with debug flags
echo "Running correlation analysis..."
hadoop jar $HADOOP_STREAMING_JAR \
    -D mapred.job.name="Correlation Analysis" \
    -D mapred.reduce.tasks=1 \
    -D mapred.map.tasks=14 \
    -D mapred.task.timeout=6000000 \
    -D mapred.map.output.compress=false \
    -D mapred.compress.map.output=false \
    -D mapred.child.java.opts="-Dpython.path=$PYTHON_PATH" \
    -input $HDFS_INPUT_DIR/$INPUT_FILE \
    -output $HDFS_OUTPUT_DIR/correlations \
    -mapper "$PYTHON_PATH hadoop/correlation_mapper.py" \
    -reducer "$PYTHON_PATH hadoop/correlation_reducer.py" \
    -file hadoop/correlation_mapper.py \
    -file hadoop/correlation_reducer.py

# Create results directory
mkdir -p results

# Save and display results
echo "Analysis complete. Results are in HDFS at $HDFS_OUTPUT_DIR"

# Handle demographic results
echo "Demographic analysis results:"
DEMO_OUTPUT=$(hadoop fs -cat $HDFS_OUTPUT_DIR/demographics/part-* 2>/dev/null)
if [ -z "$DEMO_OUTPUT" ]; then
    echo "Warning: Demographic analysis produced no output. Checking logs..."
    APP_ID=$(yarn application -list | grep "Demographic Analysis" | awk '{print $1}')
    if [ ! -z "$APP_ID" ]; then
        yarn logs -applicationId $APP_ID
    fi
else
    echo "$DEMO_OUTPUT" | tee results/demographic_analysis.json
fi

# Handle correlation results with error checking
echo -e "\nCorrelation analysis results:"
CORR_OUTPUT=$(hadoop fs -cat $HDFS_OUTPUT_DIR/correlations/part-* 2>/dev/null)
if [ -z "$CORR_OUTPUT" ]; then
    echo "Warning: Correlation analysis produced no output. Checking logs..."
    APP_ID=$(yarn application -list | grep "Correlation Analysis" | awk '{print $1}')
    if [ ! -z "$APP_ID" ]; then
        yarn logs -applicationId $APP_ID
    fi
else
    echo "$CORR_OUTPUT" | tee results/correlation_analysis.json
fi

# Disable debug mode
set +x
