import GPUtil
import psutil

from ml_monitor import logging


class BaseHook:
    def __init__(self, metrics_logger=None):
        self.metrics_logger = metrics_logger

    def __call__(self):
        return self.hook()

    def register(self, metrics_logger):
        self.metrics_logger = metrics_logger

    def monitor(self, name: str, value):
        self.metrics_logger.monitor(name, value)

    def hook(self):
        raise NotImplementedError


class UtilizationHook(BaseHook):
    def hook(self):
        logging.debug("Registering resources utilization")
        GPUs = GPUtil.getGPUs()

        utilization_metrics = {
            "RAM_used_percentage": psutil.virtual_memory().percent,
            "CPU_usage": psutil.cpu_percent(),
        }
        if len(GPUs):
            gpu = GPUs[0]
            utilization_metrics.update(
                {
                    "GPU_mem_free": gpu.memoryFree,
                    "GPU_mem_used": gpu.memoryUsed,
                    "GPU_memb_util_percentage": gpu.memoryUtil * 100,
                    "GPU_mem_total": gpu.memoryTotal,
                }
            )
        self.monitor("pull_metrics", utilization_metrics)
