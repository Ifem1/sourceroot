$ErrorActionPreference = "Stop"
$Contract = "contracts/sourceroot.py"

if (-not (Get-Command genlayer -ErrorAction SilentlyContinue)) {
    throw "GenLayer CLI is not installed. Run: npm install -g genlayer"
}
if (-not (Test-Path $Contract)) {
    throw "Run this script from the repository root."
}

python scripts/preflight.py
python -m pytest tests/static -q

if (Get-Command genvm-lint -ErrorAction SilentlyContinue) {
    genvm-lint check $Contract
}

Write-Host "Using the currently selected GenLayer account."
Write-Host "No password or private key is read from this repository."
genlayer network set studionet
genlayer account
genlayer deploy --contract $Contract
