#!/bin/sh
set -e
rm -f java_testcases/junit/POSSIBLE_CHANGE_TEST.class java_programs/POSSIBLE_CHANGE.class TestRunner.class
javac java_programs/POSSIBLE_CHANGE.java
javac -cp './junit-4.10.jar:./' java_testcases/junit/POSSIBLE_CHANGE_TEST.java
javac -cp './junit-4.10.jar:./' TestRunner.java
java -cp './junit-4.10.jar:./' TestRunner java_testcases.junit.POSSIBLE_CHANGE_TEST