#!/bin/env bash

python3 main.py &
gunicorn --bind 0.0.0.0:8080 --log-level critical web:app