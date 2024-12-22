#!/bin/bash
cd /home/adamerlandsson/crusaders-shop/device
source venv/bin/activate
pm2 start ./run_pi.sh --name "flask-server"
pm2 save
