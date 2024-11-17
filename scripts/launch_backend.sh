#!/bin/bash
cd ../device
source myvenv/bin/activate
pm2 start "python3 run.py" --name "flask-server"