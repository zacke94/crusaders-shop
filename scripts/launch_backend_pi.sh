#!/bin/bash
cd ../device
source myvenv/bin/activate
pm2 start ./run_pi.sh --name "flask-server"