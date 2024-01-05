#!/bin/env bash

gunicorn -b 0.0.0.0:8080 web:app &
python3 main.py