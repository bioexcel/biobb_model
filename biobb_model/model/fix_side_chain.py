#!/usr/bin/env python3

"""
Module containing the FixSideChain class and the command line interface
"""

import argparse
import sys
import os
from biobb_common.configuration import settings
from biobb_common.tools import file_utils as fu
import structure_checking.structure_checking as sc
from structure_checking.structure_checking import StructureChecking
from structure_checking.default_settings import DefaultSettings


class FixSideChain():
    """Class to model the missing atoms in aminoacid side chains of a PDB.
    Args:
        input_pdb_path (str) - Input PDB file path.
        output_pdb_path (str) - Output PDB file path.
        properties (dic):
    """
    def __init__(self, input_pdb_path, output_pdb_path, properties, **kwargs):
        # Input/Output files
        self.input_pdb_path = input_pdb_path
        self.output_pdb_path = output_pdb_path
        # Properties specific for BB
        # Common in all BB
        self.global_log = properties.get('global_log', None)
        self.prefix = properties.get('prefix', None)
        self.step = properties.get('step', None)
        self.path = properties.get('path', '')

    def launch(self):
        """
        Model the missing atoms in side chains.
        """

        options_dict = {'input_structure_path': self.input_pdb_path,
                        'options': ['--fix', 'All'],
                        'output_structure_path': self.output_pdb_path,
                        'force_save': False,
                        'res_lib_path': None,
                        'debug': False,
                        'command': 'fixside',
                        'json_output_path': None,
                        'quiet': False,
                        'data_library_path': None,
                        'non_interactive': False,
                        'check_only': False,
                        'data_dir': None}

        sets = DefaultSettings(os.path.dirname(sc.__file__))

        out_log_file_path = fu.create_name(path=self.path, prefix=self.prefix, step=self.step, name='log.out')
        fu.create_dir(os.path.dirname(os.path.abspath(out_log_file_path)))

        with open(out_log_file_path, 'w') as out_log:
            old_stdout = sys.stdout
            sys.stdout = out_log
            StructureChecking(sets, options_dict).launch()
            sys.stdout = old_stdout


def main():
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
    FixSideChain(input_pdb_path=args.input_pdb_path, output_pdb_path=args.output_pdb_path, properties=properties).launch()
    ####

if __name__ == '__main__':
    main()
