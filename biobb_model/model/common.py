"""Common functions for package biobb_model.model"""

import logging
from typing import Optional, Union

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


# TODO: Move this function to biobb_common.tools.file_utils
def _from_string_to_list(input_data: Optional[Union[str, list[str]]]) -> list[str]:
    """
    Converts a string to a list, splitting by commas or spaces. If the input is already a list, returns it as is.
    Returns an empty list if input_data is None.

    Parameters:
        input_data (str, list, or None): The string, list, or None value to convert.

    Returns:
        list: A list of string elements or an empty list if input_data is None.
    """
    if input_data is None:
        return []

    if isinstance(input_data, list):
        # If input is already a list, return it
        return input_data

    # If input is a string, determine the delimiter based on presence of commas
    delimiter = "," if "," in input_data else " "
    items = input_data.split(delimiter)

    # Remove whitespace from each item and ignore empty strings
    processed_items = [item.strip() for item in items if item.strip()]

    return processed_items
