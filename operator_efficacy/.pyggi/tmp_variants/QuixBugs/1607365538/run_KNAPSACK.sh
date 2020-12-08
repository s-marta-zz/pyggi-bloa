#!/bin/sh
set -e
rm -f java_testcases/junit/KNAPSACK_TEST.class java_programs/KNAPSACK.class TestRunner.class
javac java_programs/KNAPSACK.java
javac -cp './junit-4.10.jar:./' java_testcases/junit/KNAPSACK_TEST.java
javac -cp './junit-4.10.jar:./' TestRunner.java
java -cp './junit-4.10.jar:./' TestRunner java_testcases.junit.KNAPSACK_TEST