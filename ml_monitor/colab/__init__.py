import os

from ml_monitor import gdrive
from ml_monitor import metrics_logger
from ml_monitor import config
from ml_monitor import utils
from ml_monitor import logging
from ml_monitor.colab import gdrive_fetcher

def init(config_file=None, log_level='info', log_dir="/content/drive/My Drive/.ml_monitor"):
    if config_file is None:
        config_file = os.path.join(os.path.dirname(__file__), "config.yml")
    logging.create_logger(log_level, log_dir=log_dir)
    config.config = utils.safe_init(config.config, config.Config(config_file))
    metrics_logger.metrics_logger_thread = utils.safe_init(metrics_logger.metrics_logger_thread, metrics_logger.MetricsLogger())
    metrics_logger.metrics_logger_thread.start()

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
