<#
.SYNOPSIS
    bundle-context.ps1 - concatenate your operating context (the contract + your
    vision + your committed principles) into one file you can paste into a chat or
    add to a Claude Project as knowledge.

.DESCRIPTION
    PowerShell twin of bundle-context.sh, for native Windows PowerShell. Needs
    neither Git Bash nor WSL.

.PARAMETER OutputPath
    Path to write the bundle to. Defaults to context-bundle.md.

.EXAMPLE
    .\bundle-context.ps1

.EXAMPLE
    .\bundle-context.ps1 out.md

.NOTES
    The output contains YOUR corpus. It is gitignored by default. Never commit it.
#>

param(
    [string]$OutputPath = "context-bundle.md"
)

$ErrorActionPreference = "Stop"
Set-Location -Path $PSScriptRoot

function Get-NormalizedContent([string]$Path) {
    # File.ReadAllText auto-detects a BOM and defaults to UTF-8 without one.
    # Get-Content -Raw would instead fall back to the system codepage and
    # mangle non-ASCII characters (em dashes, arrows) in the corpus.
    $raw = [System.IO.File]::ReadAllText((Resolve-Path $Path).Path)
    $raw = $raw -replace "`r`n", "`n" -replace "`r", "`n"
    return $raw.TrimEnd("`n")
}

$lines = New-Object System.Collections.Generic.List[string]

function Add-Line([string]$text = "") {
    $lines.Add($text)
}

Add-Line "# My SpecSelf operating context"
Add-Line ""
Add-Line "> This is the contract my agent follows, plus my committed vision and"
Add-Line "> principles. Read it and hold to it for this conversation. You may question"
Add-Line "> anything here, but you never rewrite it: I author the record, you challenge it."
Add-Line ""
Add-Line "---"
Add-Line ""
Add-Line "## The contract (AGENTS.md)"
Add-Line ""
Add-Line (Get-NormalizedContent "AGENTS.md")

if (Test-Path "your-life/vision.md") {
    Add-Line ""
    Add-Line "---"
    Add-Line ""
    Add-Line "## Vision"
    Add-Line ""
    Add-Line (Get-NormalizedContent "your-life/vision.md")
}

if (Test-Path "your-life/aspirational.md") {
    Add-Line ""
    Add-Line "---"
    Add-Line ""
    Add-Line "## Aspirational (who I am becoming)"
    Add-Line ""
    Add-Line (Get-NormalizedContent "your-life/aspirational.md")
}

Add-Line ""
Add-Line "---"
Add-Line ""
Add-Line "## Principles"
Add-Line ""

# Every committed principle file, across all domains; skip scaffolding.
$principlesFound = $false
$principlesDir = "your-life/principles"

if (Test-Path $principlesDir) {
    $baseFull = (Resolve-Path $principlesDir).Path
    $relPaths = @(Get-ChildItem -Path $principlesDir -Recurse -File -Filter "*.md" |
        Where-Object { $_.Name -ne "README.md" } |
        ForEach-Object { $_.FullName.Substring($baseFull.Length + 1) -replace '\\', '/' })

    if ($relPaths.Count -gt 0) {
        [Array]::Sort($relPaths, [System.StringComparer]::Ordinal)
    }

    foreach ($rel in $relPaths) {
        $principlesFound = $true
        Add-Line "### $rel"
        Add-Line ""
        Add-Line (Get-NormalizedContent (Join-Path $principlesDir $rel))
        Add-Line ""
    }
}

if (-not $principlesFound) {
    Add-Line "_No committed principles yet. Run the foundation session"
    Add-Line "(see GETTING-STARTED.md), then re-run this script._"
}

$content = ($lines -join "`n") + "`n"
$fullOut = Join-Path (Get-Location) $OutputPath
[System.IO.File]::WriteAllText($fullOut, $content, (New-Object System.Text.UTF8Encoding($false)))

$lineCount = ($content -split "`n").Count - 1
Write-Host "Wrote $OutputPath ($lineCount lines)."
Write-Host "Paste it into a chat, or add it to a Claude Project as knowledge."
Write-Host "It contains your corpus and is gitignored. Do not commit it."
