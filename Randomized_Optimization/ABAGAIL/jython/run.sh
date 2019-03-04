#!/bin/bash
# edit the classpath to to the location of your ABAGAIL jar file
#
export CLASSPATH=../ABAGAIL.jar:$CLASSPATH
mkdir -p data/plot logs image

# continuous peaks
echo "continuous peaks"
jython continuouspeaks.py

# knapsack
echo "Running knapsack"
jython knapsack.py

# traveling salesman
echo "Running traveling salesman test"
jython travelingsalesman.py