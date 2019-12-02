import random
import time
import json
import numpy as np
import prometheus_client

from ml_monitor import colab
from ml_monitor import config
from ml_monitor import prometheus
from ml_monitor import logging

invoked = False

collectors = {}

def distribute_list_metrics(metrics):
    job_title = "ml_monitor"
    if "title" in metrics:
        job_title = metrics.pop("title")
    log_interval = config.config.log_interval_sec
    for m in metrics:
        metrics_np = np.array(metrics[m])
        idx = np.round(np.linspace(0, len(metrics_np) - 1, log_interval)).astype(int)
        metrics[m] = metrics_np[idx]
        if m not in collectors:
            collectors[m] = prometheus.metrics.get_gauge(m) # Just gauges so far
    for i in range(log_interval):
        start = time.time()
        for m in metrics:
            c = collectors[m]
            c.set(metrics[m][i])
        if prometheus.pushgateway:
            prometheus_client.push_to_gateway(prometheus.GATEWAY_URL, job=job_title, registry=prometheus.registry)
        time.sleep(max(0, 1 - (time.time() - start)))

def pull_metrics(metrics):
    for metrics_dict in metrics:
        for m in metrics_dict:
            if m not in collectors:
                collectors[m] = prometheus.metrics.get_gauge(m, registry=False) # Just gauges so far
            c = collectors[m]
            c.set(metrics_dict[m])

def parse_metrics():
    metrics_file = config.config.metrics_log_file
    logging.debug("Parsing metrics...")
    try:
        with open(metrics_file, "r") as f:
            metrics = json.load(f)
    except Exception as e:
        logging.warning(f"Could not open log file {metrics_file}. Exception message:\n{e}")
        time.sleep(config.config.log_interval_sec)
        return
    logging.debug(f"Metrics from file {metrics_file} loaded successfully.")
    if "pull_metrics" in metrics:
        prometheus.metrics_collector.pull_metrics(metrics.pop("pull_metrics"))
    distribute_list_metrics(metrics)

def run():
    while True:
        parse_metrics()