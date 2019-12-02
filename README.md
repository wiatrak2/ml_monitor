# ML Monitor
`ml_monitor` package introduces an effortless monitoring of a machine learning training process. It also provides some useful stats about the resources utilization out of the box. And most important - it is designed for an easy integration with not only Jupyter, but also [Google Colab](https://colab.research.google.com) notebooks.
## Simple setup
There are two components responsible for a successful monitoring of your training. First of them is a thread that collects metrics inside your notebook or python program. The second is a process that makes use of these metrics, parses them and enables things like a pretty visualization. These seemingly complex tasks are implemented to make usage as easy as possible - let's have a look:

![Init](https://github.com/wiatrak2/ml_monitoring/blob/master/docs/gifs/init.gif)
* `docker` directory contains an easy setup of tools used for metrics visualization and analysis. These are [Prometheus](https://prometheus.io) and [Grafana](https://grafana.com). You should firstly start these programs, with `docker-compose up` command. Now you should be able to reach the Grafana admin panel on http://localhost:3000. Default credentials are `username: admin` and `password: ml_monitor`.
* Alright, lets's start the monitoring! How to launch the `ml_monitor` inside your notebook? All you need is:  
```python
import ml_monitor
ml_monitor.init()
``` 
* Really, it's enough. Now there is a background thread that already collects some metrics like CPU utilization. This thread will also make use of your custom metrics when you set them with `ml_monitor.monitor("foo", 42.0)` - now the collector thread will also store a metric named `foo` with value `42.0`. 
* Metrics are already collected, let's use them. From the directory where your notebook is stored run `python` interpreter and start the mechanism that I called `control`, as it manages all the metrics etc. To start parsing the metrics collected by your local notebook use:
```python
import ml_monitor
ml_monitor.control.start()
``` 
* You are ready. Go to the Grafana web app and have the training under control. To discover how to make use of the metrics learn more about [PromQL](https://prometheus.io/docs/prometheus/latest/querying/basics/).

Following these steps will let you use the package from the very scratch. I believe that there sould be as little required code lines to setup a tool as possible. Therefore, yo udon't have to modify your already working code to extend it with the `montior`.
