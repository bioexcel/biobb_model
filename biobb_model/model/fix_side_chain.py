#!/usr/bin/env python3

"""Module containing the FixSideChain class and the command line interface."""

from typing import Optional

from biobb_common.generic.biobb_object import launcher

from biobb_model.model.common import CheckStructureBase


class FixSideChain(CheckStructureBase):
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
            * **sandbox_path** (*str*) - ("./") [WF property] Parent path to the sandbox directory.

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

    def __init__(
        self,
        input_pdb_path: str,
        output_pdb_path: str,
        properties: Optional[dict] = None,
        **kwargs,
    ) -> None:
        super().__init__(**locals())

    def run(self) -> None:
        """Execute the :class:`FixSideChain <model.fix_side_chain.FixSideChain>` object."""
        self.run_check_structure("fixside", "--fix", "ALL", *self.modeller_rebuild())


fix_side_chain = launcher(FixSideChain)

if __name__ == "__main__":
    FixSideChain.main()
