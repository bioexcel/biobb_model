# type: ignore
from biobb_common.tools import test_fixtures as fx

from biobb_model.model.checking_log import checking_log


class TestCheckingLog:
    def setup_class(self):
        fx.test_setup(self, "checking_log")

    def teardown_class(self):
        fx.test_teardown(self)
        # pass

    def test_launch(self):
        checking_log(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths["output_log_path"])
        # assert fx.equal(
        #     self.paths["output_log_path"],
        #     self.paths["reference_output_log_path"],
        #     ignore_list=["loaded", "=    "],
        # )
