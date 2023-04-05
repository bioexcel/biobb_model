""" Common functions for package biobb_model.model """
from biobb_common.tools import file_utils as fu
import logging


def modeller_installed(out_log: logging.Logger = None, global_log: logging.Logger = None) -> bool:
    try:
        import modeller
        from modeller import automodel
        fu.log(f"Modeller is installed in your environment. Modeller version: {modeller.__version__}", out_log, global_log)
        fu.log(f"Modeller automodel class: {automodel.automodel}", out_log=out_log)
    except ImportError:
        fu.log("Modeller is not installed in your environment.\nPlease install it by typing:\n\nconda install -c salilab modeller\n", out_log, global_log)
        return False

    return True
