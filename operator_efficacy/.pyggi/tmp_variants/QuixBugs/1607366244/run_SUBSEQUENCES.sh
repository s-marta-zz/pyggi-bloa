#!/bin/sh
set -e
rm -f java_testcases/junit/SUBSEQUENCES_TEST.class java_programs/SUBSEQUENCES.class TestRunner.class
javac java_programs/SUBSEQUENCES.java
javac -cp './junit-4.10.jar:./' java_testcases/junit/SUBSEQUENCES_TEST.java
javac -cp './junit-4.10.jar:./' TestRunner.java
java -cp './junit-4.10.jar:./' TestRunner java_testcases.junit.SUBSEQUENCES_TEST