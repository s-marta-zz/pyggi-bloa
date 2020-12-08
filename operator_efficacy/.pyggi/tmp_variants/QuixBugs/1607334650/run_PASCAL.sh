#!/bin/sh
set -e
rm -f java_testcases/junit/PASCAL_TEST.class java_programs/PASCAL.class TestRunner.class
javac java_programs/PASCAL.java
javac -cp './junit-4.10.jar:./' java_testcases/junit/PASCAL_TEST.java
javac -cp './junit-4.10.jar:./' TestRunner.java
java -cp './junit-4.10.jar:./' TestRunner java_testcases.junit.PASCAL_TEST