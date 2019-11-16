import random
import time
import json
import numpy as np

from prometheus_client import start_http_server

from ml_monitor import colab
from ml_monitor import config
from ml_monitor import prometheus
from ml_monitor import logging

invoked = False

collectors = {}

def distribute_list_metrics(metrics):
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
    distribute_list_metrics({m: metrics[m] for m in metrics if type(metrics[m]) is list})

def run():
    while True:
        parse_metrics()
