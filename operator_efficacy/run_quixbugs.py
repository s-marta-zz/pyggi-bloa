import sys
import random
import argparse
import os
import subprocess
import shlex
import time
import copy
import collections
import logging

from pyggi.base import Patch, AbstractProgram, RunResult
from pyggi.tree import TreeProgram, SrcmlEngine, AbstractTreeEngine
from pyggi.tree import StmtReplacement, StmtInsertion, StmtDeletion
from pyggi.tree import ComparisonOperatorSetting
from pyggi.algo import FirstImprovement
from pyggi.utils import Logger

TARGET_FILES = [
        ### 'BITCOUNT', # initilal solution failed
        'BREADTH_FIRST_SEARCH',
        ### 'BUCKETSORT', # no passing testcases
        'DEPTH_FIRST_SEARCH',
        'DETECT_CYCLE',
        ### 'FIND_FIRST_IN_SORTED', # initilal solution failed
        'FIND_IN_SORTED',
        'FLATTEN',
        ### 'GCD', # no passing testcases
        'GET_FACTORS',
        ### 'HANOI', # no passing testcases
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
        ### 'MINIMUM_SPANNING_TREE', # initilal solution failed
        'NEXT_PALINDROME',
        'NEXT_PERMUTATION',
        'PASCAL',
        ### 'POSSIBLE_CHANGE', # no passing testcases
        'POWERSET',
        'QUICKSORT',
        ### 'REVERSE_LINKED_LIST', # initilal solution failed
        ### 'RPN_EVAL', # initilal solution failed
        'SHORTEST_PATH_LENGTH',
        'SHORTEST_PATH_LENGTHS',
        ### 'SHORTEST_PATHS', # no passing testcases
        ### 'SHUNTING_YARD', # no passing testcases
        'SIEVE',
        ### 'SQRT', # initilal solution failed
        'SUBSEQUENCES',
        ### 'TO_BASE', # no passing testcases
        ### 'TOPOLOGICAL_ORDERING', # no passing testcases
        'WRAP',
    ]

STMT_TAGS = {
    'break', 'continue', 'decl_stmt', 'do', 'expr_stmt', 'for', 'goto', 'if', 'return', 'switch', 'while'
}

class MyLogger(Logger):
    def __init__(self, name):
        # initialize
        self._logger = logging.getLogger(name)
        self._logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(message)s')
        # log directory
        if not os.path.exists(Logger.LOG_DIR):
            pathlib.Path(Logger.LOG_DIR).mkdir(parents=True)
        # file handler
        self.log_file_path = os.path.join(Logger.LOG_DIR, "{}.log".format(name))
        file_handler = logging.FileHandler(self.log_file_path, delay=True)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.DEBUG)
        # add handlers to the logger
        self._logger.addHandler(file_handler)

# =============================================================================
# Target software specifics
# =============================================================================

# modifying StmtInsertion to consider only insertions before a statement
class MyStmtInsertion(StmtInsertion):
    @classmethod
    def create(cls, program, target_file=None, ingr_file=None, direction=None, method='random'):
        if target_file is None:
            target_file = program.random_file(AbstractTreeEngine)
        if ingr_file is None:
            ingr_file = program.random_file(engine=program.engines[target_file])
        assert program.engines[target_file] == program.engines[ingr_file]
        if direction is None:
            direction = 'before'
        return cls(program.random_target(target_file, method),
                   program.random_target(ingr_file, 'random'),
                   direction)

class MyFirstImprovement(FirstImprovement):
    def hook_evaluation(self, patch, run, accept, best):
        # gathering data to study how different operators applied on different
        # types of nodes influence the fitness of the program

        super().hook_evaluation(patch, run, accept, best)

        # initialising previous fitness and previous patch length
        if self.stats['steps'] == 0:
            self.previous_fitness = self.report['initial_fitness']
            self.previous_patch_len = 0

        # list of all possible modification points for current program:
        mod_points_list = next(iter(self.program.modification_points.values()))
        current_patch_len = len(patch.edit_list) # number of edits in current patch

        last_added_edit = operator = target = ingredient = None
        operator = "EditDeletion-EmptyPatch"

        if current_patch_len > 0:
            last_added_edit = patch.edit_list[-1]

            if current_patch_len < self.previous_patch_len:
                operator = "EditDeletion"
            elif isinstance(last_added_edit, StmtReplacement):
                operator = "StmtReplacement"
                target = mod_points_list[int(last_added_edit.target[1])]
                ingredient = mod_points_list[int(last_added_edit.ingredient[1])]
            elif isinstance(last_added_edit, MyStmtInsertion):
                operator = "StmtInsertion"
                target = mod_points_list[int(last_added_edit.target[1])]
                ingredient = mod_points_list[int(last_added_edit.ingredient[1])]
            elif isinstance(last_added_edit, StmtDeletion):
                operator = "StmtDeletion"
                target = mod_points_list[int(last_added_edit.target[1])]
            elif isinstance(last_added_edit, ComparisonOperatorSetting):
                operator = "ComparisonOperator"
                target = mod_points_list[int(last_added_edit.target[1])]
                ingredient = last_added_edit.value

        self.program.logger2.info("{};{};{};{};{};{};{};{};{};{};{}".format(
            self.stats['steps'] + 1, run.status, self.program.return_code, # current iteration number and run status
            run.fitness, self.previous_fitness, #  current and previous fitness
            current_patch_len, self.previous_patch_len, # number of edits in the current and previous patch
            operator, target, ingredient, # lastly added edit and its parameters
            self.program.failures_info)) # test cases failures info if applicable

        # if the patch will be accepted for further exploration
        # (meaning used as a starting point for obtaining next new patch)
        # remember its fitness and number of edits
        if accept:
            self.previous_fitness = run.fitness
            self.previous_patch_len = current_patch_len

