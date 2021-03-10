import sys
import random
import argparse
import os
import subprocess
import shlex
import time

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

def create_xml_file(path, target_file, timeout=15):

    file_path = f"{path}/{target_file}"

    if not os.path.exists(f'{file_path}.java.xml'):
        cmd = f"srcml {target_file}.java -o {target_file}.java.xml"

        cwd = os.getcwd()
        os.chdir(path)
        sprocess = subprocess.Popen(
            shlex.split(cmd),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        try:
            start = time.time()
            stdout, stderr = sprocess.communicate(timeout=timeout)
            end = time.time()
            return (sprocess.returncode, stdout.decode("ascii"), stderr.decode("ascii"), end-start)
        except subprocess.TimeoutExpired:
            sprocess.kill()
            return (None, None, None, None)
        finally:
            os.chdir(cwd)

if __name__ == "__main__":

    for target in TARGET_FILES:
        create_xml_file("./java_programs", target)
