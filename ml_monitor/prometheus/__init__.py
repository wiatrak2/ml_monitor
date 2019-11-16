from prometheus_client import start_http_server

import ml_monitor
from ml_monitor import logging
from ml_monitor.prometheus import metrics, metrics_collecor

PROMETHEUS_PORT = 8000

def start():
    metrics_collecor.invoked = True
    start_http_server(PROMETHEUS_PORT)
    logging.info(f"Prometheus metrics exposed as: http://localhost:{PROMETHEUS_PORT}")
    metrics_collecor.run()
