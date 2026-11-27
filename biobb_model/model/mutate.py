#!/usr/bin/env python3

"""Module containing the Mutate class and the command line interface."""

from typing import Optional

from biobb_common.generic.biobb_object import launcher

from biobb_model.model.common import CheckStructureBase


class Mutate(CheckStructureBase):
    """
    | biobb_model Mutate
    | Class to mutate one amino acid by another in a 3d structure.
    | Mutate side chain with minimal atom replacement. if the use_modeller property is added the `Modeller suite <https://salilab.org/modeller/>`_ will be used to optimize the side chains.

    Args:
        input_pdb_path (str): Input PDB file path. File type: input. `Sample file <https://github.com/bioexcel/biobb_model/raw/master/biobb_model/test/data/model/2ki5.pdb>`_. Accepted formats: pdb (edam:format_1476).
        output_pdb_path (str): Output PDB file path. File type: output. `Sample file <https://github.com/bioexcel/biobb_model/raw/master/biobb_model/test/reference/model/output_mutated_pdb_path.pdb>`_. Accepted formats: pdb (edam:format_1476).
        properties (dict - Python dictionary object containing the tool parameters, not input/output files):
            * **mutation_list** (*str*) - (None) Mutation list in the format "Chain:WT_AA_ThreeLeterCode Resnum MUT_AA_ThreeLeterCode" (no spaces between the elements) separated by commas. If no chain is provided as chain code all the chains in the pdb file will be mutated. ie: "A:ALA15CYS"
            * **use_modeller** (*bool*) - (False) Use `Modeller suite <https://salilab.org/modeller/>`_ to optimize the side chains.
            * **modeller_key** (*str*) - (None) Modeller license key.
            * **binary_path** (*str*) - ("check_structure") Path to the check_structure executable binary.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
            * **sandbox_path** (*str*) - ("./") [WF property] Parent path to the sandbox directory.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_model.model.mutate import mutate
            prop = { 'mutation_list': 'A:Val2Ala',
                     'use_modeller': True }
            mutate(input_pdb_path='/path/to/myStructure.pdb',
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

        # Properties specific for BB
        self.mutation_list = (self.mutation_list or "").replace(" ", "")

    def run(self) -> None:
        """Execute the :class:`Mutate <model.mutate.Mutate>` object."""
        mutations = ["--mut", self.mutation_list] if self.mutation_list else []
        self.run_check_structure("--non_interactive", "mutateside", *mutations, *self.modeller_rebuild())


mutate = launcher(Mutate)

if __name__ == "__main__":
    Mutate.main()
