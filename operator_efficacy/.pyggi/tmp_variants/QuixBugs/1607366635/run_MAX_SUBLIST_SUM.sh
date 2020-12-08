#!/bin/sh
set -e
rm -f java_testcases/junit/MAX_SUBLIST_SUM_TEST.class java_programs/MAX_SUBLIST_SUM.class TestRunner.class
javac java_programs/MAX_SUBLIST_SUM.java
javac -cp './junit-4.10.jar:./' java_testcases/junit/MAX_SUBLIST_SUM_TEST.java
javac -cp './junit-4.10.jar:./' TestRunner.java
java -cp './junit-4.10.jar:./' TestRunner java_testcases.junit.MAX_SUBLIST_SUM_TEST