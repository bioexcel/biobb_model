#!/usr/bin/env python3

"""Module containing the FixBackbone class and the command line interface."""

from typing import Optional

from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.tools import file_utils as fu


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
        properties = properties or {}

        # Call parent class constructor
        super().__init__(properties)
        self.locals_var_dict = locals().copy()

        # Input/Output files
        self.io_dict = {
            "in": {
                "input_pdb_path": input_pdb_path,
                "input_fasta_canonical_sequence_path": input_fasta_canonical_sequence_path,
            },
            "out": {"output_pdb_path": output_pdb_path},
        }

        # Properties specific for BB
        self.binary_path = properties.get("binary_path", "check_structure")
        self.add_caps = properties.get("add_caps", False)
        self.extra_gap = properties.get("extra_gap", 0)
        self.fix_known = properties.get("fix_known", False)
        self.modeller_key = properties.get("modeller_key")

    def prepare(self) -> None:
        """Create the stdin file with the path of the canonical sequence."""
        self.io_dict["in"]["stdin_file_path"] = fu.create_stdin_file(f'{self.io_dict["in"]["input_fasta_canonical_sequence_path"]}')

    def run(self) -> None:
        """Execute the :class:`FixBackbone <model.fix_backbone.FixBackbone>` object."""

        # Create command line
        self.cmd = [
            self.binary_path,
            "-i",
            self.stage_io_dict["in"]["input_pdb_path"],
            "-o",
            self.stage_io_dict["out"]["output_pdb_path"],
            "--force_save",
            "backbone",
            "--fix_atoms",
            "All",
            "--fix_chain",
            "All",
            "--add_caps",
        ]

        if self.modeller_key:
            self.cmd.insert(5, self.modeller_key)
            self.cmd.insert(5, "--modeller_key")

        if self.add_caps:
            self.cmd.append("All")
        else:
            self.cmd.append("None")
        if self.extra_gap:
            self.cmd.extend(["--extra_gap", str(self.extra_gap)])

        if self.fix_known:
            self.cmd.append("--fix_known")

        # Add stdin input file
        self.cmd.append("<")
        self.cmd.append(self.stage_io_dict["in"]["stdin_file_path"])

        # if not modeller_installed(self.out_log, self.global_log):
        #     fu.log(f"Modeller is not installed, the execution of this block will be interrupted", self.out_log, self.global_log)
        #     return 1

        # Run Biobb block
        self.run_biobb()

        # Remove temporal files
        self.tmp_files.append(self.io_dict["in"].get("stdin_file_path", ""))


def fix_backbone(
    input_pdb_path: str,
    input_fasta_canonical_sequence_path: str,
    output_pdb_path: str,
    properties: Optional[dict] = None,
    **kwargs,
) -> int:
    """Create :class:`FixBackbone <model.fix_backbone.FixBackbone>` class and
    execute the :meth:`launch() <model.fix_backbone.FixBackbone.launch>` method."""
    return FixBackbone(**dict(locals())).launch()


fix_backbone.__doc__ = FixBackbone.__doc__
main = FixBackbone.get_main(fix_backbone, "Model the missing atoms in the backbone of a PDB structure.")

if __name__ == "__main__":
    main()
