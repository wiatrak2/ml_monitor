import prometheus_client

import ml_monitor
from ml_monitor import logging
from ml_monitor.prometheus import metrics, metrics_collecor

PROMETHEUS_PORT = 8000

pushgateway = False
registry = None

def start():
    metrics_collecor.invoked = True
    prometheus_client.start_http_server(PROMETHEUS_PORT)
    logging.info(f"Prometheus metrics exposed as: http://localhost:{PROMETHEUS_PORT}")
    metrics_collecor.run()

def use_pushgateway():
    logging.info("Using PushGateway")
    logging.info("Registry should be available as http://localhost:9091")
    ml_monitor.prometheus.registry = prometheus_client.CollectorRegistry()
    ml_monitor.prometheus.pushgateway = True
    metrics_collecor.run()
