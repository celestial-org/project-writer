#!/bin/bash

export PORT=${PORT:-8080} http_proxy=http://127.0.0.1:6868 https_proxy=http://127.0.0.1:6868

gunicorn -b 0.0.0.0:$PORT helloworld:app &
python main.py