#!/usr/bin/env python3

"""Module containing the FixSideChain class and the command line interface."""
import argparse
from typing import Dict, Optional
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.configuration import settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
from biobb_model.model.common import modeller_installed


class FixSideChain(BiobbObject):
    """
    | biobb_model FixSideChain
    | Class to model the missing atoms in amino acid side chains of a PDB.
    | Model the missing atoms in amino acid side chains of a PDB using `biobb_structure_checking <https://anaconda.org/bioconda/biobb_structure_checking>`_ if the use_modeller property is added the `Modeller suite <https://salilab.org/modeller/>`_ will also be used to rebuild the missing atoms.

    Args:
        input_pdb_path (str): Input PDB file path. File type: input. `Sample file <https://github.com/bioexcel/biobb_model/raw/master/biobb_model/test/data/model/2ki5.pdb>`_. Accepted formats: pdb (edam:format_1476).
        output_pdb_path (str): Output PDB file path. File type: output. `Sample file <https://github.com/bioexcel/biobb_model/raw/master/biobb_model/test/reference/model/output_pdb_path.pdb>`_. Accepted formats: pdb (edam:format_1476).
        properties (dict - Python dictionary object containing the tool parameters, not input/output files):
            * **use_modeller** (*bool*) - (False) Use `Modeller suite <https://salilab.org/modeller/>`_ to rebuild the missing side chain atoms.
            * **modeller_key** (*str*) - (None) Modeller license key.
            * **binary_path** (*str*) - ("check_structure") Path to the check_structure executable binary.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_model.model.fix_side_chain import fix_side_chain
            prop = { 'use_modeller': True }
            fix_side_chain(input_pdb_path='/path/to/myStructure.pdb',
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

    def __init__(self, input_pdb_path: str, output_pdb_path: str, properties: Optional[Dict] = None, **kwargs) -> None:
        properties = properties or {}

        # Call parent class constructor
        super().__init__(properties)
        self.locals_var_dict = locals().copy()

        # Input/Output files
        self.io_dict = {
            "in": {"input_pdb_path": input_pdb_path},
            "out": {"output_pdb_path": output_pdb_path}
        }

        # Properties specific for BB
        self.binary_path = properties.get('binary_path', 'check_structure')
        self.use_modeller = properties.get('use_modeller', False)
        self.modeller_key = properties.get('modeller_key')

        # Check the properties
        self.check_properties(properties)
        self.check_arguments()

    @launchlogger
    def launch(self) -> int:
        """Execute the :class:`FixSideChain <model.fix_side_chain.FixSideChain>` object."""

        # Setup Biobb
        if self.check_restart():
            return 0
        self.stage_files()

        # Create command line
        self.cmd = [self.binary_path,
                    '-i', self.stage_io_dict["in"]["input_pdb_path"],
                    '-o', self.stage_io_dict["out"]["output_pdb_path"],
                    '--force_save',
                    'fixside', '--fix', 'ALL']

        if self.modeller_key:
            self.cmd.insert(1, self.modeller_key)
            self.cmd.insert(1, '--modeller_key')

        if self.use_modeller:
            if modeller_installed(self.out_log, self.global_log):
                self.cmd.append('--rebuild')
            else:
                fu.log("Modeller is not installed --rebuild option can not be used proceeding without using it", self.out_log, self.global_log)

        # Run Biobb block
        self.run_biobb()

        # Copy files to host
        self.copy_to_host()

        # Remove temporal files
        self.tmp_files.extend([self.stage_io_dict.get("unique_dir", "")])
        self.remove_tmp_files()

        self.check_arguments(output_files_created=True, raise_exception=False)
        return self.return_code


def fix_side_chain(input_pdb_path: str, output_pdb_path: str, properties: Optional[Dict] = None, **kwargs) -> int:
    """Create :class:`FixSideChain <model.fix_side_chain.FixSideChain>` class and
    execute the :meth:`launch() <model.fix_side_chain.FixSideChain.launch>` method."""
    return FixSideChain(input_pdb_path=input_pdb_path,
                        output_pdb_path=output_pdb_path,
                        properties=properties, **kwargs).launch()


def main():
    parser = argparse.ArgumentParser(description="Model the missing atoms in amino acid side chains of a PDB.",
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
    fix_side_chain(input_pdb_path=args.input_pdb_path,
                   output_pdb_path=args.output_pdb_path,
                   properties=properties)


if __name__ == '__main__':
    main()
