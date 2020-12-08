#!/bin/sh
set -e
rm -f java_testcases/junit/BREADTH_FIRST_SEARCH_TEST.class java_programs/BREADTH_FIRST_SEARCH.class TestRunner.class
javac java_programs/BREADTH_FIRST_SEARCH.java
javac -cp './junit-4.10.jar:./' java_testcases/junit/BREADTH_FIRST_SEARCH_TEST.java
javac -cp './junit-4.10.jar:./' TestRunner.java
java -cp './junit-4.10.jar:./' TestRunner java_testcases.junit.BREADTH_FIRST_SEARCH_TEST