$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$venvPath = Join-Path $repoRoot ".venv"
$requirementsPath = Join-Path $repoRoot "requirements.txt"
$pythonVersionScript = "import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)"

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
        python -c $pythonVersionScript
        if ($LASTEXITCODE -eq 0) {
            python -m venv $venvPath
        } else {
            throw "Python 3.10+ is required. The 'python' command points to an older version."
        }
    } elseif (Get-Command py -ErrorAction SilentlyContinue) {
        py -3 -c $pythonVersionScript
        if ($LASTEXITCODE -eq 0) {
            py -3 -m venv $venvPath
        } else {
            throw "Python 3.10+ is required. The 'py -3' command points to an older version."
        }
    } else {
        throw "Python 3 is required. Install Python 3.10+ and run this script again."
    }
}

$pythonExe = Join-Path $venvPath "Scripts/python.exe"

if (-not (Test-Path $pythonExe)) {
    throw "Virtual environment was not created correctly: $pythonExe was not found."
}

Invoke-NativeCommand $pythonExe -c $pythonVersionScript
Invoke-NativeCommand $pythonExe -m pip install --upgrade pip setuptools wheel
Invoke-NativeCommand $pythonExe -m pip install -r $requirementsPath

Write-Host "Virtual environment ready at $venvPath"
Write-Host "Activate with: .\.venv\Scripts\Activate.ps1"
Write-Host "Run backend and AI API with: npm run dev:backend"
Write-Host "Run frontend with: npm run dev:frontend"
