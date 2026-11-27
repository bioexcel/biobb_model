#!/usr/bin/env python3

"""Module containing the FixSSBonds class and the command line interface."""

from typing import Optional

from biobb_common.generic.biobb_object import launcher

from biobb_model.model.common import CheckStructureBase


class FixSSBonds(CheckStructureBase):
    """
    | biobb_model FixSSBonds
    | Fix SS bonds from residues.
    | Fix the SS bonds in a PDB structure.

    Args:
        input_pdb_path (str): Input PDB file path. File type: input. `Sample file <https://github.com/bioexcel/biobb_model/raw/master/biobb_model/test/data/model/1aki.pdb>`_. Accepted formats: pdb (edam:format_1476).
        output_pdb_path (str): Output PDB file path. File type: output. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_model/master/biobb_model/test/reference/model/output_ssbonds.pdb>`_. Accepted formats: pdb (edam:format_1476).
        properties (dict - Python dictionary object containing the tool parameters, not input/output files):
            * **modeller_key** (*str*) - (None) Modeller license key.
            * **binary_path** (*str*) - ("check_structure") Path to the check_structure executable binary.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
            * **sandbox_path** (*str*) - ("./") [WF property] Parent path to the sandbox directory.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_model.model.fix_ssbonds import fix_ssbonds
            prop = { 'restart': False }
            fix_ssbonds(input_pdb_path='/path/to/myStructure.pdb',
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
        """Execute the :class:`FixSSBonds <model.fix_ssbonds.FixSSBonds>` object."""
        self.run_check_structure("--non_interactive", "getss", "--mark", "All")


fix_ssbonds = launcher(FixSSBonds)

if __name__ == "__main__":
    FixSSBonds.main()
