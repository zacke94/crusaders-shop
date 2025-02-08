#!/bin/bash
export NVM_DIR="$HOME/.config/nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
export DISPLAY=:0
export XDG_RUNTIME_DIR=/run/user/1000
/home/adamerlandsson/.config/nvm/versions/node/v20.16.0/bin/pm2 delete all
sleep 5
/home/adamerlandsson/crusaders-shop/scripts/launch_web.sh
/home/adamerlandsson/crusaders-shop/scripts/launch_backend_pi.sh
sleep 5
/usr/bin/chromium-browser --kiosk 2> /dev/null http://127.0.0.1:5173