$ErrorActionPreference = 'Stop'; # stop on all errors
$packageName     = 'voterwarehouse'
$toolsDir   = "$(Split-Path -parent $MyInvocation.MyCommand.Definition)"
$scriptDir  = "$(Get-ToolsLocation)\VoterWarehouse"

$shortcutName       = 'VoterWarehouse Import Tool.lnk'

$ErrorActionPreference = 'SilentlyContinue'

Remove-Item "$ENV:ProgramData\Microsoft\Windows\Start Menu\Programs\chocolatey\$shortcutName" -Force -ErrorAction SilentlyContinue
Remove-Item "$ENV:ProgramData\Microsoft\Windows\Start Menu\Programs\VoterWarehouse\$shortcutName" -Force -ErrorAction SilentlyContinue
Remove-Item "$ENV:ChocolateyInstall\bin\$packageName.bat" -Force -ErrorAction SilentlyContinue
Remove-Item "$scriptDir\$packageName.*" -Force -ErrorAction SilentlyContinue | Out-Null

if (!(Get-ChildItem -Path "$ENV:ChocolateyToolsLocation\VoterWarehouse" | Measure-Object | %{$_.Count})) {
  $ENV:Path.Replace("$ChocolateyToolsLocation\VoterWarehouse","") | Out-Null
  Remove-Item "$ENV:ChocolateyToolsLocation\VoterWarehouse" | Out-Null
}
