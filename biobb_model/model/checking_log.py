#!/usr/bin/env python3

"""Module containing the CheckingLog class and the command line interface."""
import argparse
from biobb_common.configuration import settings
from biobb_common.tools import file_utils as fu
from biobb_common.command_wrapper import cmd_wrapper
from biobb_common.tools.file_utils import launchlogger


class CheckingLog:
    """
    | biobb_model CheckingLog
    | Class to check the errors of a PDB structure.
    | Check the errors of a PDB structure and create a report log file.

    Args:
        input_pdb_path (str): Input PDB file path. File type: input. `Sample file <https://github.com/bioexcel/biobb_model/raw/master/biobb_model/test/data/model/2ki5.pdb>`_. Accepted formats: pdb (edam:format_1476).
        output_log_path (str): Output report log file path. File type: output. `Sample file <https://github.com/bioexcel/biobb_model/raw/master/biobb_model/test/reference/model/checking.log>`_.  Accepted formats: log (edam:format_2330).
        properties (dict - Python dictionary object containing the tool parameters, not input/output files):
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_model.model.checking_log import checking_log
            prop = { 'restart': False }
            checking_log(input_pdb_path='/path/to/myStructure.pdb',
                         output_log_path='/path/to/myReport.log',
                         properties=prop)

    Info:
        * wrapped_software:
            * name: In house
            * license: Apache-2.0
        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl
    """

    def __init__(self, input_pdb_path: str, output_log_path: str, properties: dict = None, **kwargs) -> None:
        properties = properties or {}

        # Input/Output files
        self.io_dict = {
            "in": {"input_pdb_path": input_pdb_path},
            "out": {"output_log_path": output_log_path}
        }

        # Properties specific for BB
        self.check_structure_path = properties.get('check_structure_path', 'check_structure')

        # Properties common in all BB
        self.can_write_console_log = properties.get('can_write_console_log', True)
        self.global_log = properties.get('global_log', None)
        self.prefix = properties.get('prefix', None)
        self.step = properties.get('step', None)
        self.path = properties.get('path', '')
        self.remove_tmp = properties.get('remove_tmp', True)
        self.restart = properties.get('restart', False)

        # Check the properties
        fu.check_properties(self, properties)

    @launchlogger
    def launch(self) -> int:
        """Execute the :class:`CheckingLog <model.checking_log.CheckingLog>` object."""
        tmp_files = []

        # Get local loggers from launchlogger decorator
        out_log = getattr(self, 'out_log', None)
        err_log = getattr(self, 'err_log', None)

        # Restart if needed
        if self.restart:
            if fu.check_complete_files(self.io_dict["out"].values()):
                fu.log('Restart is enabled, this step: %s will the skipped' % self.step, out_log, self.global_log)
                return 0

        # check_structure -i biobb_model/test/data/model/2ki5.pdb checkall > checking.log
        cmd = [self.check_structure_path,
               '-i', self.io_dict["in"]["input_pdb_path"],
               "checkall",
               '>', self.io_dict["out"]["output_log_path"]
               ]

        returncode = cmd_wrapper.CmdWrapper(cmd, out_log, err_log, self.global_log).launch()

        if self.remove_tmp:
            fu.rm_file_list(tmp_files, out_log=out_log)

        return returncode


def checking_log(input_pdb_path: str, output_log_path: str, properties: dict = None, **kwargs) -> int:
    """Create :class:`CheckingLog <model.checking_log.CheckingLog>` class and
    execute the :meth:`launch() <model.checking_log.CheckingLog.launch>` method."""
    return CheckingLog(input_pdb_path=input_pdb_path,
                       output_log_path=output_log_path,
                       properties=properties, **kwargs).launch()


def main():
    parser = argparse.ArgumentParser(description="Check the errors of a PDB structure and create a report log file.",
                                     formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('-c', '--config', required=False, help="This file can be a YAML file, JSON file or JSON string")

    # Specific args of each building block
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('-i', '--input_pdb_path', required=True, help="Input PDB file name")
    required_args.add_argument('-o', '--output_log_path', required=True, help="Output log file name")

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config).get_prop_dic()

    # Specific call of each building block
    checking_log(input_pdb_path=args.input_pdb_path,
                 output_log_path=args.output_log_path,
                 properties=properties)


if __name__ == '__main__':
    main()
