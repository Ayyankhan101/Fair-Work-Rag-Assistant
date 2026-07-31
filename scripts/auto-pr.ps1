# Auto PR script - PowerShell equivalent for Windows
# DEF-015: Cross-platform support
# Usage: .\scripts\auto-pr.ps1 "commit message"

param(
    [string]$CommitMsg = "Update $(Get-Date -Format 'yyyy-MM-dd_HH-mm-ss')"
)

$ErrorActionPreference = "Stop"

$BranchName = "feature/$(($CommitMsg.ToLower() -replace '[^a-z0-9]','-' -replace '--+','-').Substring(0, [Math]::Min(50, $CommitMsg.Length)))-$([DateTimeOffset]::Now.ToUnixTimeSeconds())"

Write-Host "Commit message: $CommitMsg"
Write-Host "Branch name: $BranchName"

# Check for staged changes only
$staged = git diff --cached --name-only
if (-not $staged) {
    Write-Host "No staged changes found. Stage files explicitly with 'git add' first."
    Write-Host "Example: git add src/ scripts/"
    exit 1
}

# Show what will be committed
Write-Host ""
Write-Host "Files to be committed:"
git diff --cached --name-only
Write-Host ""

# Require confirmation
$confirm = Read-Host "Proceed with commit? (y/N)"
if ($confirm -notmatch '^[Yy]$') {
    Write-Host "Aborted."
    exit 1
}

# Create and switch to new branch
git checkout -b $BranchName

# Commit
git commit -m $CommitMsg

# Push with confirmation
$pushConfirm = Read-Host "Push branch $BranchName to origin? (y/N)"
if ($pushConfirm -notmatch '^[Yy]$') {
    Write-Host "Branch created locally but not pushed."
    Write-Host "To push later: git push -u origin $BranchName"
    git checkout develop
    exit 0
}

git push -u origin $BranchName

# Create PR
Write-Host "Creating Pull Request..."
try {
    $prUrl = gh pr create --base develop --head $BranchName --title $CommitMsg --body "Auto-created PR from local changes" --json url -q .url 2>$null
    if ($prUrl) {
        Write-Host "PR created: $prUrl"
    } else {
        Write-Host "Could not create PR automatically. Create manually:"
        Write-Host "  gh pr create --base develop --head $BranchName --title `"$CommitMsg`""
    }
} catch {
    Write-Host "Could not create PR automatically."
}

# Don't auto-merge - require manual review
Write-Host ""
Write-Host "Branch pushed. Create PR on GitHub for review."

# Switch back to develop
git checkout develop
try { git pull origin develop 2>$null } catch {}

Write-Host "Done! Back on develop branch"
