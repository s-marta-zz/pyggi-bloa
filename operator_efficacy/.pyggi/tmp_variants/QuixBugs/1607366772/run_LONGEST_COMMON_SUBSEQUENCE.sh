#!/bin/sh
set -e
rm -f java_testcases/junit/LONGEST_COMMON_SUBSEQUENCE_TEST.class java_programs/LONGEST_COMMON_SUBSEQUENCE.class TestRunner.class
javac java_programs/LONGEST_COMMON_SUBSEQUENCE.java
javac -cp './junit-4.10.jar:./' java_testcases/junit/LONGEST_COMMON_SUBSEQUENCE_TEST.java
javac -cp './junit-4.10.jar:./' TestRunner.java
java -cp './junit-4.10.jar:./' TestRunner java_testcases.junit.LONGEST_COMMON_SUBSEQUENCE_TEST