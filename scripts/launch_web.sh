#!/bin/bash
cd ../crusaders-webshop
pm2 start "npm run dev" --name "vite-server"