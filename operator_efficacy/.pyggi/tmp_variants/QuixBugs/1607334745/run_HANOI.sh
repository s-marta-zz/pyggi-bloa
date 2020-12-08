#!/bin/sh
set -e
rm -f java_testcases/junit/HANOI_TEST.class java_programs/HANOI.class TestRunner.class
javac java_programs/HANOI.java
javac -cp './junit-4.10.jar:./' java_testcases/junit/HANOI_TEST.java
javac -cp './junit-4.10.jar:./' TestRunner.java
java -cp './junit-4.10.jar:./' TestRunner java_testcases.junit.HANOI_TEST