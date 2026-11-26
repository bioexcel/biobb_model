#!/usr/bin/env python3

"""Module containing the CheckingLog class and the command line interface."""

from typing import Optional

from biobb_common.generic.biobb_object import launcher

from biobb_model.model.common import CheckStructureBase


class CheckingLog(CheckStructureBase):
    """
    | biobb_model CheckingLog
    | Class to check the errors of a PDB structure.
    | Check the errors of a PDB structure and create a report log file.

    Args:
        input_pdb_path (str): Input PDB file path. File type: input. `Sample file <https://github.com/bioexcel/biobb_model/raw/master/biobb_model/test/data/model/2ki5.pdb>`_. Accepted formats: pdb (edam:format_1476).
        output_log_path (str): Output report log file path. File type: output. `Sample file <https://github.com/bioexcel/biobb_model/raw/master/biobb_model/test/reference/model/checking.log>`_.  Accepted formats: log (edam:format_2330).
        properties (dict - Python dictionary object containing the tool parameters, not input/output files):
            * **modeller_key** (*str*) - (None) Modeller license key.
            * **binary_path** (*str*) - ("check_structure") Path to the check_structure executable binary.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
            * **sandbox_path** (*str*) - ("./") [WF property] Parent path to the sandbox directory.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_model.model.checking_log import checking_log
            prop = { 'restart': False }
            checking_log(input_pdb_path='/path/to/myStructure.pdb',
                         output_log_path='/path/to/myReport.log',
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
        output_log_path: str,
        properties: Optional[dict] = None,
        **kwargs,
    ) -> None:
        super().__init__(**locals())

    def run(self) -> None:
        """Execute the :class:`CheckingLog <model.checking_log.CheckingLog>` object."""
        self.run_check_structure("checkall", ">", self.stage_io_dict["out"]["output_log_path"])


checking_log = launcher(CheckingLog)

if __name__ == "__main__":
    CheckingLog.main()
