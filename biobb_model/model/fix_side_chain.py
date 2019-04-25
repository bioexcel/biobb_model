#!/usr/bin/env python3

"""Module containing the FixSideChain class and the command line interface."""
import argparse
from biobb_common.configuration import settings
from biobb_common.tools import file_utils as fu
from biobb_common.command_wrapper import cmd_wrapper

class FixSideChain():
    """Class to model the missing atoms in aminoacid side chains of a PDB.

    Args:
        input_pdb_path (str): Input PDB file path.
        output_pdb_path (str): Output PDB file path.
        properties (dic): (None) Empty dictionary by default.
    """
    def __init__(self, input_pdb_path, output_pdb_path, properties=None, **kwargs):
        properties = properties or {}

        # Input/Output files
        self.input_pdb_path = input_pdb_path
        self.output_pdb_path = output_pdb_path

        # Properties specific for BB
        self.check_structure_path = properties.get('check_structure_path', 'check_structure')

        # Common in all BB
        self.can_write_console_log = properties.get('can_write_console_log', True)
        self.global_log = properties.get('global_log', None)
        self.prefix = properties.get('prefix', None)
        self.step = properties.get('step', None)
        self.path = properties.get('path', '')

    def launch(self):
        """Model the missing atoms in side chains."""
        out_log, err_log = fu.get_logs(path=self.path, prefix=self.prefix, step=self.step, can_write_console=self.can_write_console_log)

        cmd = [self.check_structure_path,
               '-i', self.input_pdb_path,
               '-o', self.output_pdb_path,
               '--force_save',
               'fixside', '--fix', 'ALL']

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
    FixSideChain(input_pdb_path=args.input_pdb_path, output_pdb_path=args.output_pdb_path, properties=properties).launch()
    ####

if __name__ == '__main__':
    main()
