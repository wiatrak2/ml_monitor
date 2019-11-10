import os

from ml_monitor import config
from ml_monitor import log
from ml_monitor import gdrive

def init(config_file=None, config_name=None):
    if config_file is None:
        config_file = os.path.join(os.path.dirname(__file__), "config.yml")
    if config_name is None:
        config_name = list(filter(None, os.getcwd().split("/")))[-1]
    config.CONFIG = config.Config(config_file, config_name=config_name)
    log.LOG_THREAD = log.ValueMonitor()

def monitor(name, value):
    log.LOG_THREAD.monitor(name, value)

def start():
    log.LOG_THREAD.start()

def stop():
    log.LOG_THREAD.stop()

