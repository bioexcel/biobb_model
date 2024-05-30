# type: ignore
from biobb_common.tools import test_fixtures as fx
from biobb_model.model.fix_pdb import fix_pdb


class TestFixPdb:
    def setup_class(self):
        fx.test_setup(self, 'fix_pdb')

    def teardown_class(self):
        # pass
        fx.test_teardown(self)

    def test_launch(self):
        fix_pdb(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_pdb_path'])
        assert fx.compare_hash(self.paths['output_pdb_path'], self.paths['reference_output_pdb_path'])
        # Error in Biopython PDB parser
        # assert fx.equal(self.paths['output_pdb_path'], self.paths['reference_output_pdb_path'])
