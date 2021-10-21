#!/usr/bin/env python3

"""Module containing the FixChirality class and the command line interface."""
import argparse
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.configuration import settings
from biobb_common.tools import file_utils as fu
from biobb_common.command_wrapper import cmd_wrapper
from biobb_common.tools.file_utils import launchlogger


class FixChirality(BiobbObject):
    """
    | biobb_model FixChirality
    | Fix chirality errors of residues.
    | Fix stereochemical errors in residue side-chains changing It's chirality.

    Args:
        input_pdb_path (str): Input PDB file path. File type: input. `Sample file <https://github.com/bioexcel/biobb_model/raw/master/biobb_model/test/data/model/5s2z.pdb>`_. Accepted formats: pdb (edam:format_1476).
        output_pdb_path (str): Output PDB file path. File type: output. `Sample file <https://github.com/bioexcel/biobb_model/raw/master/biobb_model/test/reference/model/output_amide_pdb_path.pdb>`_. Accepted formats: pdb (edam:format_1476).
        properties (dict - Python dictionary object containing the tool parameters, not input/output files):
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_model.model.fix_chirality import fix_chirality
            prop = { 'restart': False }
            fix_chirality(input_pdb_path='/path/to/myStructure.pdb',
                          output_pdb_path='/path/to/newStructure.pdb',
                          properties=prop)

    Info:
        * wrapped_software:
            * name: In house
            * license: Apache-2.0
        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl
    """

    def __init__(self, input_pdb_path: str, output_pdb_path: str, properties: dict = None, **kwargs) -> None:
        properties = properties or {}

        # Call parent class constructor
        super().__init__(properties)

        # Input/Output files
        self.io_dict = {
            "in": {"input_pdb_path": input_pdb_path},
            "out": {"output_pdb_path": output_pdb_path}
        }

        # Properties specific for BB
        self.check_structure_path = properties.get('check_structure_path', 'check_structure')

        # Check the properties
        self.check_properties(properties)

    @launchlogger
    def launch(self) -> int:
        """Execute the :class:`FixChirality <model.fix_amides.FixChirality>` object."""

        # Setup Biobb
        if self.check_restart(): return 0
        self.stage_files()

        # Create command line
        self.cmd = [self.check_structure_path,
                    '-i', self.stage_io_dict["in"]["input_pdb_path"],
                    '-o', self.stage_io_dict["out"]["output_pdb_path"],
                    '--force_save', 'chiral',
                    '--fix', 'All']

        # Run Biobb block
        self.run_biobb()

        # Copy files to host
        self.copy_to_host()

        # Remove temporal files
        self.remove_tmp_files()

        return self.return_code


def fix_chirality(input_pdb_path: str, output_pdb_path: str, properties: dict = None, **kwargs) -> int:
    """Create :class:`FixChirality <model.fix_amides.FixChirality>` class and
    execute the :meth:`launch() <model.fix_amides.FixChirality.launch>` method."""
    return FixChirality(input_pdb_path=input_pdb_path,
                        output_pdb_path=output_pdb_path,
                        properties=properties, **kwargs).launch()


def main():
    parser = argparse.ArgumentParser(description="Fix stereochemical errors in residues changing It's chirality.",
                                     formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('-c', '--config', required=False, help="This file can be a YAML file, JSON file or JSON string")

    # Specific args of each building block
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('-i', '--input_pdb_path', required=True, help="Input PDB file name")
    required_args.add_argument('-o', '--output_pdb_path', required=True, help="Output PDB file name")

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config).get_prop_dic()

    # Specific call of each building block
    fix_chirality(input_pdb_path=args.input_pdb_path,
                  output_pdb_path=args.output_pdb_path,
                  properties=properties)


if __name__ == '__main__':
    main()
