#!/bin/sh
set -e
rm -f java_testcases/junit/DETECT_CYCLE_TEST.class java_programs/DETECT_CYCLE.class TestRunner.class
javac java_programs/DETECT_CYCLE.java
javac -cp './junit-4.10.jar:./' java_testcases/junit/DETECT_CYCLE_TEST.java
javac -cp './junit-4.10.jar:./' TestRunner.java
java -cp './junit-4.10.jar:./' TestRunner java_testcases.junit.DETECT_CYCLE_TEST