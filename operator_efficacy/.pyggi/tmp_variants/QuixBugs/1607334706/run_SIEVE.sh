#!/bin/sh
set -e
rm -f java_testcases/junit/SIEVE_TEST.class java_programs/SIEVE.class TestRunner.class
javac java_programs/SIEVE.java
javac -cp './junit-4.10.jar:./' java_testcases/junit/SIEVE_TEST.java
javac -cp './junit-4.10.jar:./' TestRunner.java
java -cp './junit-4.10.jar:./' TestRunner java_testcases.junit.SIEVE_TEST