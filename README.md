# ML Monitor
`ml_monitor` package introduces an effortless monitoring of a machine learning training process. It also provides some useful stats about the resources utilization out of the box. And most important - it is designed for an easy integration with not only Jupyter, but also [Google Colab](https://colab.research.google.com) notebooks.
![colab_example](https://github.com/wiatrak2/ml_monitoring/blob/master/docs/gifs/loss.gif?raw=true)
### Requirements:
* python >= 3.6
* [docker](https://www.docker.com)
## Instalation
1. Clone and enter the repository
```bash
git clone https://github.com/wiatrak2/ml_monitor.git
cd ml_monitor
```
2. Run `python configure_gdrive.py` to configure [Google Drive API](developers.google.com/drive/api/), which is required for Colab integration. You need to create a project and enter its credentials - `client_id` and `client_secret`. There are two ways to do it:
	* Go to [Google Drive API python tutorial](https://developers.google.com/drive/api/v3/quickstart/python) and click **Enable the Drive API**. This will create a new project named *Quickstart* that is already properly configured. You will see a window with `Client ID` and `Client Secret`, that `configure_gdrive.py` is asking you for.
	* If you want to create a new project for `ml_monitor` you need to go to the [Google API Console](https://console.developers.google.com/) and:
		* Open *Select a project*  menu (next to the *Google APIs* logo) and click *New project*
		* Set the project name, create it and enter
		* Search for the `Google Drive API` and click **Enable**
		* From the left sidebar select *Credentials*
		* If you see a **Configure Consent Screen** button click it and fill the form (entering the *Application name* is enough). Then click **Create credentials** and select **OAuth Client ID**, select *Other* from the next view and process
		* You will see a window with `Client ID` and `Client secret`. Paste them to the `configure_gdrive.py`

3. Install package using `pip`
```bash
pip install .
```
## Simple setup
There are two components responsible for a successful monitoring of your training. First of them is a thread that collects metrics inside your notebook or python program. The second is a process that makes use of these metrics, parses them and enables things like a pretty visualization. These seemingly complex tasks are implemented to make usage as easy as possible - let's have a look:
* `docker` directory contains an easy setup of tools used for metrics visualization and analysis. These are [Prometheus](https://prometheus.io) and [Grafana](https://grafana.com). You should firstly start these programs, with `docker-compose up` command. Now you should be able to reach the Grafana admin panel on http://localhost:3000. Default credentials are `username: admin` and `password: ml_monitor`. Also a Prometheus UI should be reachable on http://localhost:9090. You can learn some basics about the Prometheus and it's features [here](https://prometheus.io/docs/prometheus/latest/getting_started/).
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

![Init](https://github.com/wiatrak2/ml_monitoring/blob/master/docs/gifs/init.gif?raw=true)
## Google Colab support
Google Colab notebooks let's you run your code using some top GPUs and even TPU for free. It is a great and essential tool for many ML developers. When the `ml_monitor` project was started, it main purpose was to provide a mechanism to follow any desired metrics real time. Therefore `ml_monitor` allows you to begin the integration with Google Colab as easy as in local Jupyter notebook approach.

Parsing and visualization of all the  metrics is again done on your local machine. As code executed by Colab notebooks is separated from your device it is a bit more complicated to have a synchronized data collected by `ml_monitor` inside the Google Colab notebook. Fortunately, you can easily mount your Google Drive and use it within the notebook. Moreover, `ml_monitor` implements a simple file system to enable communication with your Google Drive. Therefore, during the training, metrics collected with `ml_monitor` are stored on your Google Drive, and `ml_monitor.control` mechanism that runs on your local machine can fetch them. All the details are configurable, but the default configuration is enough to use all the `ml_monitor` features.

To start monitoring your Google Colab notebook you should:
* Start the `ml_monitor.control`, that will fetch the metrics from your Google Drive and process them for tools like Grafana and Docker. It is done once again with a single command:
 ```python
import ml_monitor
ml_monitor.control.start()
```
* During the first usage you will be asked for a verification code, so the `ml_monitor` could communicate with your Google Drive. Your browser will (and should) complain about security reasons, but you can still obtain the code and grant the `ml_monitor`  access to your files. It is necessary, as this is the only way to collect the metrics produced by your Colab notebook.

![gdrive_auth](https://github.com/wiatrak2/ml_monitoring/blob/master/docs/gifs/gdrive_auth.gif?raw=true)
* Open your Colab notebook and start monitoring with:
 ```python
import ml_monitor
ml_monitor.colab.init()
```
* That's it. As easy as previously. Moreover you can find a pre-defined Grafana dashboard *Colab stats* that presents statistics like GPU utilization, RAM usage or how long it took to fetch the metrics from your Google Drive to your local machine.
![colab_init](https://github.com/wiatrak2/ml_monitoring/blob/master/docs/gifs/colab_init.gif?raw=true)
## Defining metrics
Collecting metrics, like value of a loss function, should not require changes in already working code. Also you should be made to add as few lines of code as possible. Therefore, if you want to monitor a metric called `some_stat` and set its value as `0.123`, all you have to do is call the `ml_monitor.monitor` function:
```python
ml_monitor.monitor("some_stat", 0.123)
```
This metric should be afterwards visible i.e. on Prometheus UI (http://localhost:9090/graph) and charted with Grafana. `some_stat` will have assigned value `0.123` as long as it will be changed manually, like:
```python
ml_monitor.monitor("some_stat", 123.0)
```
You can call the `ml_monitor.monitor` function the same way from both local code and Google Colab.

![colab_value](https://github.com/wiatrak2/ml_monitoring/blob/master/docs/gifs/colab_value.gif?raw=true)
Metrics defined within python code are collected with usage of [Prometheus Pushgateway](https://github.com/prometheus/pushgateway). You may noticed that they are described with `exported_job` label, which is by default `ml_monitor` or `colab_ml_monitor`. The `exported_job` label could be used to easily filter values (e.g. losses) from specific training process. Therefore `ml_monitor` allows you to set the `exported_job` with `ml_monitor.set_training(training_name: str)` function:
```python
...
ml_monitor.set_training("colab_ResNet_50")
...
for i in range(epochs):
	...
	ml_monitor.monitor("loss", loss.item())
	ml_monitor.monitor("epoch", i)
...
```
You should be then able to filter values from this training using PromQL and curly braces`{}` :
```
loss{exported_job="colab_ResNet_50"}
```
___
The `ml_monitor` package is during development, and this is a very alpha version :smile: I hope somebody will find it helpful during long, lonely model training sessions :computer: