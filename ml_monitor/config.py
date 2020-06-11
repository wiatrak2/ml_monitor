import yaml
import json
import os

from ml_monitor import logging


class Config:
    def __init__(self, config_file=None):
        if config_file is None:
            config_file = os.path.join(os.path.dirname(__file__), "config.yml")
        logging.debug(f"Configuring module using {config_file}...")
        self.config_file = config_file
        self.config = self._load_config_file()
        # Variables to be read from config file
        self.config_title = None
        self.files_location = None
        self.metrics_log_file = None
        self.log_interval_sec = None

        self._parse_config()
        self._create_log_file()

    @property
    def logging_file(self):
        if self.files_location == "local":
            return self.metrics_log_file
        elif self.files_location == "gdrive":
            return self.config.get("remote_metrics_log_file")
        return None

    def __getattr__(self, item):
        return self.config.get(item)

    def __getitem__(self, key):
        return self.key

    def _load_config_file(self):
        logging.debug(f"Loading configuration file {self.config_file}...")
        with open(self.config_file, "r") as config_file:
            try:
                config = yaml.safe_load(config_file)
            except yaml.YAMLError:
                try:
                    config = json.load(config_file)
                except Exception as e:
                    raise Exception(
                        f"Could not load configuration file {self.config_file}\n{e}"
                    )
        return config

    def _parse_config(self):
        logging.debug("Parsing configuration file...")
        self.config_title = self.config.get(
            "title", list(filter(None, os.getcwd().split("/")))[-1]
        )
        self.files_location = self.config.get("files_location", "local")
        self.metrics_log_file = self.config.get("metrics_log_file")
        self.log_interval_sec = self.config.get("log_interval_sec")

    def _create_log_file(self):
        logging.debug(f"Creating logging file {self.metrics_log_file}...")
        if not os.path.exists(self.metrics_log_file):
            try:
                logging.info(f"Creating log file {self.metrics_log_file}")
                os.makedirs(os.path.dirname(self.metrics_log_file), exist_ok=True)
                with open(self.metrics_log_file, "w") as f:
                    json.dump({}, f)
            except Exception as e:
                raise Exception(
                    f"Could not create log file {self.metrics_log_file}.\n {e}"
                )
