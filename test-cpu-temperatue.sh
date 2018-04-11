#!/usr/bin/env bash
# control + z 可提前结本脚本
sudo apt-get update
echo tusimple2017 | sudo -S apt-get install -y python-pip cpufrequtils stress lm-sensors > /dev/null
stress -c 56 -t 60 & python cpu_frequency.py
sleep 3
stress -c 56 -t 60 & python cpu_frequency.py
sleep 3
stress -c 56 -t 60 & python cpu_frequency.py
sleep 3
stress -c 56 -t 60 & python cpu_frequency.py
sleep 3
stress -c 56 -t 60 & python cpu_frequency.py

