#!/bin/sh
set -e
rm -f java_testcases/junit/NEXT_PERMUTATION_TEST.class java_programs/NEXT_PERMUTATION.class TestRunner.class
javac java_programs/NEXT_PERMUTATION.java
javac -cp './junit-4.10.jar:./' java_testcases/junit/NEXT_PERMUTATION_TEST.java
javac -cp './junit-4.10.jar:./' TestRunner.java
java -cp './junit-4.10.jar:./' TestRunner java_testcases.junit.NEXT_PERMUTATION_TEST