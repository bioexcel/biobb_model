#!/usr/bin/env python3

"""Module containing the FixPdb class and the command line interface."""
import argparse
from typing import Dict, Optional, Any
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.configuration import settings
from biobb_common.tools.file_utils import launchlogger

from .fix_pdb_utils import Structure, generate_map_online


class FixPdb(BiobbObject):
    """
    | biobb_model FixPdb
    | Class to renumerate residues in a PDB structure according to a reference sequence from UniProt.
    | Fix the residue numbering in a PDB structure according to a reference sequence from UniProt.

    Args:
        input_pdb_path (str): Input PDB file path. File type: input. `Sample file <https://github.com/bioexcel/biobb_model/raw/master/biobb_model/test/data/model/2ki5.pdb>`_. Accepted formats: pdb (edam:format_1476).
        output_pdb_path (str): Output PDB file path. File type: output. `Sample file <https://github.com/bioexcel/biobb_model/raw/master/biobb_model/test/reference/model/output_pdb_path.pdb>`_. Accepted formats: pdb (edam:format_1476).
        properties (dict - Python dictionary object containing the tool parameters, not input/output files):
            * **forced_uniprot_references** (*str*) - (None) Set the UniProt accessions for sequences to be used as reference.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
    Examples:
        This is a use example of how to use the building block from Python::
            from biobb_model.model.fix_pdb import fix_pdb
            prop = { 'forced_uniprot_references': ["P00533"] }
            fix_pdb(input_pdb_path='/path/to/myStructure.pdb', output_pdb_path='/path/to/newStructure.pdb', properties=prop)
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
        self.forced_uniprot_references = properties.get('forced_uniprot_references')
        # If input forced uniprot references is a string and not a list then convert it
        if isinstance(self.forced_uniprot_references, str):
            self.forced_uniprot_references = self.forced_uniprot_references.split(' ')

        # Check the properties
        self.check_properties(properties)
        self.check_arguments()

    @launchlogger
    def launch(self) -> int:
        """Execute the :class:`FixPdb <model.fix_pdb.FixPdb>` object."""

        # Setup Biobb
        if self.check_restart():
            return 0

        # Run code
        self.return_code = 0

        # Get the user arguments
        input_pdb_path = self.io_dict["in"]["input_pdb_path"]
        output_pdb_path = self.io_dict["out"]["output_pdb_path"]
        forced_uniprot_references = self.forced_uniprot_references

        # Read and parse the input pdb file
        structure = Structure.from_pdb_file(input_pdb_path)

        # Add protein chains in case they are missing
        chains = structure.chains
        if len(chains) == 0 or (len(chains) == 1 and (chains[0].name == ' ' or chains[0].name == 'X')):
            structure.raw_protein_chainer()

        # Run all the mapping function
        mapping: Optional[Dict[Any, Any]] = {}
        if forced_uniprot_references:
            mapping = generate_map_online(structure, forced_uniprot_references)

        # In case something went wrong with the mapping stop here
        if not mapping:
            self.return_code = -1
            return self.return_code

        # Change residue numbers in the structure according to the mapping results
        mapped_residue_numbers = mapping['residue_reference_numbers']
        for r, residue in enumerate(structure.residues):
            mapped_residue_number = mapped_residue_numbers[r]
            if mapped_residue_number is None:
                continue
            residue.number = mapped_residue_number

        # Write the modified structure to a new pdb file
        structure.generate_pdb_file(output_pdb_path)

        print('Fixed :)')

        # Remove temporal files
        self.tmp_files.extend([self.stage_io_dict.get("unique_dir", "")])
        self.remove_tmp_files()

        self.check_arguments(output_files_created=True, raise_exception=False)
        return self.return_code


def fix_pdb(input_pdb_path: str, output_pdb_path: str, properties: Optional[Dict] = None, **kwargs) -> int:
    """Create :class:`FixPdb <model.fix_pdb.FixPdb>` class and
    execute the :meth:`launch() <model.fix_pdb.FixPdb.launch>` method."""
    return FixPdb(input_pdb_path=input_pdb_path,
                  output_pdb_path=output_pdb_path,
                  properties=properties, **kwargs).launch()


def main():
    parser = argparse.ArgumentParser(description="Model the missing atoms in the backbone of a PDB structure.",
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
    fix_pdb(input_pdb_path=args.input_pdb_path,
            output_pdb_path=args.output_pdb_path,
            properties=properties)


if __name__ == '__main__':
    main()
