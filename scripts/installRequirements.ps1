<#
.SYNOPSIS
    Install all packages from requirements.txt file.
.DESCRIPTION
    Script assumes that it is located in a subfolder of a python project. When run it will install all packages from requirements.txt into the virtual environment.
.EXAMPLE
    .\installRequirements.ps1
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

# check if venv exists
$venvPath = Join-Path -Path $basePath -ChildPath "venv"
if (!(Test-Path -Path $venvPath)) {
    Write-Host "No venv folder found. Install venv before running this script."
    Read-Host "Script finished. Press ENTER to exit."
    exit
}

# read requirements.txt file
$requirementsFile = Join-Path $basePath -ChildPath "requirements.txt"
$allRequirements = Get-Content -Path $requirementsFile

# build path to venv activation script
$activatePath = Join-Path $venvPath -ChildPath "Scripts"
$activatePath = Join-Path $activatePath -ChildPath "Activate.ps1"

# activate virtual environment
. $activatePath

# install each item
foreach ($oneItem in $allRequirements) {
    pip install $oneItem
}

Read-Host "Script ended. Press ENTER to exit..."
