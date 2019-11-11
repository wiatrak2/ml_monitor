import os

from ml_monitor import log
from ml_monitor import gdrive
from ml_monitor import colab
from ml_monitor.config import config, Config

def init(config_file=None, config_name=None):
    if config_file is None:
        config_file = os.path.join(os.path.dirname(__file__), "config.yml")
    if config_name is None:
        config_name = list(filter(None, os.getcwd().split("/")))[-1]
    config = Config(config_file, config_name=config_name)
    log.monitor_thread = log.ValueMonitor()
    log.monitor_thread.start()

def monitor(name, value):
    log.monitor_thread.monitor(name, value)

def start():
    log.monitor_thread.start()

def stop():
    log.monitor_thread.stop()

