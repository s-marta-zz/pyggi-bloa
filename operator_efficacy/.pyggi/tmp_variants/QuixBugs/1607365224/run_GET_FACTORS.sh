#!/bin/sh
set -e
rm -f java_testcases/junit/GET_FACTORS_TEST.class java_programs/GET_FACTORS.class TestRunner.class
javac java_programs/GET_FACTORS.java
javac -cp './junit-4.10.jar:./' java_testcases/junit/GET_FACTORS_TEST.java
javac -cp './junit-4.10.jar:./' TestRunner.java
java -cp './junit-4.10.jar:./' TestRunner java_testcases.junit.GET_FACTORS_TEST