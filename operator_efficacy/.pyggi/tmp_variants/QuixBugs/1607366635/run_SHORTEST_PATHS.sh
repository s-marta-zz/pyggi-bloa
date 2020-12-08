#!/bin/sh
set -e
rm -f java_testcases/junit/SHORTEST_PATHS_TEST.class java_programs/SHORTEST_PATHS.class TestRunner.class
javac java_programs/SHORTEST_PATHS.java
javac -cp './junit-4.10.jar:./' java_testcases/junit/SHORTEST_PATHS_TEST.java
javac -cp './junit-4.10.jar:./' TestRunner.java
java -cp './junit-4.10.jar:./' TestRunner java_testcases.junit.SHORTEST_PATHS_TEST