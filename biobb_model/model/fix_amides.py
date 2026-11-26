#!/usr/bin/env python3

"""Module containing the FixAmides class and the command line interface."""

from typing import Optional

from biobb_common.generic.biobb_object import launcher

from biobb_model.model.common import CheckStructureBase


class FixAmides(CheckStructureBase):
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
            * **sandbox_path** (*str*) - ("./") [WF property] Parent path to the sandbox directory.

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

    def __init__(
        self,
        input_pdb_path: str,
        output_pdb_path: str,
        properties: Optional[dict] = None,
        **kwargs,
    ) -> None:
        super().__init__(**locals())

    def run(self) -> None:
        """Execute the :class:`FixAmides <model.fix_amides.FixAmides>` object."""
        self.run_check_structure("amide", "--fix", "All")


fix_amides = launcher(FixAmides)

if __name__ == "__main__":
    FixAmides.main()
