from ml_monitor import gdrive
from ml_monitor import config

class LogFetcher:
    def __init__(self, log_file):
        self.log_file = log_file
        self.files_location = config.config.files_location
        self.fetch = self._resolve_fetch_method()

    def _resolve_fetch_method(self):
        if self.files_location == "local":
            return self._local_fetch
        if self.files_location == "gdrive":
            return self._gdrive_fetch

    def _local_fetch(self):
        return

    def _gdrive_fetch(self):
        local_log_file = config.config.log_file
        gdrive.gdrive.download(self.log_file, local_log_file)
