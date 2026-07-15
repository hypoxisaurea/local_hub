$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$venvPath = Join-Path $repoRoot ".venv"
$requirementsPath = Join-Path $repoRoot "requirements.txt"

function Invoke-NativeCommand {
    param(
        [Parameter(Mandatory = $true)]
        [string] $FilePath,

        [Parameter(ValueFromRemainingArguments = $true)]
        [string[]] $Arguments
    )

    & $FilePath @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Command failed with exit code $LASTEXITCODE`: $FilePath $($Arguments -join ' ')"
    }
}

if (-not (Test-Path $venvPath)) {
    if (Get-Command python -ErrorAction SilentlyContinue) {
        python -m venv $venvPath
    } elseif (Get-Command py -ErrorAction SilentlyContinue) {
        py -3 -m venv $venvPath
    } else {
        throw "Python 3 is required. Install Python 3.11+ and run this script again."
    }
}

$pythonExe = Join-Path $venvPath "Scripts/python.exe"

if (-not (Test-Path $pythonExe)) {
    throw "Virtual environment was not created correctly: $pythonExe was not found."
}

Invoke-NativeCommand $pythonExe -m pip install --upgrade pip setuptools wheel
Invoke-NativeCommand $pythonExe -m pip install -r $requirementsPath

Write-Host "Virtual environment ready at $venvPath"
Write-Host "Activate with: .\.venv\Scripts\Activate.ps1"
