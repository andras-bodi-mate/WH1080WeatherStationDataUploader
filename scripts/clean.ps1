try
{
    cd ../
    uv run python src/main.py clean
    pause
}
catch
{
    Write-Host "Uv was not found, installing..."
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    Write-Host "Installation complete. Please restart this script to continue."
    pause
    exit 1
}