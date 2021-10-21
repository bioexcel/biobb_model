#!/usr/bin/env python3

"""Module containing the FixBackbone class and the command line interface."""
import argparse
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.configuration import settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
from biobb_model.model.common import modeller_installed


class FixBackbone(BiobbObject):
    """
    | biobb_model FixBackbone
    | Class to model the missing atoms in the backbone of a PDB structure.
    | Model the missing atoms in the backbone of a PDB structure using `biobb_structure_checking <https://anaconda.org/bioconda/biobb_structure_checking>`_ and the `Modeller suite <https://salilab.org/modeller/>`_.

    Args:
        input_pdb_path (str): Input PDB file path. File type: input. `Sample file <https://github.com/bioexcel/biobb_model/raw/master/biobb_model/test/data/model/2ki5.pdb>`_. Accepted formats: pdb (edam:format_1476).
        input_fasta_canonical_sequence_path (str): Input FASTA file path. File type: input. `Sample file <https://github.com/bioexcel/biobb_model/raw/master/biobb_model/test/data/model/2ki5.fasta>`_. Accepted formats: fasta (edam:format_1476).
        output_pdb_path (str): Output PDB file path. File type: output. `Sample file <https://github.com/bioexcel/biobb_model/raw/master/biobb_model/test/reference/model/output_pdb_path.pdb>`_. Accepted formats: pdb (edam:format_1476).
        properties (dict - Python dictionary object containing the tool parameters, not input/output files):
            * **add_caps** (*bool*) - (False) Add caps to terminal residues.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_model.model.fix_backbone import fix_backbone
            prop = { 'restart': False }
            fix_backbone(input_pdb_path='/path/to/myStructure.pdb',
                         input_fasta_canonical_sequence_path='/path/to/myCanonicalSequence.fasta',
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

    def __init__(self, input_pdb_path: str, input_fasta_canonical_sequence_path: str, output_pdb_path: str,
                 properties: dict = None, **kwargs) -> None:
        properties = properties or {}

        # Call parent class constructor
        super().__init__(properties)

        # Input/Output files
        self.io_dict = {
            "in": {"input_pdb_path": input_pdb_path,
                   "input_fasta_canonical_sequence_path": input_fasta_canonical_sequence_path},
            "out": {"output_pdb_path": output_pdb_path}
        }

        # Properties specific for BB
        self.check_structure_path = properties.get('check_structure_path', 'check_structure')
        self.add_caps = properties.get('add_caps', False)

        # Check the properties
        self.check_properties(properties)

    @launchlogger
    def launch(self) -> int:
        """Execute the :class:`FixBackbone <model.fix_backbone.FixBackbone>` object."""

        # Setup Biobb
        if self.check_restart(): return 0
        self.stage_files()

        # Create command line
        self.cmd = ['echo', '-e', '\'' + self.io_dict["in"]["input_fasta_canonical_sequence_path"] + '\'', '|',
                    self.check_structure_path,
                    '-i', self.io_dict["in"]["input_pdb_path"],
                    '-o', self.io_dict["out"]["output_pdb_path"],
                    '--force_save', 'backbone',
                    '--fix_atoms', 'All',
                    '--fix_chain', 'All',
                    '--add_caps']

        if self.add_caps:
            self.cmd.append('All')
        else:
            self.cmd.append('None')

        if not modeller_installed(self.out_log, self.global_log):
            fu.log(f"Modeller is not installed, the execution of this block will be interrupted", self.out_log, self.global_log)
            return 1

        # Run Biobb block
        self.run_biobb()

        # Copy files to host
        self.copy_to_host()

        # Remove temporal files
        self.remove_tmp_files()

        return self.return_code


def fix_backbone(input_pdb_path: str, input_fasta_canonical_sequence_path: str, output_pdb_path: str,
                 properties: dict = None, **kwargs) -> int:
    """Create :class:`FixBackbone <model.fix_backbone.FixBackbone>` class and
    execute the :meth:`launch() <model.fix_backbone.FixBackbone.launch>` method."""
    return FixBackbone(input_pdb_path=input_pdb_path,
                       input_fasta_canonical_sequence_path=input_fasta_canonical_sequence_path,
                       output_pdb_path=output_pdb_path,
                       properties=properties, **kwargs).launch()


def main():
    parser = argparse.ArgumentParser(description="Model the missing atoms in the backbone of a PDB structure.",
                                     formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('-c', '--config', required=False, help="This file can be a YAML file, JSON file or JSON string")

    # Specific args of each building block
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('-i', '--input_pdb_path', required=True, help="Input PDB file name")
    required_args.add_argument('-f', '--input_fasta_canonical_sequence_path', required=True, help="Input FASTA file name")
    required_args.add_argument('-o', '--output_pdb_path', required=True, help="Output PDB file name")

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config).get_prop_dic()

    # Specific call of each building block
    fix_backbone(input_pdb_path=args.input_pdb_path,
                 input_fasta_canonical_sequence_path=args.input_fasta_canonical_sequence_path,
                 output_pdb_path=args.output_pdb_path,
                 properties=properties)


if __name__ == '__main__':
    main()
