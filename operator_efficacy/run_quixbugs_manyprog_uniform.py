import sys
import random
import argparse
import os
import subprocess
import shlex
import time
import copy
import collections

from pyggi.base import Patch, AbstractProgram
from pyggi.tree import TreeProgram, SrcmlEngine
from pyggi.tree import StmtReplacement, StmtInsertion, StmtDeletion
from pyggi.tree import ComparisonOperatorSetting
from pyggi.algo import FirstImprovement
from pyggi.utils import Logger

TARGET_FILES = [
        #'BITCOUNT',
        'BREADTH_FIRST_SEARCH',
        #'BUCKETSORT',
        #'DEPTH_FIRST_SEARCH',
        #'DETECT_CYCLE',
        #'FIND_FIRST_IN_SORTED',
        #'FIND_IN_SORTED',
        #'FLATTEN',
        #'GCD',
        #'GET_FACTORS',
        #'HANOI',
        #'IS_VALID_PARENTHESIZATION',
        #'KHEAPSORT',
        #'KNAPSACK',
        #'KTH',
        #'LCS_LENGTH',
        #'LEVENSHTEIN',
        #'LIS',
        #'LONGEST_COMMON_SUBSEQUENCE',
        #'MAX_SUBLIST_SUM',
        #'MERGESORT',
        #'MINIMUM_SPANNING_TREE',
        #'NEXT_PALINDROME',
        #'PASCAL',
        #'POSSIBLE_CHANGE',
        #'POWERSET',
        #'QUICKSORT',
        #'REVERSE_LINKED_LIST',
        #'RPN_EVAL',
        #'SHORTEST_PATH_LENGTH',
        #'SHORTEST_PATH_LENGTHS',
        #'SHORTEST_PATHS',
        #'SHUNTING_YARD',
        #'SIEVE',
        #'SQRT',
        #'SUBSEQUENCES',
        #'TO_BASE',
        #'TOPOLOGICAL_ORDERING',
        #'WRAP',
    ]
STMT_TAGS = {
    'break', 'continue', 'decl_stmt', 'do', 'expr_stmt', 'for', 'goto', 'if', 'return', 'switch', 'while'
}

# =============================================================================
# Target software specifics
# =============================================================================

class MyFirstImprovement(FirstImprovement):
    def hook_evaluation(self, patch, run, accept, best):
        super().hook_evaluation(patch, run, accept, best)

class MySrcmlEngine(SrcmlEngine):
    TAG_RENAME = dict()
    TAG_FOCUS = {'operator_comp', 'break', 'continue', 'decl_stmt', 'do', 'expr_stmt', 'for', 'goto', 'if', 'return', 'switch', 'while'}
    #TAG_FOCUS = {}

class MyProgram(TreeProgram):
    def __init__(self, path, config=None):
        super().__init__(path, config)
        self.logger2 = Logger(self.name + '_' + self.timestamp + '_2')

    def setup(self):
        self.possible_edits = [StmtReplacement, StmtInsertion, StmtDeletion, ComparisonOperatorSetting]

    def load_config(self, path, config):
        # self.target_files = ["java_programs/LIS.java.xml"]
        # self.test_command = "./run_LIS.sh"
        self.target_files = config["target_files"]
        self.test_command = config["test_command"]

    def chose_operator(self):
        # modification points for the program:
        mod_points_list = next(iter(self.modification_points.values()))
        # number of mod points that are comparison operators (m) or are statements (n):
        m = len([mp for mp in mod_points_list if "operator_comp" in mp])
        n = len(mod_points_list) - m

        # probabilities of operators getting selected for simulating uniform sampling
        sum = n + (n * n) + 2 * (n * n) + 5 * m
        prob_del = (n) / sum
        prob_rep = (n*n) / sum
        prob_ins = (2*n*n) / sum
        prob_comp = (5*m) / sum

        probs = (prob_rep, prob_ins, prob_del, prob_comp)
        return random.choices(self.possible_edits, weights=probs, k=1)[0]

    def create_edit(self, patch=None):
        if len(self.possible_edits) == 0:
            raise AssertionError('Impossible to create new edits')
        #operator = random.choice(self.possible_edits)
        operator = self.chose_operator()
        for _ in range(1000):
            edit = operator.create(self)
            if self.would_edit_be_valid(edit):
                return edit
        raise AssertionError('Failed to create a valid edit of type {}'.format(operator))

    def would_edit_be_valid(self, edit):
        if isinstance(edit, ComparisonOperatorSetting):
            target_file, target_point = edit.target
            target_tag = self.contents[target_file].find(self.modification_points[target_file][target_point]).tag
            return target_tag == 'operator_comp'
        elif isinstance(edit, StmtDeletion):
            target_file, target_point = edit.target
            target_tag = self.contents[target_file].find(self.modification_points[target_file][target_point]).tag
            #return target_tag == 'stmt'
            return target_tag in STMT_TAGS
        elif any(isinstance(edit, c) for c in [StmtReplacement, StmtInsertion, StmtDeletion]):
            target_file, target_point = edit.target
            ingredient_file, ingredient_point = edit.ingredient
            target_tag = self.contents[target_file].find(self.modification_points[target_file][target_point]).tag
            ingredient_tag = self.contents[ingredient_file].find(self.modification_points[ingredient_file][ingredient_point]).tag
            #return target_tag == ingredient_tag == 'stmt'
            return target_tag in STMT_TAGS and ingredient_tag in STMT_TAGS
        return True

    @classmethod
    def get_engine(cls, file_name):
        return MySrcmlEngine

