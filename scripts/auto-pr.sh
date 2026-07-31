#!/bin/bash
# Auto PR script - creates branch, commits, pushes, creates PR
# DEF-023: Added safety controls - no auto-stage, confirmation required
# Usage: ./scripts/auto-pr.sh "commit message"

set -e

COMMIT_MSG="${1:-Update $(date +%Y-%m-%d_%H-%M-%S)}"
BRANCH_NAME="feature/$(echo "$COMMIT_MSG" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | cut -c1-50)-$(date +%s)"

echo "Commit message: $COMMIT_MSG"
echo "Branch name: $BRANCH_NAME"

# DEF-022: Check for staged changes only (don't stage all)
if git diff --cached --quiet; then
    echo "No staged changes found. Stage files explicitly with 'git add' first."
    echo "Example: git add src/ scripts/"
    exit 1
fi

# DEF-023: Show what will be committed
echo ""
echo "Files to be committed:"
git diff --cached --name-only
echo ""

# DEF-023: Require explicit confirmation
read -p "Proceed with commit? (y/N): " CONFIRM
if [[ ! "$CONFIRM" =~ ^[Yy]$ ]]; then
    echo "Aborted."
    exit 1
fi

# Create and switch to new branch
git checkout -b "$BRANCH_NAME"

# Commit (only staged files)
git commit -m "$COMMIT_MSG"

# DEF-023: Push with confirmation
read -p "Push branch $BRANCH_NAME to origin? (y/N): " PUSH_CONFIRM
if [[ ! "$PUSH_CONFIRM" =~ ^[Yy]$ ]]; then
    echo "Branch created locally but not pushed."
    echo "To push later: git push -u origin $BRANCH_NAME"
    git checkout develop
    exit 0
fi

git push -u origin "$BRANCH_NAME"

# Create PR
echo "Creating Pull Request..."
PR_URL=$(gh pr create \
    --base develop \
    --head "$BRANCH_NAME" \
    --title "$COMMIT_MSG" \
    --body "Auto-created PR from local changes" \
    --json url -q .url 2>/dev/null || echo "")

if [ -n "$PR_URL" ]; then
    echo "PR created: $PR_URL"
else
    echo "Could not create PR automatically. Create manually:"
    echo "  gh pr create --base develop --head $BRANCH_NAME --title \"$COMMIT_MSG\""
fi

# DEF-023: Don't auto-merge - require manual review
echo ""
echo "Branch pushed. Create PR on GitHub for review."
echo "Do NOT auto-merge - requires team review."

# Switch back to develop
git checkout develop
git pull origin develop 2>/dev/null || true

echo "Done! Back on develop branch"
