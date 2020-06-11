import json
import threading
from typing import List

from collections import defaultdict

import ml_monitor
from ml_monitor import logging


class MetricsLogger:
    def __init__(self, config: ml_monitor.Config):
        logging.debug("Creating logging thread...")
        self.config = config
        self.monitor_values = defaultdict(list)
        self.metrics_log_file = self.config.logging_file
        self.thread = None
        self.thread_running = False
        self.pre_log_hooks: List[ml_monitor.BaseHook] = []

    def log(self):
        logging.debug("Serializing metrics...")
        for hook in self.pre_log_hooks:
            logging.debug("Applying hook")
            hook()
        self.monitor_values["title"] = self.config.title or "ml_monitor"
        try:
            with open(self.metrics_log_file, "w") as f:
                json.dump(self.monitor_values, f)
            self.clean()
        except Exception as e:
            logging.error(f"Error while serializing metrics: {e}")
            logging.error("Stopping serialization thread")
            self.thread.cancel()
            self.thread_running = False

    def monitor(self, name: str, value):
        logging.debug(f"Receive metric: {name} with value: {value}")
        self.monitor_values[name].append(value)

    def register_hook(self, hook: ml_monitor.BaseHook):
        self.pre_log_hooks.append(hook)

    def clean(self):
        logging.debug("Removing monitored metrics")
        self.monitor_values = defaultdict(list)

    def remove_hooks(self):
        self.pre_log_hooks = []

    def _run_thread(self):
        self.thread_running = False
        self.start()
        self.log()

    def start(self):
        logging.info("Starting metrics logging thread...")
        if not self.thread_running:
            self.thread = threading.Timer(
                self.config.log_interval_sec, self._run_thread
            )
            self.thread.start()
            self.thread_running = True

    def stop(self):
        logging.info("Canceling metrics logging thread...")
        self.thread.cancel()
        self.thread_running = False
