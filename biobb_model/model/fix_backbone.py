#!/usr/bin/env python3

"""Module containing the FixBackbone class and the command line interface."""

from typing import Optional

from biobb_common.generic.biobb_object import launcher

from biobb_model.model.common import CheckStructureBase


class FixBackbone(CheckStructureBase):
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
            * **extra_gap** (*int*) - (0) Recover additional residues from the model on either side of the break to help fix loop connections.
            * **fix_known** (*bool*) - (False) Optimize only the missing residues with Modeller, the residues in the structure keep their coordinates.
            * **modeller_key** (*str*) - (None) Modeller license key.
            * **binary_path** (*str*) - ("check_structure") Path to the check_structure executable binary.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
            * **sandbox_path** (*str*) - ("./") [WF property] Parent path to the sandbox directory.

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

    def __init__(
        self,
        input_pdb_path: str,
        input_fasta_canonical_sequence_path: str,
        output_pdb_path: str,
        properties: Optional[dict] = None,
        **kwargs,
    ) -> None:
        super().__init__(**locals())

    def run(self) -> None:
        """Execute the :class:`FixBackbone <model.fix_backbone.FixBackbone>` object."""
        options = ["--add_caps", "All" if self.add_caps else "None"]
        if self.extra_gap:
            options += ["--extra_gap", str(self.extra_gap)]
        if self.fix_known:
            options.append("--fix_known")
        self.run_check_structure(
            "--sequence", self.stage_io_dict["in"]["input_fasta_canonical_sequence_path"], "--non_interactive",
            "backbone", "--fix_atoms", "All", "--fix_chain", "All", *options,
        )


fix_backbone = launcher(FixBackbone)

if __name__ == "__main__":
    FixBackbone.main()
