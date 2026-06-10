# setup_env.ps1
Write-Host "Setting up AgriSentry Environment..." -ForegroundColor Green

if (-not (Test-Path -Path "venv")) {
    Write-Host "Creating Virtual Environment..."
    python -m venv venv
}

Write-Host "Activating Virtual Environment..."
# Cannot activate for user in a sub-script easily in powershell, but we can install
.\venv\Scripts\python.exe -m pip install --upgrade pip
.\venv\Scripts\pip.exe install -r requirements.txt
.\venv\Scripts\pip.exe install -r backend/requirements.txt

Write-Host "Environment setup complete! Activate with: .\venv\Scripts\activate" -ForegroundColor Green
