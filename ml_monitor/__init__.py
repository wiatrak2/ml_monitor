import os
import yaml

from ml_monitor import metrics_logger
from ml_monitor import gdrive
from ml_monitor import colab
from ml_monitor import logging
from ml_monitor import config
from ml_monitor import control
from ml_monitor import prometheus
from ml_monitor import utils

def init(config_file=None, log_level='info'):
    logging.create_logger(log_level)
    if config_file is None:
        config_file = os.path.join(os.path.dirname(__file__), "config.yml")
    config.config = utils.safe_init(config.config, config.Config(config_file))
    metrics_logger.metrics_logger_thread = utils.safe_init(metrics_logger.metrics_logger_thread, metrics_logger.MetricsLogger())
    metrics_logger.metrics_logger_thread.start()

def monitor(name, value):
    metrics_logger.metrics_logger_thread.monitor(name, value)

def start():
    metrics_logger.metrics_logger_thread.start()

def stop():
    metrics_logger.metrics_logger_thread.stop()

def print_config():
    print(yaml.dump(config.config.config))

def set_training(training_name):
    if not training_name.startswith("_"):
        training_name = "_" + training_name
    config.config.title = config.config.config_title + training_name
