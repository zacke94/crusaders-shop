#!/bin/bash
cd /home/adamerlandsson/crusaders-shop/crusaders-webshop
pm2 start "npm run dev" --name "vite-server"
pm2 save
