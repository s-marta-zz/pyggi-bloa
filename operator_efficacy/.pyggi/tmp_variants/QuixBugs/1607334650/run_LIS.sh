#!/bin/sh
set -e
rm -f java_testcases/junit/LIS_TEST.class java_programs/LIS.class TestRunner.class
javac java_programs/LIS.java
javac -cp './junit-4.10.jar:./' java_testcases/junit/LIS_TEST.java
javac -cp './junit-4.10.jar:./' TestRunner.java
java -cp './junit-4.10.jar:./' TestRunner java_testcases.junit.LIS_TEST