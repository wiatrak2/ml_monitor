import threading

from ml_monitor import config

class ValueMonitor:
    def __init__(self):
        self.monitor_values = {}
        self.log_file = config.config.get_logging_file()
        self.thread_running = False

    def log(self):
        try:
            with open(self.log_file, "w") as f:
                f.write(f"{config.config.config_title}:\n")
                for var in self.monitor_values:
                    f.write(f"{var}: {self.monitor_values[var]}\n")
        except:
            self.thread.cancel()
            self.thread_running = False

    def monitor(self, name, value):
        self.monitor_values[name] = value

    def clean(self):
        self.monitor_values = {}

    def _run_thread(self):
        self.thread_running = False
        self.start()
        self.log()

    def start(self):
        if not self.thread_running:
            self.thread = threading.Timer(config.config.log_interval_sec, self._run_thread)
            self.thread.start()
            self.thread_running = True

    def stop(self):
        self.thread.cancel()
        self.thread_running = False

monitor_thread = None
