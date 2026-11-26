#!/usr/bin/env python3

"""Module containing the FixChirality class and the command line interface."""

from typing import Optional

from biobb_common.generic.biobb_object import BiobbObject, launcher


class FixChirality(BiobbObject):
    """
    | biobb_model FixChirality
    | Fix chirality errors of residues.
    | Fix stereochemical errors in residue side-chains changing It's chirality.

    Args:
        input_pdb_path (str): Input PDB file path. File type: input. `Sample file <https://github.com/bioexcel/biobb_model/raw/master/biobb_model/test/data/model/5s2z.pdb>`_. Accepted formats: pdb (edam:format_1476).
        output_pdb_path (str): Output PDB file path. File type: output. `Sample file <https://github.com/bioexcel/biobb_model/raw/master/biobb_model/test/reference/model/output_amide_pdb_path.pdb>`_. Accepted formats: pdb (edam:format_1476).
        properties (dict - Python dictionary object containing the tool parameters, not input/output files):
            * **modeller_key** (*str*) - (None) Modeller license key.
            * **binary_path** (*str*) - ("check_structure") Path to the check_structure executable binary.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
            * **sandbox_path** (*str*) - ("./") [WF property] Parent path to the sandbox directory.

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

    def __init__(
        self,
        input_pdb_path: str,
        output_pdb_path: str,
        properties: Optional[dict] = None,
        **kwargs,
    ) -> None:
        super().__init__(**locals())

    def run(self) -> None:
        """Execute the :class:`FixChirality <model.fix_chirality.FixChirality>` object."""

        # Create command line
        self.cmd = [
            self.binary_path,
            "-i",
            self.stage_io_dict["in"]["input_pdb_path"],
            "-o",
            self.stage_io_dict["out"]["output_pdb_path"],
            "--force_save",
            "chiral",
            "--fix",
            "All",
        ]

        if self.modeller_key:
            self.cmd.insert(1, self.modeller_key)
            self.cmd.insert(1, "--modeller_key")

        # Run Biobb block
        self.run_biobb()


fix_chirality = launcher(FixChirality)

if __name__ == "__main__":
    FixChirality.main()
