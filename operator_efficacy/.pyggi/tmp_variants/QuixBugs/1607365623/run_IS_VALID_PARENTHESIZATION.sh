#!/bin/sh
set -e
rm -f java_testcases/junit/IS_VALID_PARENTHESIZATION_TEST.class java_programs/IS_VALID_PARENTHESIZATION.class TestRunner.class
javac java_programs/IS_VALID_PARENTHESIZATION.java
javac -cp './junit-4.10.jar:./' java_testcases/junit/IS_VALID_PARENTHESIZATION_TEST.java
javac -cp './junit-4.10.jar:./' TestRunner.java
java -cp './junit-4.10.jar:./' TestRunner java_testcases.junit.IS_VALID_PARENTHESIZATION_TEST