import GPUtil
import psutil

import ml_monitor
from ml_monitor import logging

def safe_init(variable, instance):
    if variable is None:
        return instance
    return variable

def register_utlitization():
    logging.debug("Registering resources utilization")
    GPUs = GPUtil.getGPUs()

    utilization_metrics = {
        "RAM_used_percentage": psutil.virtual_memory().percent,
        "CPU_usage": psutil.cpu_percent(),
    }
    if len(GPUs):
        gpu = GPUs[0]
        utilization_metrics.update({
        "GPU_mem_free": gpu.memoryFree,
        "GPU_mem_used": gpu.memoryUsed,
        "GPU_memb_util_percentage": gpu.memoryUtil*100,
        "GPU_mem_total": gpu.memoryTotal,
        })

    ml_monitor.monitor("pull_metrics", utilization_metrics)
