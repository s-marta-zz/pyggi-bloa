#!/bin/sh
set -e
rm -f java_testcases/junit/MINIMUM_SPANNING_TREE_TEST.class java_programs/MINIMUM_SPANNING_TREE.class TestRunner.class
javac java_programs/MINIMUM_SPANNING_TREE.java
javac -cp './junit-4.10.jar:./' java_testcases/junit/MINIMUM_SPANNING_TREE_TEST.java
javac -cp './junit-4.10.jar:./' TestRunner.java
java -cp './junit-4.10.jar:./' TestRunner java_testcases.junit.MINIMUM_SPANNING_TREE_TEST