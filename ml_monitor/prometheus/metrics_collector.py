import time
import json
import os

import numpy as np
import prometheus_client

from ml_monitor import prometheus
from ml_monitor import logging


class MetricsCollector:
    PROMETHEUS_PORT = os.getenv("PROMETHEUS_PORT", 8000)
    GATEWAY_URL = os.getenv("GATEWAY_URL", "http://localhost:9091")
    SERVER_CREATED = False

    def __init__(self, config):
        self.config = config
        self.collectors = {}
        self.pushgateway = False
        self.registry = None

        if self.SERVER_CREATED:
            logging.info(
                f"Using already existing metrics server: http://localhost:{self.PROMETHEUS_PORT}"
            )
        else:
            logging.debug("Creating Prometheus http server...")
            try:
                prometheus_client.start_http_server(self.PROMETHEUS_PORT)
                logging.info(
                    f"Prometheus metrics exposed as: http://localhost:{self.PROMETHEUS_PORT}"
                )
            except OSError:
                logging.warning(
                    f"http://localhost:{self.PROMETHEUS_PORT} is already used.\n"
                    "Assuming it is ocupated by Prometheus server."
                )
            self.SERVER_CREATED = True
            self._create_pushgateway()

    def _create_pushgateway(self):
        logging.info("Configuring Prometheus Pushgateway.")
        logging.info(
            f"Prometheus Pushgateway should be available as {self.GATEWAY_URL}"
        )
        self.registry = prometheus_client.CollectorRegistry()
        self.pushgateway = True

    def _distribute_list_metrics(self, metrics):
        job_title = metrics.pop("title", "ml_monitor")
        log_interval = self.config.log_interval_sec
        for metric in metrics:
            metrics_np = np.array(metrics[metric])
            idx = np.round(np.linspace(0, len(metrics_np) - 1, log_interval)).astype(
                int
            )
            metrics[metric] = metrics_np[idx]
            if metric not in self.collectors:
                self.collectors[metric] = prometheus.metrics.get_gauge(
                    metric, registry=self.registry
                )  # Just gauges so far
        for i in range(log_interval):
            start = time.time()
            for metric in metrics:
                try:
                    collector = self.collectors[metric]
                    collector.set(metrics[metric][i])
                except ValueError:
                    logging.warning(f"Could not convert {metric} metric")
            if self.pushgateway:
                prometheus_client.push_to_gateway(
                    self.GATEWAY_URL, job=job_title, registry=self.registry
                )
            time.sleep(max(0, 1 - (time.time() - start)))

    def _pull_metrics(self, metrics):
        for metrics_dict in metrics:
            for metric in metrics_dict:
                if metric not in self.collectors:
                    self.collectors[metric] = prometheus.metrics.get_gauge(
                        metric
                    )  # Just gauges so far
                collector = self.collectors[metric]
                collector.set(metrics_dict[metric])

    def _parse_metrics(self):
        metrics_file = self.config.metrics_log_file
        logging.debug("Parsing metrics...")
        try:
            with open(metrics_file, "r") as f:
                metrics = json.load(f)
        except Exception as e:
            logging.warning(
                f"Could not open log file {metrics_file}. Exception message:\n{e}"
            )
            time.sleep(self.config.log_interval_sec)
            return
        logging.debug(f"Metrics from file {metrics_file} loaded successfully.")
        if "pull_metrics" in metrics:
            self._pull_metrics(metrics.pop("pull_metrics"))
        self._distribute_list_metrics(metrics)

    def run(self):
        while True:
            self._parse_metrics()
