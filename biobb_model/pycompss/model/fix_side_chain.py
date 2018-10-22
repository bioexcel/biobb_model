import traceback
from pycompss.api.task import task
from biobb_common.tools import file_utils as fu
from biobb_model.model import fix_side_chain

@task(input_pdb_path=FILE_IN, output_pdb_path=FILE_OUT)
def fix_side_chain_pc(input_pdb_path, output_pdb_path, properties, **kwargs):
    try:
        fix_side_chain.FixSideChain(input_pdb_path=input_pdb_path, output_pdb_path=output_pdb_path, properties=properties, **kwargs).launch()
    except Exception:
        traceback.print_exc()
        fu.write_failed_output(output_pdb_path)
