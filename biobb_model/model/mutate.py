#!/usr/bin/env python3

"""
Module containing the Mutate class and the command line interface.
"""

import argparse
import sys
import os
from biobb_common.configuration   import settings
from biobb_common.tools import file_utils as fu
import structure_checking.structure_checking as sc
from structure_checking.structure_checking import StructureChecking
from structure_checking.default_settings import DefaultSettings


class Mutate():
    """Class to mutate one aminoacid by another in a 3d structure.
    Args:
        input_pdb_path (str) - Input PDB file path.
        output_pdb_path (str) - Output PDB file path.
        properties (dic):
            | - **mutation** (*str*): Mutation list in the format "Chain.WT_AA_ThreeLeterCode.Resnum.MUT_AA_ThreeLeterCode" separated by commas. If no chain is provided as chain code all the chains in the pdb file will be mutated. ie: "A.ALA15CYS"
    """
    def __init__(self, input_pdb_path, output_pdb_path, properties, **kwargs):
        # Input/Output files
        self.input_pdb_path = input_pdb_path
        self.output_pdb_path = output_pdb_path
        # Properties specific for BB
        self.mutation_list = properties.get('mutation_list', None)
        # Common in all BB
        self.global_log = properties.get('global_log', None)
        self.prefix = properties.get('prefix', None)
        self.step = properties.get('step', None)
        self.path = properties.get('path', '')

    def launch(self):
        """
        Model the missing atoms in side chains.
        """
        options_dict = {'force_save': False,
                        'command': 'mutateside',
                        'data_dir': None,
                        'json_output_path': None,
                        'data_library_path': None,
                        'res_lib_path': None,
                        'quiet': False,
                        'output_structure_path': self.output_pdb_path,
                        'options': ['--mut', self.mutation_list],
                        'non_interactive': False,
                        'debug': False,
                        'check_only': False,
                        'input_structure_path': self.input_pdb_path}

        sets = DefaultSettings(os.path.dirname(sc.__file__))

        out_log_file_path = fu.create_name(path=self.path, prefix=self.prefix, step=self.step, name='log.out')
        fu.create_dir(os.path.dirname(os.path.abspath(out_log_file_path)))

        with open(out_log_file_path, 'w') as out_log:
            old_stdout = sys.stdout
            sys.stdout = out_log
            StructureChecking(sets, options_dict).launch()
            sys.stdout = old_stdout


def main():
    """
    Command line interface.
    """
    parser = argparse.ArgumentParser(description="Model the missing atoms in aminoacid side chains of a PDB.")
    parser.add_argument('--config', required=True)
    parser.add_argument('--system', required=False)
    parser.add_argument('--step', required=False)

    # Specific args of each building block
    parser.add_argument('--input_pdb_path', required=True)
    parser.add_argument('--output_pdb_path', required=True)
    ####

    args = parser.parse_args()
    properties = settings.ConfReader(config=args.config, system=args.system).get_prop_dic()
    if args.step:
        properties = properties[args.step]

    #Specific call of each building block
    Mutate(input_pdb_path=args.input_pdb_path, output_pdb_path=args.output_pdb_path, properties=properties).launch()
    ####

if __name__ == '__main__':
    main()
