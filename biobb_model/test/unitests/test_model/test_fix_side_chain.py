from biobb_common.tools import test_fixtures as fx
from biobb_model.model.fix_side_chain import FixSideChain

class TestFixSideChain:
    def setUp(self):
        fx.test_setup(self, 'fix_side_chain')

    def tearDown(self):
        fx.test_teardown(self)

    def test_launch(self):
        FixSideChain(properties=self.properties, **self.paths).launch()
        assert fx.not_empty(self.paths['output_pdb_path'])
        assert fx.equal(self.paths['output_pdb_path'], self.paths['reference_output_pdb_path'])
