import threading

from ml_monitor import gdrive
from ml_monitor import config

class GDriveFetcher:
    def __init__(self, fetch_interval_sec=3):
        self.remote_log_file = self._resolve_log_file()
        self.local_log_file = config.config.log_file
        self.fetch_interval_sec = fetch_interval_sec
        self.thread_running = False

    def fetch(self):
        gdrive.gdrive.download(self.remote_log_file, self.local_log_file)

    def _run_thread(self):
        self.thread_running = False
        self.start()
        self.fetch()

    def start(self):
        if not self.thread_running:
            self.thread = threading.Timer(self.fetch_interval_sec, self._run_thread)
            self.thread.start()
            self.thread_running = True

    def stop(self):
        self.thread.cancel()
        self.thread_running = False

    def _resolve_log_file(self):
        if config.config["gdrive_log_file"] is not None:
            return config.config["gdrive_log_file"]

        remote_log_file = config.config["remote_log_file"]
        file_location_parts = list(filter(None, remote_log_file.split("/")))
        gdrive_loc = ""
        for part in file_location_parts[::-1]:
            gdrive_loc = f"/{part}{gdrive_loc}"
            if gdrive.gdrive.get(gdrive_loc) is not None:
                return gdrive_loc

        raise Exception(f"Could not resolve log file location from config: {remote_log_file}")

fetch_thread = None
