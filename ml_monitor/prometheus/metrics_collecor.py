from prometheus_client import start_http_server, Summary
from ml_monitor import gdrive
import random
import time

FETCHING_TIME = Summary("fetching_gdrive_seconds", "time spent on fetching file from Google Drive")

@FETCHING_TIME.time()
def fetch_metrics(gdrive, src, dst):
    gdrive.download(src, dst)

if __name__ == '__main__':
    start_http_server(8000)
    gdrive = gdrive.GDrive("/Users/Wojtek/Desktop/Coding/ML/monitoring/ml_monitor/gdrive/settings.yaml")
    while True:
        fetch_metrics(gdrive, "DistSup/yamls/_default_triple_probes.yaml", "/Users/Wojtek/Desktop/Coding/ML/monitoring/ml_monitor/prometheus/test.yaml")
