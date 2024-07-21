#!/bin/sh

# Check if the .env file exists
if [ -f ngrok.env ]; then
  set -o allexport
  # shellcheck disable=SC2039
  source ngrok.env
  set +o allexport
else
  echo ".env file not found."
fi

curl \
-X GET \
-H "Authorization: Bearer ${API_KEY}" \
-H "Ngrok-Version: 2" \
https://api.ngrok.com/endpoints | jq -r '.endpoints[0].public_url' | sed -E 's/^(tcp|http(s)?)\:\/\///' >> ngrok-url
