[CmdletBinding(SupportsShouldProcess)]
param(
    [Parameter(Mandatory=$true)][string]$ProjectRoot
)
$ErrorActionPreference = 'Stop'
$sourceRoot = [System.IO.Path]::GetFullPath($PSScriptRoot)
$targetRoot = [System.IO.Path]::GetFullPath($ProjectRoot)
if (-not (Test-Path -LiteralPath $targetRoot -PathType Container)) {
    throw 'ProjectRoot must be an existing directory.'
}
$scopes = @('skills\infron_repost_sourcing', '10.26\bonus_repost_sourcing')
$copyPlan = @()
foreach ($scope in $scopes) {
    $scopeRoot = Join-Path $sourceRoot $scope
    foreach ($file in Get-ChildItem -LiteralPath $scopeRoot -File -Recurse) {
        if ($file.FullName -match '[\\/]__pycache__[\\/]' -or $file.Extension -eq '.pyc') { continue }
        $relative = [System.IO.Path]::GetRelativePath($sourceRoot, $file.FullName)
        $target = [System.IO.Path]::GetFullPath((Join-Path $targetRoot $relative))
        $targetPrefix = $targetRoot.TrimEnd('\') + '\'
        if (-not $target.StartsWith($targetPrefix, [System.StringComparison]::OrdinalIgnoreCase)) {
            throw 'Resolved destination escapes ProjectRoot.'
        }
        if (Test-Path -LiteralPath $target) {
            if (-not (Test-Path -LiteralPath $target -PathType Leaf)) { throw "Path conflict: $target" }
            $existingHash = (Get-FileHash -LiteralPath $target -Algorithm SHA256).Hash
            $sourceHash = (Get-FileHash -LiteralPath $file.FullName -Algorithm SHA256).Hash
            if ($existingHash -ne $sourceHash) {
                throw "Existing file differs; nothing copied. Preserve/reconcile it manually: $target"
            }
        } else {
            $copyPlan += [PSCustomObject]@{Source=$file.FullName; Target=$target}
        }
    }
}
# All conflicts are checked before any copy; never overwrite existing bytes.
foreach ($item in $copyPlan) {
    if ($PSCmdlet.ShouldProcess($item.Target, 'Copy new task file')) {
        $parent = Split-Path -Parent $item.Target
        [System.IO.Directory]::CreateDirectory($parent) | Out-Null
        [System.IO.File]::Copy($item.Source, $item.Target, $false)
    }
}
Write-Output "New task files planned: $($copyPlan.Count). Existing files preserved. No push, publishing, scheduling or global installation."
