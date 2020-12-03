#!/bin/sh
set -e
rm -f java_testcases/junit/WRAP_TEST.class java_programs/WRAP.class TestRunner.class
javac java_programs/WRAP.java
javac -cp './junit-4.10.jar:./' java_testcases/junit/WRAP_TEST.java
javac -cp './junit-4.10.jar:./' TestRunner.java
java -cp './junit-4.10.jar:./' TestRunner java_testcases.junit.WRAP_TEST