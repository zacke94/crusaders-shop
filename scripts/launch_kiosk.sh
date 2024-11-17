#!/bin/bash
pm2 delete all
./launch_web.sh && ./launch_backend.sh
sleep 10
# continue here