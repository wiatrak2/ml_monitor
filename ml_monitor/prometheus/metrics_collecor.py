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

def distribute_list_metrics(metrics, job_title=None):
    log_interval = config.config.log_interval_sec
    for m in metrics:
        metrics_np = np.array(metrics[m])
        idx = np.round(np.linspace(0, len(metrics_np) - 1, log_interval)).astype(int)
        metrics[m] = metrics_np[idx]
    for i in range(log_interval):
        start = time.time()
        for m in metrics:
            c = collectors[m]
            c.set(metrics[m][i])
        if prometheus.pushgateway:
            prometheus_client.push_to_gateway('localhost:9091', job=job_title, registry=prometheus.registry)
        time.sleep(1 - (time.time() - start))

def parse_metrics():
    metrics_file = config.config.log_file
    logging.debug("Parsing metrics...")
    try:
        with open(metrics_file, "r") as f:
            metrics = json.load(f)
    except Exception as e:
        logging.warning(f"Could not open log file {metrics_file}. Exception message:\n{e}")
        return
    for m in metrics:
        if m not in collectors:
            collectors[m] = prometheus.metrics.get_gauge(m) # Just gauges so far
        if isinstance(metrics[m], (int, float)):
            c = collectors[m]
            c.set(metrics[m])
    job_title = metrics.get("title") or "ml_monitor"
    if prometheus.pushgateway:
        prometheus_client.push_to_gateway('localhost:9091', job=job_title, registry=prometheus.registry)
    distribute_list_metrics({m: metrics[m] for m in metrics if type(metrics[m]) is list}, job_title)

def run():
    while True:
        parse_metrics()
