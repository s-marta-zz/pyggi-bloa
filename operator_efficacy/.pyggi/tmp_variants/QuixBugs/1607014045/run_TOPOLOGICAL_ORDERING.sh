#!/bin/sh
set -e
rm -f java_testcases/junit/TOPOLOGICAL_ORDERING_TEST.class java_programs/TOPOLOGICAL_ORDERING.class TestRunner.class
javac java_programs/TOPOLOGICAL_ORDERING.java
javac -cp './junit-4.10.jar:./' java_testcases/junit/TOPOLOGICAL_ORDERING_TEST.java
javac -cp './junit-4.10.jar:./' TestRunner.java
java -cp './junit-4.10.jar:./' TestRunner java_testcases.junit.TOPOLOGICAL_ORDERING_TEST