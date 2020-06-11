import yaml

from ml_monitor import Config, metrics_logger, logging


class Monitor:
    def __init__(self, config_file=None, log_level="info", log_dir=None):
        logging.create_logger(log_level, log_dir=log_dir)
        self.config = Config(config_file)
        self.metrics_logger_thread = metrics_logger.MetricsLogger(self.config)

    def monitor(self, name, value):
        self.metrics_logger_thread.monitor(name, value)

    def start(self):
        self.metrics_logger_thread.start()

    def stop(self):
        self.metrics_logger_thread.stop()

    def pretty_config(self):
        return yaml.dump(self.config)

    def set_training(self, training_name):
        if not training_name.startswith("_"):
            training_name = "_" + training_name
        self.config.title = self.config.config_title + training_name

    def register_hook(self, hook):
        hook.register(self)
        self.metrics_logger_thread.register_hook(hook)
