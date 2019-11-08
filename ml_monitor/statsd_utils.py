import statsd

def get_client(statsd_host='localhost', statsd_port=8125, prefix='ml_monitor'):
    return statsd.StatsClient(statsd_host, statsd_port, prefix=prefix)

def send_metric(statsd_clinet, metric_name, value):
    statsd_clinet.gauge(metric_name, value)