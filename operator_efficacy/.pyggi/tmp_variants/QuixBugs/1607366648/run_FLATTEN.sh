#!/bin/sh
set -e
rm -f java_testcases/junit/FLATTEN_TEST.class java_programs/FLATTEN.class TestRunner.class
javac java_programs/FLATTEN.java
javac -cp './junit-4.10.jar:./' java_testcases/junit/FLATTEN_TEST.java
javac -cp './junit-4.10.jar:./' TestRunner.java
java -cp './junit-4.10.jar:./' TestRunner java_testcases.junit.FLATTEN_TEST