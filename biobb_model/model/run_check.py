#!/usr/bin/env python3

"""Module containing the Check class and the command line interface."""
import argparse
import shutil
from pathlib import Path, PurePath
from biobb_common.configuration import  settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
from biobb_common.command_wrapper import cmd_wrapper

class Check():
    """Description for the Check (http://templatedocumentation.org) module.

    Args:
        input_file_path (str): Path to input PDB File. File type: input. `Sample file <https://urlto.sample>`_. Accepted formats: pdb, cif.
        input_sequence_path (str) (Optional): Canonical sequence (optional). File type: fasta. `Sample file <https://urlto.sample>`_. Accepted formats: fasta.
        output_file_path (str): Output PDB file. File type: output. `Sample file <https://urlto.sample>`_. Accepted formats: pdb.
        properties (dic):
            * **command** (*str*) - Command to perform
            * **command_options** (*str*) - Specific options to command
            * **check_only** (*bool*) - Check only. No fix
            * **modeller_key**(*str*) - License key for Modeller (required for backbond rebuilding)
            * **executable_binary_property** (*str*) - ("check_structure")
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
    """

    def __init__(self, input_file_path, input_sequence_path, output_file_path, properties, **kwargs):
        properties = properties or {}

        # Input/Output files
        self.io_dict = { 
            'in': { 
                'input_file_path': input_file_path, 
                'input_sequence_path': input_sequence_path 
            }, 
            'out': { 'output_file_path': output_file_path } 
        }

        # Properties specific for BB
        self.properties = properties
        self.check_only_property = properties.get('check_only', False)        
        self.command = properties.get('command', 'checkall')
        self.command_options = properties.get('command_options', '')
        self.modeller_key = properties.get('modeller_key', '')
        self.executable_binary_property = properties.get('executable_binary_property', 'check_structure')

        # Properties common in all BB
        self.can_write_console_log = properties.get('can_write_console_log', True)
        self.global_log = properties.get('global_log', None)
        self.prefix = properties.get('prefix', None)
        self.step = properties.get('step', None)
        self.path = properties.get('path', '')
        self.remove_tmp = properties.get('remove_tmp', True)
        self.restart = properties.get('restart', False)

    @launchlogger
    def launch(self):
        """Launches the execution of the check module."""
        
        # Get local loggers from launchlogger decorator
        out_log = getattr(self, 'out_log', None)
        err_log = getattr(self, 'err_log', None)

        # Check the properties
        fu.check_properties(self, self.properties)

        # Restart
        if self.restart:
            output_file_list = [self.io_dict['out']['output_file_path']]
            if fu.check_complete_files(output_file_list):
                fu.log('Restart is enabled, this step: %s will the skipped' % self.step, out_log, self.global_log)
                return 0

        # Creating temporary folder
        self.tmp_folder = fu.create_unique_dir()
        fu.log('Creating %s temporary folder' % self.tmp_folder, out_log)

        # Copy input_file_path to temporary folder
        shutil.copy(self.io_dict['in']['input_file_path'], self.tmp_folder)
        if self.io_dict['in']['input_sequence_path']:
            # Copy input_file_path2 to temporary folder
            shutil.copy(self.io_dict['in']['input_sequence_path'], self.tmp_folder)

        # Instructions for command line
        instructions = ['--non_interactive', '--force_save']
        if self.check_only_property:
            instructions.append('--check_only')
        # Command and options should go at the end of the command line
        instructions.append(self.command)
        instructions.append(self.command_options)
        
        # Creating command line

        cmd = [self.executable_binary_property]
        cmd.append('-i')
        cmd.append(str(PurePath(self.tmp_folder).joinpath(PurePath(self.io_dict['in']['input_file_path']).name)))
        cmd.append('-o')
        cmd.append(self.io_dict['out']['output_file_path'])             

        # Add optional input file if provided
        if self.io_dict['in']['input_sequence_path']:
            # Append optional input_sequence_path to cmd
            cmd.append('--sequence')
            cmd.append(str(PurePath(self.tmp_folder).joinpath(PurePath(self.io_dict['in']['input_sequence_path']).name)))

        cmd.append(' '.join(instructions))
        
        fu.log('Creating command line with instructions and required arguments', out_log, self.global_log)
        
        # Launch execution
        returncode = cmd_wrapper.CmdWrapper(cmd, out_log, err_log, self.global_log).launch()

        # Remove temporary file(s)
        if self.remove_tmp: 
            fu.rm(self.tmp_folder)
            fu.log('Removed: %s' % str(self.tmp_folder), out_log)

        return returncode

def main():
    parser = argparse.ArgumentParser(description='Description for the template module.', formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('--config', required=False, help='Configuration file')

    # Specific args of each building block
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_file_path', required=True, help='Input structure file path. Accepted formats: pdb,cif.')
    parser.add_argument('--input_sequence_path', required=False, help='Input canonical sequence (optional). Accepted formats: Fasta.')
    parser.add_argument('--modeller_key', required=False, help='Modeller license key (optional). Accepted formats: str.')
    required_args.add_argument('--output_file_path', required=True, help='Output strucure file. Accepted formats: pdb.')

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config).get_prop_dic()

    # Specific call of each building block
    Check(input_file_path=args.input_file_path, input_sequence_path=args.input_sequence_path, 
             output_file_path=args.output_file_path, 
             properties=properties).launch()

if __name__ == '__main__':
    main()
