# Lightweight python script that will test the HDD speed
## Features
* `standalone.py` and `disk_speed_flask.py` are as basic as they can be
* docker image enables functionality through the WEBUI to test in a different path of the container; be aware that said path must be mounted
i.e. 2 HDD/SSDs mounted to the container:

host: `/mnt/ssd` mounted to `/ssd` correct path is: `/ssd` 
host: `/mnt/hdd` mounted to `/hdd`correct path is: `/hdd`

* docker image also displays graphs for comparison purposes 

## Ways to run it:
* tweak file size within standalone.py and `python standalone.py` from cli
* or use the jupyter test_hdd_speed.ipynb notebook
* or `python disk_speed_flask.py` to run it in flask then access `http://127.0.0.1:5000`
* or use the Dockerfile to build `docker build -t disk-speed .` and run it `docker run -p 5000:5000 disk-speed`
* or simply pull from dockerhub with `docker pull alexvm6/lightweight-python-disk-speed:1.0 `