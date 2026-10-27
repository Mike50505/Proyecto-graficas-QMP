$ErrorActionPreference = 'Stop'
$destino = Join-Path $PSScriptRoot 'static/vendor'
New-Item -ItemType Directory -Force -Path $destino | Out-Null
Invoke-WebRequest 'https://cdn.jsdelivr.net/npm/chart.js@4.4.8/dist/chart.umd.js' -OutFile (Join-Path $destino 'chart.umd.js')
Invoke-WebRequest 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css' -OutFile (Join-Path $destino 'bootstrap.min.css')
Write-Host 'Bibliotecas descargadas. La aplicación ya no requiere conexión.'
