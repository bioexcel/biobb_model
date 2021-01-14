from biobb_common.tools import test_fixtures as fx
from biobb_model.model.checking_log import checking_log


class TestCheckingLog:
    def setUp(self):
        fx.test_setup(self, 'checking_log')

    def tearDown(self):
        fx.test_teardown(self)
        # pass

    def test_launch(self):
        checking_log(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_log_path'])
        assert fx.equal(self.paths['output_log_path'], self.paths['reference_output_log_path'])
