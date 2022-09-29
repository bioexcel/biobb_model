#!/usr/bin/env python3

"""Module containing the FixAmides class and the command line interface."""
import argparse
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.configuration import settings
from biobb_common.tools.file_utils import launchlogger


class FixAmides(BiobbObject):
    """
    | biobb_model FixAmides
    | Fix amide groups from residues.
    | Flip the clashing amide groups to avoid clashes.

    Args:
        input_pdb_path (str): Input PDB file path. File type: input. `Sample file <https://github.com/bioexcel/biobb_model/raw/master/biobb_model/test/data/model/5s2z.pdb>`_. Accepted formats: pdb (edam:format_1476).
        output_pdb_path (str): Output PDB file path. File type: output. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_model/master/biobb_model/test/reference/model/output_amide_pdb_path.pdb>`_. Accepted formats: pdb (edam:format_1476).
        properties (dict - Python dictionary object containing the tool parameters, not input/output files):
            * **modeller_key** (*str*) - (None) Modeller license key.
            * **binary_path** (*str*) - ("check_structure") Path to the check_structure executable binary.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_model.model.fix_amides import fix_amides
            prop = { 'restart': False }
            fix_amides(input_pdb_path='/path/to/myStructure.pdb',
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
        self.binary_path = properties.get('binary_path', 'check_structure')
        self.modeller_key = properties.get('modeller_key')

        # Check the properties
        self.check_properties(properties)

    @launchlogger
    def launch(self) -> int:
        """Execute the :class:`FixAmides <model.fix_amides.FixAmides>` object."""

        # Setup Biobb
        if self.check_restart(): return 0
        self.stage_files()

        self.cmd = [self.binary_path,
               '-i', self.stage_io_dict["in"]["input_pdb_path"],
               '-o', self.stage_io_dict["out"]["output_pdb_path"],
               '--force_save',
               'amide', '--fix', 'All']

        if self.modeller_key:
            self.cmd.insert(1, self.modeller_key)
            self.cmd.insert(1, '--modeller_key')

        # Run Biobb block
        self.run_biobb()

        # Copy files to host
        self.copy_to_host()

        # Remove temporal files
        self.remove_tmp_files()

        return self.return_code


def fix_amides(input_pdb_path: str, output_pdb_path: str, properties: dict = None, **kwargs) -> int:
    """Create :class:`FixAmides <model.fix_amides.FixAmides>` class and
    execute the :meth:`launch() <model.fix_amides.FixAmides.launch>` method."""
    return FixAmides(input_pdb_path=input_pdb_path,
                     output_pdb_path=output_pdb_path,
                     properties=properties, **kwargs).launch()


def main():
    parser = argparse.ArgumentParser(description="Flip the clashing amide groups to avoid clashes.",
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
    fix_amides(input_pdb_path=args.input_pdb_path,
               output_pdb_path=args.output_pdb_path,
               properties=properties)


if __name__ == '__main__':
    main()
