import ml_monitor
from ml_monitor import logging


class Controller:
    def __init__(self, config_file=None, log_level="info", logging_dir=None):
        logging.create_logger(log_level=log_level, log_dir=logging_dir)
        self.config = ml_monitor.Config(config_file)
        self.metrics_collector = None

    def start(self):
        try:
            if self.metrics_collector is None:
                logging.debug("Starting Prometheus metrics collector..")
                self.metrics_collector = ml_monitor.prometheus.MetricsCollector(
                    self.config
                )
                self.metrics_collector.run()
        except Exception as e:
            logging.error(f"Exception raised, stopping metrics collecting.\n{e}")
            self.stop()
            raise e

    def stop(self):
        logging.info("Stopping metrics fetching threads...")


controller = None


def start(*args, **kwargs):
    ml_monitor.control.controller = Controller(*args, **kwargs)
    ml_monitor.control.controller.start()


def stop():
    if ml_monitor.control.controller is not None:
        ml_monitor.control.controller.stop()
