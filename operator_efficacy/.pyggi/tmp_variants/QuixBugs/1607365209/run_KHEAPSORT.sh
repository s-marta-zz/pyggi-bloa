#!/bin/sh
set -e
rm -f java_testcases/junit/KHEAPSORT_TEST.class java_programs/KHEAPSORT.class TestRunner.class
javac java_programs/KHEAPSORT.java
javac -cp './junit-4.10.jar:./' java_testcases/junit/KHEAPSORT_TEST.java
javac -cp './junit-4.10.jar:./' TestRunner.java
java -cp './junit-4.10.jar:./' TestRunner java_testcases.junit.KHEAPSORT_TEST