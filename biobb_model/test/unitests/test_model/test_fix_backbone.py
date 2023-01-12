from biobb_common.tools import test_fixtures as fx
from biobb_model.model.fix_backbone import fix_backbone

class TestFixBackbone:
    def setup_class(self):
        fx.test_setup(self, 'fix_backbone')

    def teardown_class(self):
        # pass
        fx.test_teardown(self)

    def test_launch(self):
        fix_backbone(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_pdb_path'])
        assert fx.equal(self.paths['output_pdb_path'], self.paths['reference_output_pdb_path'])
