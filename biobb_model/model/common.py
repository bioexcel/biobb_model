"""Common functions for package biobb_model.model"""

import logging
from typing import Optional

from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.tools import file_utils as fu


def modeller_installed(
    out_log: Optional[logging.Logger] = None,
    global_log: Optional[logging.Logger] = None,
) -> bool:
    try:
        import modeller  # type: ignore
        from modeller import automodel

        fu.log(
            f"Modeller is installed in your environment. Modeller version: {modeller.__version__}",
            out_log,
            global_log,
        )
        fu.log(f"Modeller automodel class: {automodel.automodel}", local_log=out_log)
    except ImportError:
        fu.log(
            "Modeller is not installed in your environment.\nPlease install it by typing:\n\nconda install -c salilab modeller\n",
            out_log,
            global_log,
        )
        return False

    return True


class CheckStructureBase(BiobbObject):
    """Base of the blocks that run check_structure (biobb_structure_checking) on their input_pdb_path."""

    def run_check_structure(self, *command: str) -> None:
        """Go from a check_structure command (ie: ``"amide", "--fix", "All"``) to its execution on the staged
        input_pdb_path, with the modeller_key and, if the block has an output_pdb_path, -o and --force_save."""
        self.cmd = [self.binary_path]
        if self.modeller_key:
            self.cmd += ["--modeller_key", self.modeller_key]
        self.cmd += ["-i", self.stage_io_dict["in"]["input_pdb_path"]]
        if "output_pdb_path" in self.stage_io_dict["out"]:
            self.cmd += ["-o", self.stage_io_dict["out"]["output_pdb_path"], "--force_save"]
        self.cmd += command
        self.run_biobb()

    def modeller_rebuild(self) -> list[str]:
        """Go from the use_modeller property to the --rebuild option of check_structure. Outside a container it
        needs Modeller in the environment: without it the option is left out (logged)."""
        if not self.use_modeller:
            return []
        if self.container_path or modeller_installed(self.out_log, self.global_log):
            return ["--rebuild"]
        fu.log(
            "Modeller is not installed --rebuild option can not be used proceeding without using it",
            self.out_log,
            self.global_log,
        )
        return []
