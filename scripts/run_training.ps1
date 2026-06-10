# run_training.ps1
Write-Host "Starting AgriSentry Training Pipeline..." -ForegroundColor Green

# Ensure we have the base model
if (-not (Test-Path -Path "models\yolov8n.pt")) {
    Write-Host "Downloading base YOLOv8n model to models/ directory..."
    # Ultralytics will auto-download if missing, but we can pre-fetch if needed.
}

$env:PYTHONPATH = "."
python src/train.py

Write-Host "Training Script Completed." -ForegroundColor Green
