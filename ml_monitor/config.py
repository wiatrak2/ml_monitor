import yaml
import json
import os

class Config:
    def __init__(self, config_file, config_name="ml_monitor"):
        self.config_file = config_file
        self.config = self._load_config_file()
        self.config_name = config_name

        self._parse_config()
        self._create_log_file()

        self.monitor_vars = {}

    def _parse_config(self):
        self.log_file = self.config["log_file"]
        self.log_interval_sec = self.config["log_interval_sec"]

    def _load_config_file(self):
        with open(self.config_file, "r") as config_file:
            try:
                config = yaml.safe_load(config_file)
            except yaml.YAMLError:
                try:
                    config = json.load(config_file)
                except Exception as e:
                    raise Exception(f"Could not load configuration file {self.config_file}\n{e}")
        return config

    def _create_log_file(self):
        if not os.path.exists(self.log_file):
            try:
                os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
                with open(self.log_file, "w") as f:
                    pass
            except Exception as e:
                raise Exception(f"Could not create log file {self.log_file}.\n {e}")

config = None
