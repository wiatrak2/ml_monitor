import os

from ml_monitor import gdrive
from ml_monitor import log
from ml_monitor import config
from ml_monitor import utils
from ml_monitor import logging
from ml_monitor.colab import gdrive_fetcher

def init(config_file=None, log_level='info'):
    if config_file is None:
        config_file = os.path.join(os.path.dirname(__file__), "config.yml")
    logging.create_logger(log_level)
    config.config = utils.safe_init(config.config, config.Config(config_file))
    log.monitor_thread = utils.safe_init(log.monitor_thread, log.ValueMonitor())
    log.monitor_thread.start()

def sync(config_file=None):
    logging.debug("Starting Google Colab synchronization...")
    if config_file is None:
        config_file = os.path.join(os.path.dirname(__file__), "config.yml")
    config.config = utils.safe_init(config.config, config.Config(config_file))

    if gdrive.gdrive is None:
        gdrive_settings = config.config.gdrive_settings_file
        gdrive.gdrive  = gdrive.GDrive(gdrive_settings)

    fetch_interval_sec = config.config.fetch_interval_sec or 3
    logging.debug(f"Fetching interval set as {fetch_interval_sec} seconds.")
    gdrive_fetcher.fetch_thread = gdrive_fetcher.GDriveFetcher(fetch_interval_sec=fetch_interval_sec)
    gdrive_fetcher.fetch_thread.start()

def sync_stop():
    logging.info("Stopping Google Colab sychronization...")
    gdrive_fetcher.fetch_thread.stop()

def set_model(model_name):
    config.config.title = config.config.config_title + model_name

def stop_training():
    for metric in log.monitor_thread.monitor_values:
        log.monitor_thread.monitor_values[metric] = -1
