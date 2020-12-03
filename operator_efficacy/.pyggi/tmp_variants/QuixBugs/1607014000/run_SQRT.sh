#!/bin/sh
set -e
rm -f java_testcases/junit/SQRT_TEST.class java_programs/SQRT.class TestRunner.class
javac java_programs/SQRT.java
javac -cp './junit-4.10.jar:./' java_testcases/junit/SQRT_TEST.java
javac -cp './junit-4.10.jar:./' TestRunner.java
java -cp './junit-4.10.jar:./' TestRunner java_testcases.junit.SQRT_TEST