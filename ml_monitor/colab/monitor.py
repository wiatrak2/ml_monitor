import os

from ml_monitor import Monitor, colab


class ColabMonitor(Monitor):
    def __init__(
        self,
        config_file=None,
        log_level="info",
        log_dir="/content/drive/My Drive/.ml_monitor",
    ):
        if config_file is None:
            config_file = os.path.join(os.path.dirname(__file__), "config.yml")
        super().__init__(config_file=config_file, log_level=log_level, log_dir=log_dir)
        self.register_hook(colab.ColabUtilizationHook())
