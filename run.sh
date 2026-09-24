#!/bin/bash

# Installation
python3 -m venv .venv
source .venv/bin/activate
echo "pgzero" > requirements.txt
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# Start game
pgzrun main.py &
pid=$!

# Finish game
wait "$pid"
rm -rf requirements.txt
deactivate
