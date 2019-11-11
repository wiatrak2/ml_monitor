import os

from ml_monitor import gdrive
from ml_monitor import log
from ml_monitor import config
from ml_monitor.colab import gdrive_fetcher

def init(config_file=None):
    if config_file is None:
        config_file = os.path.join(os.path.dirname(__file__), "config.yml")
    config.config = config.Config(config_file)
    log.monitor_thread = log.ValueMonitor()
    log.monitor_thread.start()

def sync(config_file=None):
    if config_file is None:
        config_file = os.path.join(os.path.dirname(__file__), "config.yml")
    config.config = config.Config(config_file)

    if gdrive.gdrive is None:
        gdrive_settings = config.config["gdrive_settings_file"]
        gdrive.gdrive  = gdrive.GDrive(gdrive_settings)

    fetch_interval_sec = config.config["fetch_interval_sec"] or 3
    gdrive_fetcher.fetch_thread = gdrive_fetcher.GDriveFetcher(fetch_interval_sec=fetch_interval_sec)
    gdrive_fetcher.fetch_thread.start()
