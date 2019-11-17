import GPUtil
import psutil

import ml_monitor

def register_utlitization():
    GPUs = GPUtil.getGPUs()
    gpu = GPUs[0]
    utilization_metrics = {
        "colab_GPU_mem_free": gpu.memoryFree,
        "colab_GPU_mem_used": gpu.memoryUsed,
        "colab_GPU_mem_util_percentage": gpu.memoryUtil*100,
        "colab_GPU_mem_total": gpu.memoryTotal,
        "colab_RAM_used_percentage": psutil.virtual_memory().percent,
        "colab_RAM_total_MB": psutil.virtual_memory().total/(1024*1024),
    }
    ml_monitor.monitor("pull_metrics", utilization_metrics)
