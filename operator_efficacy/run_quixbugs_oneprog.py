import sys
import random
import argparse
import os
import subprocess
import shlex
import time
import copy

from pyggi.base import Patch, AbstractProgram
from pyggi.tree import TreeProgram, SrcmlEngine
from pyggi.tree import StmtReplacement, StmtInsertion, StmtDeletion
from pyggi.tree import ComparisonOperatorSetting
from pyggi.algo import FirstImprovement

# =============================================================================
# Target software specifics
# =============================================================================

class MySrcmlEngine(SrcmlEngine):
    TAG_RENAME = {
        'stmt': {'break', 'continue', 'decl_stmt', 'do', 'expr_stmt', 'for', 'goto', 'if', 'return', 'switch', 'while'},
        'operator_comp': {'operator_comp'},
    }
    TAG_FOCUS = { t for tl in TAG_RENAME.values() for t in tl }

class MyProgram(TreeProgram):
    def setup(self):
        self.possible_edits = [StmtReplacement, StmtInsertion, StmtDeletion, ComparisonOperatorSetting]

    def load_config(self, path, config):
        self.target_files = ["java_programs/LIS.java.xml"]
        self.test_command = "./run_LIS.sh"

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
            return target_tag == 'stmt'
        elif any(isinstance(edit, c) for c in [StmtReplacement, StmtInsertion, StmtDeletion]):
            target_file, target_point = edit.target
            ingredient_file, ingredient_point = edit.ingredient
            target_tag = self.contents[target_file].find(self.modification_points[target_file][target_point]).tag
            ingredient_tag = self.contents[ingredient_file].find(self.modification_points[ingredient_file][ingredient_point]).tag
            return target_tag == ingredient_tag == 'stmt'
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
        if self.program is None:
            raise AssertionError('Program not specified')
        if self.search is None:
            raise AssertionError('Search not specified')

        self.search.config['warmup'] = 3
        self.search.program = self.program

        logger = self.program.logger
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

# =============================================================================
# Main function
# =============================================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Running one program from QuixBugs')
    parser.add_argument('--epoch', type=int, default=20)
    parser.add_argument('--iter', type=int, default=1000)
    args = parser.parse_args()

    protocol = ExpProtocol()
    protocol.nb_epoch = args.epoch
    protocol.search = FirstImprovement()
    protocol.search.stop['fitness'] = 0
    protocol.search.stop['steps'] = args.iter
    protocol.program = MyProgram('./QuixBugs')

    # run experiment
    time_start = time.time()
    protocol.run()
    time_end = time.time()

    print(f"experiment duration: {time_end - time_start}")
