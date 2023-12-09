#!/bin/env bash

python3 main.py &
gunicorn --bind 0.0.0.0:8080 api.main:app