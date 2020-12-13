import sys
import random
import argparse
import os
import subprocess
import shlex
import time

def create_run_file(path, programs, testcases, target_file):

    if os.path.exists(os.path.join(path, f"run_{target_file}.sh")):
        os.remove(os.path.join(path, f"run_{target_file}.sh"))

    f = open(os.path.join(path, f"run_{target_file}.sh"), "w+")

    f.write("#!/bin/sh\n")
    f.write("set -e\n")
    f.write(f"rm -f {testcases}/{target_file}_TEST.class {programs}/{target_file}.class TestRunner.class\n")

    f.write(f"javac {programs}/{target_file}.java\n")
    f.write(f"javac -cp './junit-4.10.jar:./' {testcases}/{target_file}_TEST.java\n")
    f.write(f"javac -cp './junit-4.10.jar:./' TestRunner.java\n")

    class_testcase_path = testcases.replace("/", ".")
    f.write(f"java -cp './junit-4.10.jar:./' TestRunner {class_testcase_path}.{target_file}_TEST")

    f.close()

    os.chmod(os.path.join(path, f"run_{target_file}.sh"), 0o777) # set all permissions

TARGET_FILES = [
        'BITCOUNT',
        'BREADTH_FIRST_SEARCH',
        'BUCKETSORT',
        'DEPTH_FIRST_SEARCH',
        'DETECT_CYCLE',
        'FIND_FIRST_IN_SORTED',
        'FIND_IN_SORTED',
        'FLATTEN',
        'GCD',
        'GET_FACTORS',
        'HANOI',
        'IS_VALID_PARENTHESIZATION',
        'KHEAPSORT',
        'KNAPSACK',
        'KTH',
        'LCS_LENGTH',
        'LEVENSHTEIN',
        'LIS',
        'LONGEST_COMMON_SUBSEQUENCE',
        'MAX_SUBLIST_SUM',
        'MERGESORT',
        'MINIMUM_SPANNING_TREE',
        'NEXT_PALINDROME',
        'NEXT_PERMUTATION',
        'PASCAL',
        'POSSIBLE_CHANGE',
        'POWERSET',
        'QUICKSORT',
        'REVERSE_LINKED_LIST',
        'RPN_EVAL',
        'SHORTEST_PATH_LENGTH',
        'SHORTEST_PATH_LENGTHS',
        'SHORTEST_PATHS',
        'SHUNTING_YARD',
        'SIEVE',
        'SQRT',
        'SUBSEQUENCES',
        'TO_BASE',
        'TOPOLOGICAL_ORDERING',
        'WRAP',
    ]

if __name__ == "__main__":

    for target in TARGET_FILES:
        create_run_file("./", "java_programs", "java_testcases/junit", target)
