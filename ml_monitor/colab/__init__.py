import os

from ml_monitor import gdrive
from ml_monitor import log
from ml_monitor import config

def init(config_file=None, config_name=None):
    if config_file is None:
        config_file = os.path.join(os.path.dirname(__file__), "config.yml")
    if config_name is None:
        config_name = "ml_monitor_colab"
    config.CONFIG = config.Config(config_file, config_name=config_name)
    log.LOG_THREAD = log.ValueMonitor()
    log.LOG_THREAD.start()
