from ml_monitor import config
from ml_monitor import gdrive
from ml_monitor.prometheus import log_fetcher

def start():
    log_file = _resolve_log_file()
    fetcher = log_fetcher.LogFetcher(log_file)
    return fetcher

def _resolve_log_file():
    files_location = config.config.files_location
    if files_location == "local":
        return config.config.log_file

    if config.config["gdrive_log_file"] is not None:
        return config.config["gdrive_log_file"]

    remote_log_file = config.config["remote_log_file"]
    file_location_parts = list(filter(None, remote_log_file.split("/")))
    gdrive_loc = ""
    for part in file_location_parts[::-1]:
        gdrive_loc = f"/{part}{gdrive_loc}"
        if gdrive.gdrive.get(gdrive_loc) is not None:
            return gdrive_loc

    raise Exception(f"Could not resolve log file location from config: {remote_log_file}")

