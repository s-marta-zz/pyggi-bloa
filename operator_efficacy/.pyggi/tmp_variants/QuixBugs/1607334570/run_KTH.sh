#!/bin/sh
set -e
rm -f java_testcases/junit/KTH_TEST.class java_programs/KTH.class TestRunner.class
javac java_programs/KTH.java
javac -cp './junit-4.10.jar:./' java_testcases/junit/KTH_TEST.java
javac -cp './junit-4.10.jar:./' TestRunner.java
java -cp './junit-4.10.jar:./' TestRunner java_testcases.junit.KTH_TEST