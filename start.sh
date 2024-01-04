#!/bin/bash

gunicorn -b 0.0.0.0:8080 --log-level critical web:app &
python3 main.py