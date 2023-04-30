<#
.SYNOPSIS
    Create venv folder in python project.
.DESCRIPTION
    Script assumes that it is located in a subfolder of a python project. When run it will create a venv folder in the root of the project.
.EXAMPLE
    .\createVenv.ps1
    Runs the script
.INPUTS
    -
.OUTPUTS
    -
.NOTES
    author: Martin Pucovski (martinautomates.com)
#>

# get project directory
$basePath = Split-Path -Path $PSScriptRoot -Parent

# backup current venv
$venvPath = Join-Path -Path $basePath -ChildPath "venv"
if (Test-Path -Path $venvPath) {
    $currentTime = Get-Date -Format "yyyyMMdd_HHmmss"
    $backupVenv = Join-Path -Path $basePath -ChildPath "venv_$currentTime"
    Rename-Item -Path $venvPath -NewName $backupVenv
}

# run python venv module
$processInfo = New-Object System.Diagnostics.ProcessStartInfo
$processInfo.FileName = "python"
$processInfo.Arguments = "-m venv venv"
$processInfo.RedirectStandardError = $true
$processInfo.RedirectStandardOutput = $true
$processInfo.UseShellExecute = $false
$processInfo.WorkingDirectory = $basePath

$process = New-Object System.Diagnostics.Process
$process.StartInfo = $processInfo
$process.Start() | Out-Null

$stdout = $process.StandardOutput.ReadToEnd()
$stderr = $process.StandardError.ReadToEnd()
$process.WaitForExit()

Write-Host "Standard output: $stdout"
Write-Host "Standard error: $stderr"
Write-Host "exit code: " + $process.ExitCode

Read-Host "Script finished. Press ENTER key to exit..."