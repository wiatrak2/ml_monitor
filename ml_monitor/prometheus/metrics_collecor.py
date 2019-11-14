import random
import time
import json

from prometheus_client import start_http_server

from ml_monitor import colab
from ml_monitor import config
from ml_monitor import prometheus

invoked = False

collectors = {}

def parse_metrics():
    metrics_file = config.config.log_file
    try:
        with open(metrics_file, "r") as f:
            metrics = json.load(f)
    except:
        return
    for m in metrics:
        if m not in collectors:
            collectors[m] = prometheus.metrics.get_gauge(m)
        gauge = collectors[m]
        gauge.set(metrics[m])

if __name__ == '__main__':
    prometheus.metrics_collecor.invoked = True
    start_http_server(8000)
    colab.sync()
