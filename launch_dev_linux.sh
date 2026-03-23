#!/bin/bash

# Development Launch Script for Linux
# This script sets up the virtual environment and starts the development server

set -e  # Exit on error

echo "=== Setting up Python virtual environment ==="
python3 -m venv .venv

echo "=== Activating virtual environment ==="
source .venv/bin/activate

echo "=== Installing packages ==="
pip install -r requirements.txt

echo "=== Starting development server ==="
python wsgi.py
