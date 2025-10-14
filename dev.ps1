# Setup script for Windows
Write-Host "Setting up GrowTheory development environment..." -ForegroundColor Green

# Check if venv exists
if (-Not (Test-Path ".venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv .venv
}

# Activate venv
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
.\.venv\Scripts\Activate.ps1

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

Write-Host "Setup complete! Virtual environment is activated." -ForegroundColor Green
Write-Host "To activate in future sessions, run: .\.venv\Scripts\Activate.ps1" -ForegroundColor Cyan