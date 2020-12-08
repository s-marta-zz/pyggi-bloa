#!/bin/sh
set -e
rm -f java_testcases/junit/GCD_TEST.class java_programs/GCD.class TestRunner.class
javac java_programs/GCD.java
javac -cp './junit-4.10.jar:./' java_testcases/junit/GCD_TEST.java
javac -cp './junit-4.10.jar:./' TestRunner.java
java -cp './junit-4.10.jar:./' TestRunner java_testcases.junit.GCD_TEST