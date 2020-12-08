#!/bin/sh
set -e
rm -f java_testcases/junit/MERGESORT_TEST.class java_programs/MERGESORT.class TestRunner.class
javac java_programs/MERGESORT.java
javac -cp './junit-4.10.jar:./' java_testcases/junit/MERGESORT_TEST.java
javac -cp './junit-4.10.jar:./' TestRunner.java
java -cp './junit-4.10.jar:./' TestRunner java_testcases.junit.MERGESORT_TEST