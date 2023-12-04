#!/bin/env bash

python3 main.py &
gunicorn --log-level critical --bind 0.0.0.0:8080 keepalive:app