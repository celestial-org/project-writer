#!/bin/bash

export PORT=${PORT:-8080}
gunicorn -b 0.0.0.0:$PORT helloworld:app &
python3 task.py &
cd src && python3 main.py