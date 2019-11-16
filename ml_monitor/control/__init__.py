import ml_monitor
from ml_monitor import logging

def start(log_level="info", logging_dir=None):
    logging.create_logger(log_level=log_level, log_dir=logging_dir)
    try:
        logging.debug("Starting Prometheus metrics collector..")
        ml_monitor.prometheus.start()
    except KeyboardInterrupt:
        logging.info("Metrics collector stopped.")
        ml_monitor.control.stop()

def colab(config_file=None, log_level="info", logging_dir=None):
    logging.create_logger(log_level=log_level, log_dir=logging_dir)
    ml_monitor.colab.sync(config_file=config_file)
    ml_monitor.control.start()

def stop():
    logging.info("Stopping metrics fetching threads...")
    gdrive_fetcher_thread = ml_monitor.colab.gdrive_fetcher.fetch_thread
    if gdrive_fetcher_thread is not None:
        gdrive_fetcher_thread.stop()
