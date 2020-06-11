import os

import ml_monitor

from ml_monitor import logging
from ml_monitor.colab import GDriveFetcher
from ml_monitor.control import Controller


class ColabController(Controller):
    def __init__(self, config_file=None, log_level="info", logging_dir=None):
        if config_file is None:
            config_file = os.path.join(os.path.dirname(__file__), "config.yml")
        super().__init__(config_file, log_level, logging_dir)

        self.gdrive = ml_monitor.gdrive.GDriveClient(self.config.gdrive_settings_file)
        self.gdrive_fetcher_thread = self._sync()

    def _sync(self):
        logging.debug("Starting Google Colab synchronization...")
        fetch_interval_sec = self.config.fetch_interval_sec or 3
        logging.debug(f"Fetching interval set as {fetch_interval_sec} seconds.")
        gdrive_fetcher_thread = GDriveFetcher(
            self.gdrive, self.config, fetch_interval_sec=fetch_interval_sec
        )
        gdrive_fetcher_thread.start()
        return gdrive_fetcher_thread

    def stop(self):
        super().stop()
        self.gdrive_fetcher_thread.stop()


controller = None


def control(*args, **kwargs):
    ml_monitor.colab.controller = ColabController(*args, **kwargs)
    ml_monitor.colab.controller.start()


def stop():
    if ml_monitor.colab.controller is not None:
        ml_monitor.colab.controller.stop()
