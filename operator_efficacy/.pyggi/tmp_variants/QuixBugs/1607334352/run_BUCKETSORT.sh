#!/bin/sh
set -e
rm -f java_testcases/junit/BUCKETSORT_TEST.class java_programs/BUCKETSORT.class TestRunner.class
javac java_programs/BUCKETSORT.java
javac -cp './junit-4.10.jar:./' java_testcases/junit/BUCKETSORT_TEST.java
javac -cp './junit-4.10.jar:./' TestRunner.java
java -cp './junit-4.10.jar:./' TestRunner java_testcases.junit.BUCKETSORT_TEST