from biobb_common.tools import test_fixtures as fx
from model.fix_side_chain import FixSideChain


class TestFixSideChain(object):
    def setUp(self):
        fx.test_setup(self, 'fixsidechain')

    def tearDown(self):
        fx.test_teardown(self)

    def test_launch(self):
        FixSideChain(properties=self.properties, **self.paths).launch()
        assert fx.not_empty(self.paths['output_pdb_path'])
