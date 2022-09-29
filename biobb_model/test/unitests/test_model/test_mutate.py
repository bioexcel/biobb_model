from biobb_common.tools import test_fixtures as fx
from biobb_model.model.mutate import mutate


class TestFixSideChain:
    def setup_class(self):
        fx.test_setup(self, 'mutate')

    def teardown_class(self):
        fx.test_teardown(self)

    def test_launch(self):
        mutate(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_pdb_path'])
        assert fx.equal(self.paths['output_pdb_path'], self.paths['reference_output_pdb_path'])
