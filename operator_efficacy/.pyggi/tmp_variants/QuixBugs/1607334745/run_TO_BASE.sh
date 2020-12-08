#!/bin/sh
set -e
rm -f java_testcases/junit/TO_BASE_TEST.class java_programs/TO_BASE.class TestRunner.class
javac java_programs/TO_BASE.java
javac -cp './junit-4.10.jar:./' java_testcases/junit/TO_BASE_TEST.java
javac -cp './junit-4.10.jar:./' TestRunner.java
java -cp './junit-4.10.jar:./' TestRunner java_testcases.junit.TO_BASE_TEST