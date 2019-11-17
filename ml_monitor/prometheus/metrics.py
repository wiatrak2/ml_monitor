import prometheus_client

from ml_monitor import prometheus

def get_gauge(metric_name, registry=True):
    if not registry:
        return prometheus_client.Gauge(metric_name, metric_name)
    return prometheus_client.Gauge(metric_name, metric_name, registry=prometheus.registry)

# ml_monitor.colab.gdrive_fetcher.py
fetching_duration = prometheus_client.Histogram("fetching_duration", "Fetching data from Google Drive duration")
