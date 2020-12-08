#!/bin/sh
set -e
rm -f java_testcases/junit/LCS_LENGTH_TEST.class java_programs/LCS_LENGTH.class TestRunner.class
javac java_programs/LCS_LENGTH.java
javac -cp './junit-4.10.jar:./' java_testcases/junit/LCS_LENGTH_TEST.java
javac -cp './junit-4.10.jar:./' TestRunner.java
java -cp './junit-4.10.jar:./' TestRunner java_testcases.junit.LCS_LENGTH_TEST