#!/usr/bin/env python3

"""Module containing the FixAltLocs class and the command line interface."""

from typing import Optional

from biobb_common.generic.biobb_object import launcher
from biobb_common.tools import file_utils as fu

from biobb_model.model.common import CheckStructureBase


class FixAltLocs(CheckStructureBase):
    """
    | biobb_model FixAltLocs
    | Fix alternate locations from residues.
    | Fix alternate locations using the altlocs list or occupancy.

    Args:
        input_pdb_path (str): Input PDB file path. File type: input. `Sample file <https://github.com/bioexcel/biobb_model/raw/master/biobb_model/test/data/model/3ebp.pdb>`_. Accepted formats: pdb (edam:format_1476).
        output_pdb_path (str): Output PDB file path. File type: output. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_model/master/biobb_model/test/reference/model/output_altloc.pdb>`_. Accepted formats: pdb (edam:format_1476).
        properties (dict - Python dictionary object containing the tool parameters, not input/output files):
            * **altlocs** (*list*) - (None) List of alternate locations to fix. Format: ["A339:A", "A171:B", "A768:A"]; where for each residue the format is as follows: "<chain><residue id>:<chosen alternate location>". If empty, no action will be executed.
            * **modeller_key** (*str*) - (None) Modeller license key.
            * **binary_path** (*str*) - ("check_structure") Path to the check_structure executable binary.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
            * **sandbox_path** (*str*) - ("./") [WF property] Parent path to the sandbox directory.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_model.model.fix_altlocs import fix_altlocs
            prop = { 'altlocs': ['A339:A', 'A171:B', 'A768:A'] }
            fix_altlocs(input_pdb_path='/path/to/myStructure.pdb',
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
        self.altlocs = fu.str_to_list(self.altlocs)

    def run(self) -> None:
        """Execute the :class:`FixAltLocs <model.fix_altlocs.FixAltLocs>` object."""
        self.run_check_structure("--non_interactive", "altloc", "--select", ",".join(self.altlocs) or "occupancy")


fix_altlocs = launcher(FixAltLocs)

if __name__ == "__main__":
    FixAltLocs.main()
