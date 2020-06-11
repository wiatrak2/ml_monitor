import threading

from ml_monitor import prometheus, logging


class GDriveFetcher:
    def __init__(self, gdrive, config, fetch_interval_sec=3):
        self.gdrive = gdrive
        self.config = config

        self.remote_metrics_log_file = self._resolve_log_file()
        self.local_log_file = self.config.metrics_log_file
        self.fetch_interval_sec = fetch_interval_sec
        self.thread_running = False
        self.thread = None

    def fetch(self):
        try:
            logging.debug("Fetching metrics from Google Drive...")
            with prometheus.fetching_duration.time():
                self.gdrive.download(self.remote_metrics_log_file, self.local_log_file)
        except Exception as e:
            logging.error(
                f"Exception raised while fetching files from Google Drive:\n{e}"
            )
            logging.error("Stopping fetching thread due to the exception.")
            self.stop()

    def _run_thread(self):
        self.thread_running = False
        self.start()
        self.fetch()

    def start(self):
        logging.debug("Starting Google Drive featching thread.")
        if not self.thread_running:
            self.thread = threading.Timer(self.fetch_interval_sec, self._run_thread)
            self.thread.start()
            self.thread_running = True

    def stop(self):
        logging.info("Stopping Google Drive featching thread.")
        self.thread.cancel()
        self.thread_running = False

    def _resolve_log_file(self):
        logging.debug("Resolving log file location...")
        if self.config.gdrive_log_file is not None:
            return self.config.gdrive_log_file

        remote_metrics_log_file = self.config.remote_metrics_log_file
        file_location_parts = list(filter(None, remote_metrics_log_file.split("/")))
        gdrive_loc = ""
        for part in file_location_parts[::-1]:
            gdrive_loc = f"/{part}{gdrive_loc}"
            if self.gdrive.get(gdrive_loc) is not None:
                logging.info(
                    f"Google Drive log file location resolved as {gdrive_loc}."
                )
                return gdrive_loc

        raise Exception(
            f"Could not resolve log file location from config: {remote_metrics_log_file}"
        )
