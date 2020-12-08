#!/bin/sh
set -e
rm -f java_testcases/junit/NEXT_PALINDROME_TEST.class java_programs/NEXT_PALINDROME.class TestRunner.class
javac java_programs/NEXT_PALINDROME.java
javac -cp './junit-4.10.jar:./' java_testcases/junit/NEXT_PALINDROME_TEST.java
javac -cp './junit-4.10.jar:./' TestRunner.java
java -cp './junit-4.10.jar:./' TestRunner java_testcases.junit.NEXT_PALINDROME_TEST