#!/bin/sh
set -e
rm -f java_testcases/junit/POWERSET_TEST.class java_programs/POWERSET.class TestRunner.class
javac java_programs/POWERSET.java
javac -cp './junit-4.10.jar:./' java_testcases/junit/POWERSET_TEST.java
javac -cp './junit-4.10.jar:./' TestRunner.java
java -cp './junit-4.10.jar:./' TestRunner java_testcases.junit.POWERSET_TEST