# ================================================================================
# Experimental protocol
# ================================================================================

class ExpProtocol:
    def __init__(self):
        self.nb_epoch = 10
        self.search = None
        self.program = None

    def run(self):
        logger = self.program.logger

        logger.info('========== EXPERIMENT FOR {}  =========='.format(self.program.target_files))

        # modification points for the program:
        mod_points_list = next(iter(self.program.modification_points.values()))
        # number of mod points that are comparison operators or are statements:
        m = len([mp for mp in mod_points_list if "operator_comp" in mp])
        n = len(mod_points_list) - m
        logger.info("modification points:\n {}".format(mod_points_list))
        logger.info("number of statements and comparisons: {}, {}".format(n, m))

        time_start = time.time()

        if self.program is None:
            raise AssertionError('Program not specified')
        if self.search is None:
            raise AssertionError('Search not specified')

        self.search.config['warmup'] = 3
        self.search.program = self.program

        result = []
        try:
            for epoch in range(self.nb_epoch):
                logger.info('========== EPOCH {} =========='.format(epoch+1))
                self.search.reset()
                self.search.run()
                r = copy.deepcopy(self.search.report)
                r['diff'] = self.program.diff(r['best_patch'])
                result.append(r)
                logger.info('')
        except KeyboardInterrupt:
            pass

        logger.info('========== REPORT ==========')
        for epoch in range(len(result)):
            logger.info('==== Epoch {} ===='.format(epoch+1))
            logger.info('Termination: {}'.format(result[epoch]['stop']))
            if result[epoch]['best_patch']:
                logger.info('Best fitness: {}'.format(result[epoch]['best_fitness']))
                logger.info('Best patch: {}'.format(result[epoch]['best_patch']))
                logger.info('Diff:\n{}'.format(result[epoch]['diff']))
        self.program.remove_tmp_variant()

        time_end = time.time()
        logger.info('Experiment duration: {}'.format(time_end - time_start))

# =============================================================================
# Main function
# =============================================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Running one program from QuixBugs')
    parser.add_argument('--epoch', type=int, default=20)
    parser.add_argument('--iter', type=int, default=1000)
    args = parser.parse_args()

    for target in TARGET_FILES:

        protocol = ExpProtocol()
        protocol.nb_epoch = args.epoch
        protocol.search = MyFirstImprovement()
        protocol.search.stop['fitness'] = 0
        protocol.search.stop['steps'] = args.iter

        config = {
            "target_files": [f"java_programs/{target}.java.xml"],
            "test_command": f"./run_{target}.sh"
        }
        protocol.program = MyProgram('./QuixBugs', config)

        # theengine = next(iter(protocol.program.engines.values()))
        # thetree = next(iter(protocol.program.contents.values()))
        # print(theengine.tree_to_string(thetree))

        # run experiment
        protocol.run()
