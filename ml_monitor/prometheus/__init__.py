from prometheus_client import start_http_server

import ml_monitor

from ml_monitor.prometheus import metrics, metrics_collecor

def start():
    metrics_collecor.invoked = True
    start_http_server(8000)
    metrics_collecor.run()
