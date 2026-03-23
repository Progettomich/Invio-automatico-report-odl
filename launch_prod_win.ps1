# Production Launch Script for Windows
# This script sets up the virtual environment and starts the production server using Waitress

Write-Host "=== Setting up Python virtual environment ===" -ForegroundColor Cyan
python -m venv .venv

Write-Host "=== Activating virtual environment ===" -ForegroundColor Cyan
.\venv\Scripts\activate

Write-Host "=== Installing packages ===" -ForegroundColor Cyan
pip install -r requirements.txt

Write-Host "=== Starting production server with Waitress ===" -ForegroundColor Cyan
waitress-serve --port=5000 wsgi:app
