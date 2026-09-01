param(
  [string]$RepoUrl = 'https://github.com/wazirlegacy/venu-skillset-plugin-devolopment.git',
  [string]$WorkDir = "$env:TEMP\venu-skillset-plugin-devolopment"
)
$ErrorActionPreference = 'Stop'

Write-Host 'Venu Skill Library GitHub uploader' -ForegroundColor Cyan
Write-Host "Repository: $RepoUrl"

if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
  Write-Host 'GitHub CLI (gh) is not installed.' -ForegroundColor Yellow
  Write-Host 'Install GitHub CLI, authenticate with: gh auth login' -ForegroundColor Yellow
  exit 1
}
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
  throw 'Git is not installed or not on PATH.'
}

gh auth status | Out-Host

$packageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not (Test-Path "$packageRoot\skills")) {
  throw "Package folder not found: $packageRoot\skills"
}

if (Test-Path $WorkDir) { Remove-Item $WorkDir -Recurse -Force }
New-Item -ItemType Directory -Path $WorkDir | Out-Null

git clone $RepoUrl $WorkDir

# Handle an empty repository (no HEAD / no branch yet).
$hasHead = $true
try { git -C $WorkDir rev-parse --verify HEAD *> $null } catch { $hasHead = $false }
if ($hasHead) {
  git -C $WorkDir checkout main
} else {
  git -C $WorkDir switch --orphan main
}

# Copy package contents. The repository is expected to be empty or intentionally prepared.
Copy-Item "$packageRoot\*" $WorkDir -Recurse -Force -Exclude 'PUSH_TO_GITHUB.ps1'

# Avoid accidentally committing local secret files.
Get-ChildItem $WorkDir -Recurse -Force -File |
  Where-Object { $_.Name -in '.env','.env.local','.env.production','.npmrc' -or $_.Name -match '(^|\.)(key|pem|p12)$' } |
  Remove-Item -Force

# Create a concise manifest of the uploaded Skill packages.
$skillDirs = Get-ChildItem "$WorkDir\skills" -Directory -Recurse |
  Where-Object { $_.Name -eq 'SKILL.md' } # intentionally empty; SKILL.md are files
$skillFiles = Get-ChildItem "$WorkDir\skills" -Recurse -File -Filter 'SKILL.md'
"Canonical and extension Skill packages with SKILL.md files: $($skillFiles.Count)" | Set-Content "$WorkDir\UPLOAD-REPORT.md"

Push-Location $WorkDir
try {
  git add -A
  if (git diff --cached --quiet) {
    Write-Host 'No changes to commit.' -ForegroundColor Yellow
    exit 0
  }
  git commit -m 'feat: import Venu Skill Library'
  git push origin main
  Write-Host 'Upload complete.' -ForegroundColor Green
} finally {
  Pop-Location
}
