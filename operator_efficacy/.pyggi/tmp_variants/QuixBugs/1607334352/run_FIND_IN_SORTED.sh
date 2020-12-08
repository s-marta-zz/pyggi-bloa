#!/bin/sh
set -e
rm -f java_testcases/junit/FIND_IN_SORTED_TEST.class java_programs/FIND_IN_SORTED.class TestRunner.class
javac java_programs/FIND_IN_SORTED.java
javac -cp './junit-4.10.jar:./' java_testcases/junit/FIND_IN_SORTED_TEST.java
javac -cp './junit-4.10.jar:./' TestRunner.java
java -cp './junit-4.10.jar:./' TestRunner java_testcases.junit.FIND_IN_SORTED_TEST