$ErrorActionPreference = 'Stop'
$envDestino = Join-Path $PSScriptRoot '.env.docker'
$envEjemplo = Join-Path $PSScriptRoot '.env.docker.example'
if (-not (Test-Path -LiteralPath $envDestino)) {
    Copy-Item -LiteralPath $envEjemplo -Destination $envDestino
}
$contenidoDocker = [IO.File]::ReadAllText($envDestino)
$lineaClave = [regex]::Match($contenidoDocker, '(?m)^SECRET_KEY=([^\r\n]*)')
if (-not $lineaClave.Success -or [string]::IsNullOrWhiteSpace($lineaClave.Groups[1].Value)) {
    $bytesClaveDocker = New-Object byte[] 48
    $generadorClaveDocker = [Security.Cryptography.RandomNumberGenerator]::Create()
    try { $generadorClaveDocker.GetBytes($bytesClaveDocker) }
    finally { $generadorClaveDocker.Dispose() }
    $claveDocker = [Convert]::ToBase64String($bytesClaveDocker)
    if ($lineaClave.Success) {
        $contenidoDocker = [regex]::Replace($contenidoDocker, '(?m)^SECRET_KEY=[^\r\n]*', "SECRET_KEY=$claveDocker")
    } else {
        $contenidoDocker = $contenidoDocker.TrimEnd() + "`nSECRET_KEY=$claveDocker`n"
    }
    [IO.File]::WriteAllText($envDestino, $contenidoDocker, [Text.UTF8Encoding]::new($false))
}
Write-Host 'Configuracion Docker preparada en .env.docker. La clave existente se conserva.'
Write-Host 'Inicio: docker compose --env-file .env.docker up -d --build'
