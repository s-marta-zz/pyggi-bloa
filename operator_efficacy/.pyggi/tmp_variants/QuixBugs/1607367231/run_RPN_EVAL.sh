#!/bin/sh
set -e
rm -f java_testcases/junit/RPN_EVAL_TEST.class java_programs/RPN_EVAL.class TestRunner.class
javac java_programs/RPN_EVAL.java
javac -cp './junit-4.10.jar:./' java_testcases/junit/RPN_EVAL_TEST.java
javac -cp './junit-4.10.jar:./' TestRunner.java
java -cp './junit-4.10.jar:./' TestRunner java_testcases.junit.RPN_EVAL_TEST