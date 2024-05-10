#!/bin/bash

export PORT=${PORT:-8080}
gunicorn -b 0.0.0.0:$PORT helloworld:app &
cd src && python3 main.py