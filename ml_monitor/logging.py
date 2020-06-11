import logging
import daiquiri

import ml_monitor

logger = None


def create_logger(log_level="info", log_dir=".ml_monitor", mute_gdrive=True):
    if ml_monitor.logging.logger is not None:
        return

    log_level = getattr(logging, log_level.upper())

    if log_dir is None:
        outputs = [daiquiri.output.STDERR]
    else:
        outputs = [daiquiri.output.File(directory=log_dir)]

    if mute_gdrive:
        ml_monitor.logging.mute_gdrive_logger()

    daiquiri.setup(level=log_level, outputs=outputs)
    ml_monitor.logging.logger = daiquiri.getLogger(__name__)


def debug(msg):
    if ml_monitor.logging.logger is not None:
        ml_monitor.logging.logger.debug(msg)


def info(msg):
    if ml_monitor.logging.logger is not None:
        ml_monitor.logging.logger.info(msg)


def warning(msg):
    if ml_monitor.logging.logger is not None:
        ml_monitor.logging.logger.warning(msg)


def error(msg):
    if ml_monitor.logging.logger is not None:
        ml_monitor.logging.logger.error(msg)


def mute_gdrive_logger():
    logging.getLogger("googleapiclient").setLevel(logging.ERROR)
