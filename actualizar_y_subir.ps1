$proyecto = "C:\Users\Intel\OneDrive\Documentos\observatorio_precio"
Set-Location $proyecto

# 1. Descargar, validar y guardar lo nuevo (y dejar un registro)
& "$proyecto\.venv\Scripts\python.exe" actualizar.py 2>&1 | Tee-Object -FilePath "datos\registro.txt" -Append

# 2. Si Python falló, no subir nada
if ($LASTEXITCODE -ne 0) {
    Write-Host "actualizar.py falló. No se sube nada."
    exit 1
}

# 3. Subir la base solo si cambió
git add datos/precios.db
git diff --cached --quiet
if ($LASTEXITCODE -ne 0) {
    git commit -m "Actualización automática de precios"
    git push
} else {
    Write-Host "Sin cambios en la base."
}