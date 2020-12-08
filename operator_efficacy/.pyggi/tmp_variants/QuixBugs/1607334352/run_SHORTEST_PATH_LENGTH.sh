#!/bin/sh
set -e
rm -f java_testcases/junit/SHORTEST_PATH_LENGTH_TEST.class java_programs/SHORTEST_PATH_LENGTH.class TestRunner.class
javac java_programs/SHORTEST_PATH_LENGTH.java
javac -cp './junit-4.10.jar:./' java_testcases/junit/SHORTEST_PATH_LENGTH_TEST.java
javac -cp './junit-4.10.jar:./' TestRunner.java
java -cp './junit-4.10.jar:./' TestRunner java_testcases.junit.SHORTEST_PATH_LENGTH_TEST