#!/bin/sh
set -e
rm -f java_testcases/junit/QUICKSORT_TEST.class java_programs/QUICKSORT.class TestRunner.class
javac java_programs/QUICKSORT.java
javac -cp './junit-4.10.jar:./' java_testcases/junit/QUICKSORT_TEST.java
javac -cp './junit-4.10.jar:./' TestRunner.java
java -cp './junit-4.10.jar:./' TestRunner java_testcases.junit.QUICKSORT_TEST