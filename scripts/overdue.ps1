# SpecSelf per-tier overdue check (ADR-008 D11) — PowerShell twin of overdue.sh.
#
# Reads review filenames out of a reviews directory and prints one line per
# tier (weekly/monthly/quarterly/annual) whose newest recorded period is more
# than one period behind the current one. The period currently in progress is
# never overdue: a review one period behind "now" just hasn't been written
# yet. Prints nothing and exits 0 when every tier is current. This script
# only prints; it never writes a review.
#
# Usage: overdue.ps1 [-ReviewsDir <path>]
#   default ReviewsDir: $env:CLAUDE_PROJECT_DIR (or .) + \your-life\reviews

param(
    [Parameter(Position = 0)]
    [string]$ReviewsDir
)

if (-not $ReviewsDir) {
    $projectDir = if ($env:CLAUDE_PROJECT_DIR) { $env:CLAUDE_PROJECT_DIR } else { "." }
    $ReviewsDir = Join-Path $projectDir "your-life\reviews"
}

# Monday-of-ISO-week date for ISO year $Year, week $Week (derived from
# Jan 4, which always falls in week 1). Windows PowerShell 5.1 has no
# System.Globalization.ISOWeek class, so ISO week math is done by hand.
function Get-WeekMonday([int]$Year, [int]$Week) {
    $jan4 = (Get-Date -Year $Year -Month 1 -Day 4).Date
    $jan4Dow = [int]$jan4.DayOfWeek
    if ($jan4Dow -eq 0) { $jan4Dow = 7 }  # ISO: Monday=1 .. Sunday=7
    $week1Monday = $jan4.AddDays(-($jan4Dow - 1))
    return $week1Monday.AddDays(($Week - 1) * 7)
}

# ISO (year, week) for an arbitrary date, via the Thursday-of-this-week rule.
function Get-ISOYearWeek([datetime]$Date) {
    $Date = $Date.Date  # strip time-of-day so day-count subtraction is exact
    $isoDow = ([int]$Date.DayOfWeek + 6) % 7 + 1  # ISO: Monday=1 .. Sunday=7
    $thursday = $Date.AddDays(4 - $isoDow)
    $isoYear = $thursday.Year
    $jan1 = (Get-Date -Year $isoYear -Month 1 -Day 1).Date
    $isoWeek = [int][math]::Floor(($thursday - $jan1).Days / 7) + 1
    return [PSCustomObject]@{ Year = $isoYear; Week = $isoWeek }
}

$weeklyLatest = $null; $monthlyLatest = $null; $quarterlyLatest = $null; $annualLatest = $null
$foundAny = $false

if (Test-Path -LiteralPath $ReviewsDir -PathType Container) {
    foreach ($f in Get-ChildItem -LiteralPath $ReviewsDir -File) {
        $base = $f.Name
        if ($base -match '^(?<y>[0-9]{4})-W(?<w>[0-9]{2})') {
            $tok = "$($Matches.y)-W$($Matches.w)"
            $foundAny = $true
            if (-not $weeklyLatest -or $tok -gt $weeklyLatest) { $weeklyLatest = $tok }
        } elseif ($base -match '^(?<y>[0-9]{4})-Q(?<q>[1-4])') {
            $tok = "$($Matches.y)-Q$($Matches.q)"
            $foundAny = $true
            if (-not $quarterlyLatest -or $tok -gt $quarterlyLatest) { $quarterlyLatest = $tok }
        } elseif ($base -match '^(?<y>[0-9]{4})-(?<m>0[1-9]|1[0-2])(?!\d)') {
            $tok = "$($Matches.y)-$($Matches.m)"
            $foundAny = $true
            if (-not $monthlyLatest -or $tok -gt $monthlyLatest) { $monthlyLatest = $tok }
        } elseif ($base -match '^(?<y>[0-9]{4})') {
            $tok = $Matches.y
            $foundAny = $true
            if (-not $annualLatest -or $tok -gt $annualLatest) { $annualLatest = $tok }
        }
    }
}

if (-not $foundAny) {
    Write-Output "SpecSelf: no reviews yet — run GETTING-STARTED.md to seed your life OS."
    exit 0
}

$now = Get-Date
$nowYear = $now.Year
$nowMonth = $now.ToString("yyyy-MM")
$isoNow = Get-ISOYearWeek -Date $now
$nowGYear = $isoNow.Year
$nowW = $isoNow.Week
$nowWeek = "{0}-W{1:D2}" -f $nowGYear, $nowW
$nowQ = [math]::Floor(($now.Month - 1) / 3) + 1
$nowQuarter = "$nowYear-Q$nowQ"

if ($weeklyLatest) {
    $parts = $weeklyLatest -split '-W'
    $ly = [int]$parts[0]; $lw = [int]$parts[1]
    $nowMonday = Get-WeekMonday -Year $nowGYear -Week $nowW
    $latestMonday = Get-WeekMonday -Year $ly -Week $lw
    $diff = [math]::Round(($nowMonday - $latestMonday).TotalDays / 7)
    if ($diff -gt 1) {
        Write-Output "SpecSelf: weekly review overdue (latest $weeklyLatest, now $nowWeek)."
    }
}

if ($monthlyLatest) {
    $parts = $monthlyLatest -split '-'
    $ly = [int]$parts[0]; $lm = [int]$parts[1]
    $nowIdx = $nowYear * 12 + $now.Month
    $latestIdx = $ly * 12 + $lm
    if (($nowIdx - $latestIdx) -gt 1) {
        Write-Output "SpecSelf: monthly review overdue (latest $monthlyLatest, now $nowMonth)."
    }
}

if ($quarterlyLatest) {
    $parts = $quarterlyLatest -split '-Q'
    $ly = [int]$parts[0]; $lq = [int]$parts[1]
    $nowIdx = $nowYear * 4 + $nowQ
    $latestIdx = $ly * 4 + $lq
    if (($nowIdx - $latestIdx) -gt 1) {
        Write-Output "SpecSelf: quarterly review overdue (latest $quarterlyLatest, now $nowQuarter)."
    }
}

if ($annualLatest) {
    if (($nowYear - [int]$annualLatest) -gt 1) {
        Write-Output "SpecSelf: annual review overdue (latest $annualLatest, now $nowYear)."
    }
}

exit 0
