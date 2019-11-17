import os
import prometheus_client

from ml_monitor import logging
from ml_monitor import prometheus

PROMETHEUS_PORT = os.getenv("PROMETHEUS_PORT", 8000)
GATEWAY_URL = os.getenv("GATEWAY_URL", "localhost:9091")

pushgateway = False
registry = None

def start():
    prometheus.metrics_collector.invoked = True
    logging.debug("Creating Prometheus http server...")
    prometheus_client.start_http_server(PROMETHEUS_PORT)
    logging.info(f"Prometheus metrics exposed as: http://localhost:{PROMETHEUS_PORT}")
    prometheus.create_pushgateway()

def create_pushgateway():
    logging.info("Configuring Prometheus Pushgateway")
    logging.info(f"Prometheus Pushgateway should be available as {GATEWAY_URL}")
    prometheus.registry = prometheus_client.CollectorRegistry()
    prometheus.pushgateway = True
    prometheus.metrics_collector.run()
