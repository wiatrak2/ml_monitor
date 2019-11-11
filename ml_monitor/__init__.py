import os

from ml_monitor import log
from ml_monitor import gdrive
from ml_monitor import colab
from ml_monitor import config
from ml_monitor import prometheus

def init(config_file=None):
    if config_file is None:
        config_file = os.path.join(os.path.dirname(__file__), "config.yml")
    config.config = config.Config(config_file)
    log.monitor_thread = log.ValueMonitor()
    log.monitor_thread.start()

def monitor(name, value):
    log.monitor_thread.monitor(name, value)

def start():
    log.monitor_thread.start()

def stop():
    log.monitor_thread.stop()
