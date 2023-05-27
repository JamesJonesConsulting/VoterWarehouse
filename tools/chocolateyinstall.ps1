$ErrorActionPreference = 'Stop'; # stop on all errors
$packageName     = 'voterwarehouse'
$toolsDir   = "$(Split-Path -parent $MyInvocation.MyCommand.Definition)"
$scriptDir  = "$(Get-ToolsLocation)\VoterWarehouse"
$executable     = 'voterwarehouse.exe'

#$shortcutName       = 'VoterWarehouse Import Tool.lnk'
# Setup
# New storage location moving forward for all my Chocolatey scripts
if (!(Test-Path "$ENV:ChocolateyToolsLocation\VoterWarehouse")) { New-Item -Path "$ENV:ChocolateyToolsLocation" -Name "VoterWarehouse" -ItemType "Directory" | Out-Null }

# Install script
Move-Item "$toolsDir\$executable" "$scriptDir" -Force -ErrorAction SilentlyContinue

# Create "shim"
Install-ChocolateyPowershellCommand -PackageName "$packageName" -PSFileFullPath "$scriptDir\$executable"

# Cleanup
Remove-Item "$toolsDir\voterwarehouse.*" -Exclude VoterWarehouse.ico -Force -ErrorAction SilentlyContinue | Out-Null
Remove-Item "$toolsDir\voterwarehouse.*" -Exclude VoterWarehouse.png -Force -ErrorAction SilentlyContinue | Out-Null
if ($ENV:Path -NotMatch "VoterWarehouse"){ Install-ChocolateyPath "$scriptDir" "Machine" ; refreshenv }

# Create Start Menu icon
#if (!(Test-Path "$ENV:ProgramData\Microsoft\Windows\Start Menu\Programs\VoterWarehouse")) { New-Item -Path "$ENV:ProgramData\Microsoft\Windows\Start Menu\Programs" -Name "VoterWarehouse" -ItemType "Directory" | Out-Null }
#Install-ChocolateyShortcut -shortcutFilePath "$ENV:ProgramData\Microsoft\Windows\Start Menu\Programs\VoterWarehouse\$shortcutName" -targetPath "$env:ChocolateyInstall\bin\voterwarehouse.bat" -IconLocation "$toolsDir\voterwarehouse.ico" -RunAsAdmin

