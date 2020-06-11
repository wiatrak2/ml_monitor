import GPUtil
import psutil

from ml_monitor import logging, BaseHook


class ColabUtilizationHook(BaseHook):
    def hook(self):
        logging.debug("Registering resources utilization")
        GPUs = GPUtil.getGPUs()
        gpu = GPUs[0]
        utilization_metrics = {
            "colab_GPU_mem_free": gpu.memoryFree,
            "colab_GPU_mem_used": gpu.memoryUsed,
            "colab_GPU_mem_util_percentage": gpu.memoryUtil * 100,
            "colab_GPU_mem_total": gpu.memoryTotal,
            "colab_RAM_used_percentage": psutil.virtual_memory().percent,
            "colab_RAM_total_MB": psutil.virtual_memory().total / (1024 * 1024),
        }
        self.monitor("pull_metrics", utilization_metrics)
