#!/usr/bin/env python3

"""Module containing the FixAltLocs class and the command line interface."""

import argparse
from typing import Optional

from biobb_common.configuration import settings
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.tools.file_utils import launchlogger

from biobb_model.model.common import _from_string_to_list


class FixAltLocs(BiobbObject):
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
        properties = properties or {}

        # Call parent class constructor
        super().__init__(properties)
        self.locals_var_dict = locals().copy()

        # Input/Output files
        self.io_dict = {
            "in": {"input_pdb_path": input_pdb_path},
            "out": {"output_pdb_path": output_pdb_path},
        }

        # Properties specific for BB
        self.binary_path = properties.get("binary_path", "check_structure")
        self.altlocs = _from_string_to_list(properties.get("altlocs", None))
        self.modeller_key = properties.get("modeller_key")

        # Check the properties
        self.check_properties(properties)
        self.check_arguments()

    @launchlogger
    def launch(self) -> int:
        """Execute the :class:`FixAltLocs <model.fix_altlocs.FixAltLocs>` object."""

        # Setup Biobb
        if self.check_restart():
            return 0
        self.stage_files()

        self.cmd = [
            self.binary_path,
            "-i",
            self.stage_io_dict["in"]["input_pdb_path"],
            "-o",
            self.stage_io_dict["out"]["output_pdb_path"],
            "--force_save",
            "--non_interactive",
            "altloc",
            "--select",
        ]

        if self.altlocs:
            self.cmd.append(",".join(self.altlocs))
        else:
            self.cmd.append("occupancy")

        if self.modeller_key:
            self.cmd.insert(1, self.modeller_key)
            self.cmd.insert(1, "--modeller_key")

        # Run Biobb block
        self.run_biobb()

        # Copy files to host
        self.copy_to_host()

        # Remove temporal files
        # self.tmp_files.extend([self.stage_io_dict.get("unique_dir", "")])
        self.remove_tmp_files()

        self.check_arguments(output_files_created=True, raise_exception=False)
        return self.return_code


def fix_altlocs(
    input_pdb_path: str,
    output_pdb_path: str,
    properties: Optional[dict] = None,
    **kwargs,
) -> int:
    """Create :class:`FixAltLocs <model.fix_altlocs.FixAltLocs>` class and
    execute the :meth:`launch() <model.fix_altlocs.FixAltLocs.launch>` method."""
    return FixAltLocs(
        input_pdb_path=input_pdb_path,
        output_pdb_path=output_pdb_path,
        properties=properties,
        **kwargs,
    ).launch()

    fix_altlocs.__doc__ = FixAltLocs.__doc__


def main():
    parser = argparse.ArgumentParser(
        description="Fix alternate locations from residues",
        formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999),
    )
    parser.add_argument(
        "-c",
        "--config",
        required=False,
        help="This file can be a YAML file, JSON file or JSON string",
    )

    # Specific args of each building block
    required_args = parser.add_argument_group("required arguments")
    required_args.add_argument(
        "-i", "--input_pdb_path", required=True, help="Input PDB file name"
    )
    required_args.add_argument(
        "-o", "--output_pdb_path", required=True, help="Output PDB file name"
    )

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config).get_prop_dic()

    # Specific call of each building block
    fix_altlocs(
        input_pdb_path=args.input_pdb_path,
        output_pdb_path=args.output_pdb_path,
        properties=properties,
    )


if __name__ == "__main__":
    main()
