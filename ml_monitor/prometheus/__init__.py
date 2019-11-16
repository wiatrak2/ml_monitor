from prometheus_client import start_http_server

import ml_monitor

from ml_monitor.prometheus import metrics, metrics_collecor

def colab():
    metrics_collecor.invoked = True
    start_http_server(8000)
    ml_monitor.colab.sync()
    ml_monitor.print_config()

    while True:
        metrics_collecor.parse_metrics()
