from biobb_common.tools import test_fixtures as fx
from biobb_model.model.fix_ssbonds import fix_ssbonds


class TestFixSSBonds:
    def setUp(self):
        fx.test_setup(self, 'fix_ssbonds')

    def tearDown(self):
        fx.test_teardown(self)

    def test_launch(self):
        fix_ssbonds(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_pdb_path'])
        assert fx.equal(self.paths['output_pdb_path'], self.paths['reference_output_pdb_path'])
