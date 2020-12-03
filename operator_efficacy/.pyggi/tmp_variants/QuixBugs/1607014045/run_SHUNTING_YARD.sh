#!/bin/sh
set -e
rm -f java_testcases/junit/SHUNTING_YARD_TEST.class java_programs/SHUNTING_YARD.class TestRunner.class
javac java_programs/SHUNTING_YARD.java
javac -cp './junit-4.10.jar:./' java_testcases/junit/SHUNTING_YARD_TEST.java
javac -cp './junit-4.10.jar:./' TestRunner.java
java -cp './junit-4.10.jar:./' TestRunner java_testcases.junit.SHUNTING_YARD_TEST