$ErrorActionPreference = "Stop"
Set-Location -Path $PSScriptRoot

$PythonBin = $env:VNC_TYPER_PYTHON
if (-not $PythonBin) {
    $candidates = @(
        @("py", "-3"),
        @("python"),
        @("python3")
    )
    foreach ($candidate in $candidates) {
        $exe = $candidate[0]
        $args = @()
        if ($candidate.Length -gt 1) {
            $args = $candidate[1..($candidate.Length - 1)]
        }
        try {
            & $exe @args -c "import sys; sys.exit(0 if sys.version_info[0] == 3 else 1)" *> $null
            if ($LASTEXITCODE -eq 0) {
                $PythonBin = ($candidate -join " ")
                break
            }
        } catch {
        }
    }
}

if (-not $PythonBin) {
    Write-Error "No Python 3 executable was found. Install Python 3 or set VNC_TYPER_PYTHON."
    exit 1
}

if (-not (Test-Path ".venv")) {
    Invoke-Expression "$PythonBin -m venv .venv"
}

. .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python main.py
