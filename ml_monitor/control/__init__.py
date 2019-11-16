import ml_monitor

def start():
    try:
        ml_monitor.prometheus.start()
    except KeyboardInterrupt:
        pass

def colab(config_file=None):
    ml_monitor.colab.sync(config_file=config_file)
    ml_monitor.control.start()

def stop():
    gdrive_fetcher_thread = ml_monitor.colab.gdrive_fetcher.fetch_thread
    if gdrive_fetcher_thread is not None:
        gdrive_fetcher_thread.stop()
