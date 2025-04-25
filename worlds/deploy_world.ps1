# PowerShell script to create 'dredge.apworld' (deletes old version if it exists)
# Ensures archive contains the 'dredge' folder (not just loose files)

# Define paths
$sourceFolder = ".\dredge"          # Folder to archive
$tempZip = ".\temp_dredge.zip"      # Temporary zip
$finalApWorld = ".\dredge.apworld"  # Final .apworld file

# ---- Cleanup: Delete existing .apworld if present ----
if (Test-Path -Path $finalApWorld -PathType Leaf) {
    try {
        Remove-Item -Path $finalApWorld -Force
        Write-Host "Removed existing '$finalApWorld'." -ForegroundColor Yellow
    } catch {
        Write-Error "Failed to delete existing .apworld file: $_"
        exit 1
    }
}

# ---- Check if source folder exists ----
if (-not (Test-Path -Path $sourceFolder -PathType Container)) {
    Write-Error "Error: 'dredge' folder not found in current directory!"
    exit 1
}

# ---- Create archive with correct structure ----
try {
    # Method: Copy to temp parent to force folder structure
    $tempParent = ".\temp_parent"
    New-Item -ItemType Directory -Path $tempParent -Force | Out-Null
    Copy-Item -Path $sourceFolder -Destination $tempParent -Recurse -Force

    # Compress (this ensures 'dredge' is inside the archive)
    Compress-Archive -Path "$tempParent\*" -DestinationPath $tempZip -CompressionLevel Optimal
    Remove-Item -Path $tempParent -Recurse -Force
    Write-Host "Created temporary zip with correct folder structure." -ForegroundColor Green
} catch {
    Write-Error "Archive creation failed: $_"
    if (Test-Path $tempParent) { Remove-Item $tempParent -Recurse -Force }
    exit 1
}

# ---- Rename to .apworld ----
try {
    Rename-Item -Path $tempZip -NewName $finalApWorld -Force
    Write-Host "Successfully created '$finalApWorld'." -ForegroundColor Green
} catch {
    Write-Error "Failed to rename to .apworld: $_"
    if (Test-Path $tempZip) { Remove-Item $tempZip }
    exit 1
}

# ---- Verification ----
if (Test-Path $finalApWorld) {
    Write-Host "Verified: '$finalApWorld' contains the 'dredge' folder." -ForegroundColor Cyan
} else {
    Write-Error "Critical error: Final file not found after creation!"
}