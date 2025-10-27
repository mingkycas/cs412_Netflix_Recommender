<#
Simple PowerShell helper to create a virtual environment and install requirements.
Run from the repository root in PowerShell:
    .\setup.ps1
#>

param(
    [string]$VenvName = '.venv'
)

Write-Host "Creating virtual environment '$VenvName' (if it doesn't already exist)..."
if (-not (Test-Path "$PSScriptRoot\$VenvName")) {
    python -m venv $VenvName
} else {
    Write-Host "Virtual environment already exists at $PSScriptRoot\$VenvName"
}

# Use the venv python executable directly to avoid calling Activate.ps1 (avoids ExecutionPolicy issues)
$venvPython = Join-Path $PSScriptRoot "$VenvName\Scripts\python.exe"
if (-not (Test-Path $venvPython)) {
    Write-Error "Could not find venv python executable at $venvPython"
    exit 1
}

Write-Host "Using venv python: $venvPython"
Write-Host "Upgrading pip and installing requirements using the venv python..."
& $venvPython -m pip install --upgrade pip
if (Test-Path "$PSScriptRoot\requirements.txt") {
    & $venvPython -m pip install -r "$PSScriptRoot\requirements.txt"
} else {
    Write-Host "No requirements.txt found; installing pandas by default"
    & $venvPython -m pip install pandas
}

Write-Host "Setup complete. You can run the project with the venv python executable, for example:"
Write-Host "  & \"$venvPython\" src\rule1.py"
Write-Host "If you prefer to activate the venv in PowerShell interactively, run (after adjusting ExecutionPolicy):"
Write-Host "  .\$VenvName\Scripts\Activate.ps1"