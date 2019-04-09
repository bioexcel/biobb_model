#!/usr/bin/env python3

"""Module containing the Mutate class and the command line interface."""
import argparse
import sys
import os
from biobb_common.configuration   import settings
from biobb_common.tools import file_utils as fu
from biobb_common.command_wrapper import cmd_wrapper
import biobb_model.structure_checking.structure_checking as sc
from biobb_model.structure_checking.structure_checking import StructureChecking
from biobb_model.structure_checking.default_settings import DefaultSettings

class Mutate():
    """Class to mutate one aminoacid by another in a 3d structure.

    Args:
        input_pdb_path (str): Input PDB file path.
        output_pdb_path (str): Output PDB file path.
        properties (dic):
            | - **mutation_list** (*str*): ("A:Val2Ala") Mutation list in the format "Chain:WT_AA_ThreeLeterCode Resnum MUT_AA_ThreeLeterCode" (no spaces between the elements) separated by commas. If no chain is provided as chain code all the chains in the pdb file will be mutated. ie: "A:ALA15CYS"
    """
    def __init__(self, input_pdb_path, output_pdb_path, properties=None, **kwargs):
        properties = properties or {}

        # Input/Output files
        self.input_pdb_path = input_pdb_path
        self.output_pdb_path = output_pdb_path

        # Properties specific for BB
        self.check_structure_path = properties.get('check_structure_path', 'check_structure')
        self.mutation_list = properties.get('mutation_list', 'A:Val2Ala').replace(" ","")

        # Common in all BB
        self.can_write_console_log = properties.get('can_write_console_log', True)
        self.global_log = properties.get('global_log', None)
        self.prefix = properties.get('prefix', None)
        self.step = properties.get('step', None)
        self.path = properties.get('path', '')

    def launch(self):
        """Mutate one or more aminoacids."""
        out_log, err_log = fu.get_logs(path=self.path, prefix=self.prefix, step=self.step, can_write_console=self.can_write_console_log)
        cmd = [self.check_structure_path,
               '-i', self.input_pdb_path,
               '-o', self.output_pdb_path,
               'mutateside', '--mut', self.mutation_list]

        command = cmd_wrapper.CmdWrapper(cmd, out_log, err_log, self.global_log)
        return command.launch()

def main():
    """Command line interface."""
    parser = argparse.ArgumentParser(description="Model the missing atoms in aminoacid side chains of a PDB.", formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('-c', '--config', required=False, help="This file can be a YAML file, JSON file or JSON string")
    parser.add_argument('--system', required=False, help="Check 'https://biobb-common.readthedocs.io/en/latest/system_step.html' for help")
    parser.add_argument('--step', required=False, help="Check 'https://biobb-common.readthedocs.io/en/latest/system_step.html' for help")

    #Specific args of each building block
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('-i', '--input_pdb_path', required=True, help="Input PDB file name")
    required_args.add_argument('-o', '--output_pdb_path', required=True, help="Output PDB file name")
    ####

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config, system=args.system).get_prop_dic()
    if args.step:
        properties = properties[args.step]

    #Specific call of each building block
    Mutate(input_pdb_path=args.input_pdb_path, output_pdb_path=args.output_pdb_path, properties=properties).launch()

if __name__ == '__main__':
    main()
