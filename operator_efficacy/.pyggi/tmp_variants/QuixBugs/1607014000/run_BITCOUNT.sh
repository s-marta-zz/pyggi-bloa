#!/bin/sh
set -e
rm -f java_testcases/junit/BITCOUNT_TEST.class java_programs/BITCOUNT.class TestRunner.class
javac java_programs/BITCOUNT.java
javac -cp './junit-4.10.jar:./' java_testcases/junit/BITCOUNT_TEST.java
javac -cp './junit-4.10.jar:./' TestRunner.java
java -cp './junit-4.10.jar:./' TestRunner java_testcases.junit.BITCOUNT_TEST