class MySrcmlEngine(SrcmlEngine):
    TAG_RENAME = dict()
    TAG_FOCUS = {'operator_comp', 'break', 'continue', 'decl_stmt', 'do', 'expr_stmt', 'for', 'goto', 'if', 'return', 'switch', 'while'}

class MyProgram(TreeProgram):
    def __init__(self, path, config=None):
        super().__init__(path, config)
        self.logger2 = MyLogger(self.name + '_' + self.timestamp + '_2')
        self.logger3 = MyLogger(self.name + '_' + self.timestamp + '_3')

    def setup(self):
        self.possible_edits = [StmtReplacement, MyStmtInsertion, StmtDeletion, ComparisonOperatorSetting]

    def load_config(self, path, config):
        # self.target_files = ["java_programs/LIS.java.xml"]
        # self.test_command = "./run_LIS.sh"
        self.target_files = config["target_files"]
        self.test_command = config["test_command"]

    def create_edit(self, patch=None):
        if len(self.possible_edits) == 0:
            raise AssertionError('Impossible to create new edits')
        operator = random.choice(self.possible_edits)
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

    # overwriting evaluate_patch method to extract testcases failure info
    def evaluate_patch(self, patch, timeout=15):
        # apply + run
        self.apply(patch)
        cwd = os.getcwd()
        try:
            os.chdir(self.tmp_path)
            return_code, stdout, stderr, elapsed_time = self.exec_cmd(shlex.split(self.test_command), timeout)
            _, fitness = self.decode_stdout(stdout, return_code) # extract fitness from the stdout
            # self.logger3.info("EVALUATE RESULTS: {} {} {}".format(return_code, stdout, stderr)) # debug
        finally:
            os.chdir(cwd)
        if return_code is None: # timeout
            return RunResult('TIMEOUT')
        else:
            result = RunResult('SUCCESS', None)
            self.compute_fitness(result, return_code, fitness, stderr.decode("ascii"), elapsed_time)
            assert not (result.status == 'SUCCESS' and result.fitness is None)
            return result

    def decode_stdout(self, stdout, return_code):
        stdout_decoded = stdout.decode("ascii")
        stdout_decoded = stdout_decoded.split('\n')
        stdout_decoded = [el for el in stdout_decoded if el]

        self.return_code = return_code
        self.failures_info = None

        fitness = None
        # if the execution was succesfull
        if return_code == 0:
            fitness = stdout_decoded[0] # extract the fitness from the first line
            del stdout_decoded[0] # delete the fitness from the list
            stdout_decoded = set(stdout_decoded) # transform results per test to a set
            self.failures_info = stdout_decoded

        return stdout_decoded, fitness

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

        iter_per_epoch = dict()
        result = []
        try:
            for epoch in range(self.nb_epoch):
                logger.info('========== EPOCH {} =========='.format(epoch+1))
                self.search.reset()
                self.search.run()
                r = copy.deepcopy(self.search.report)
                r['diff'] = self.program.diff(r['best_patch'])
                result.append(r)
                iter_per_epoch[epoch] = self.search.stats['steps']
                logger.info('')
        except KeyboardInterrupt:
            pass

        logger.info('========== REPORT ==========')
        for epoch in range(len(result)):
            logger.info('==== Epoch {} ===='.format(epoch+1))
            logger.info('Termination: {}'.format(result[epoch]['stop']))
            logger.info('Number of interations: {}'.format(iter_per_epoch[epoch]))
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
    parser = argparse.ArgumentParser(description='Running programs from QuixBugs')
    parser.add_argument('--epoch', type=int, default=20)
    parser.add_argument('--iter', type=int, default=500)
    args = parser.parse_args()

    experiment_durations = dict()

    for target in TARGET_FILES:
        protocol = ExpProtocol()
        protocol.nb_epoch = args.epoch
        protocol.search = FirstImprovement()
        protocol.search.stop['fitness'] = 0
        protocol.search.stop['steps'] = args.iter

        config = {
            "target_files": [f"java_programs/{target}.java.xml"],
            "test_command": f"./run_{target}.sh"
        }
        protocol.program = MyProgram('./QuixBugs', config)

        # run experiment
        protocol.run()
