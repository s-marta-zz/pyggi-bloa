#!/bin/sh
set -e
rm -f java_testcases/junit/SHORTEST_PATH_LENGTHS_TEST.class java_programs/SHORTEST_PATH_LENGTHS.class TestRunner.class
javac java_programs/SHORTEST_PATH_LENGTHS.java
javac -cp './junit-4.10.jar:./' java_testcases/junit/SHORTEST_PATH_LENGTHS_TEST.java
javac -cp './junit-4.10.jar:./' TestRunner.java
java -cp './junit-4.10.jar:./' TestRunner java_testcases.junit.SHORTEST_PATH_LENGTHS_TEST