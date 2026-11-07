# Diagnostica el VBS sin ejecutar Python, abrir ventanas ni instalar nada.
$ErrorActionPreference = 'Stop'
$origenInicio = Join-Path (Split-Path -Parent $PSScriptRoot) 'Iniciar Archivo Omnitrix.vbs'
$pruebaInicio = Join-Path ([System.IO.Path]::GetTempPath()) ('Omnitrix prueba ' + [guid]::NewGuid().ToString('N'))
$carpetaScripts = Join-Path $pruebaInicio '.venv\Scripts'
$archivoVbs = Join-Path $pruebaInicio 'Iniciar Archivo Omnitrix.vbs'
$archivosPrueba = @('iniciar.py', 'app.py', 'requirements.txt', '.venv\Scripts\python.exe')
try {
    New-Item -ItemType Directory -Path $carpetaScripts -Force | Out-Null
    Copy-Item -LiteralPath $origenInicio -Destination $archivoVbs
    $salidaSinEntorno = & cscript.exe //nologo $archivoVbs /comprobar
    if ($LASTEXITCODE -eq 0) { throw 'Se debieron rechazar los archivos ausentes.' }
    foreach ($nombrePrueba in $archivosPrueba) {
        [System.IO.File]::WriteAllText((Join-Path $pruebaInicio $nombrePrueba), '')
    }
    $salidaConArchivos = & cscript.exe //nologo $archivoVbs /comprobar
    if ($LASTEXITCODE -ne 0) { throw 'Se debieron aceptar los archivos de prueba.' }
    Write-Output 'Correcto: rechazo de ausencias y comprobacion positiva en carpeta con espacios.'
    Write-Output 'Los archivos simulados no se ejecutaron. No se abrieron ventanas ni navegador.'
    Write-Output $salidaConArchivos
} finally {
    # Solo elimina los archivos creados y sus directorios vacios; no hay borrado recursivo.
    foreach ($nombrePrueba in $archivosPrueba) {
        $archivoPrueba = Join-Path $pruebaInicio $nombrePrueba
        if (Test-Path -LiteralPath $archivoPrueba) { Remove-Item -LiteralPath $archivoPrueba }
    }
    if (Test-Path -LiteralPath $archivoVbs) { Remove-Item -LiteralPath $archivoVbs }
    if (Test-Path -LiteralPath $carpetaScripts) { Remove-Item -LiteralPath $carpetaScripts }
    $carpetaEntorno = Join-Path $pruebaInicio '.venv'
    if (Test-Path -LiteralPath $carpetaEntorno) { Remove-Item -LiteralPath $carpetaEntorno }
    if (Test-Path -LiteralPath $pruebaInicio) { Remove-Item -LiteralPath $pruebaInicio }
}
