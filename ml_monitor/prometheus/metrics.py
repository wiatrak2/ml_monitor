import prometheus_client


def get_gauge(metric_name, registry=None):
    if registry is None:
        return prometheus_client.Gauge(metric_name, metric_name)
    return prometheus_client.Gauge(metric_name, metric_name, registry=registry)


# ml_monitor.colab.gdrive_fetcher.py
fetching_duration = prometheus_client.Histogram(
    "fetching_duration", "Fetching data from Google Drive duration"
)
