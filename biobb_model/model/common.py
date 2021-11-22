""" Common functions for package biobb_model.model """
from biobb_common.tools import file_utils as fu
from typing import List, Dict, Tuple, Mapping, Union, Set, Sequence
import logging


def modeller_installed(out_log: logging.Logger = None, global_log: logging.Logger = None) -> bool:
    try:
        import modeller
        from modeller import automodel
    except ImportError:
        fu.log(f"Modeller is not installed in your environment.\nPlease install it by typing:\n\nconda install -c salilab modeller\n", out_log, global_log)
        return False

    return True

