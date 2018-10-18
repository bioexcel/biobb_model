from biobb_common.tools import test_fixtures as fx
from model.mutate import Mutate


class TestFixSideChain(object):
    def setUp(self):
        fx.test_setup(self, 'mutate')

    def tearDown(self):
        fx.test_teardown(self)

    def test_launch(self):
        Mutate(properties=self.properties, **self.paths).launch()
        assert fx.not_empty(self.paths['output_pdb_path'])
