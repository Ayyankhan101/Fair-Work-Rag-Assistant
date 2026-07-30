#!/bin/bash
# Auto PR script - creates branch, commits, pushes, creates PR
# Usage: ./scripts/auto-pr.sh "commit message"

set -e

COMMIT_MSG="${1:-Update $(date +%Y-%m-%d_%H-%M-%S)}"
BRANCH_NAME="feature/$(echo "$COMMIT_MSG" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | cut -c1-50)-$(date +%s)"

echo "📝 Commit message: $COMMIT_MSG"
echo "🌿 Branch name: $BRANCH_NAME"

# Check if there are changes
if git diff --quiet && git diff --cached --quiet; then
    echo "❌ No changes to commit"
    exit 1
fi

# Create and switch to new branch
git checkout -b "$BRANCH_NAME"

# Stage and commit
git add .
git commit -m "$COMMIT_MSG"

# Push branch
echo "⬆️  Pushing branch..."
git push -u origin "$BRANCH_NAME"

# Create PR
echo "🔀 Creating Pull Request..."
PR_URL=$(gh pr create \
    --base develop \
    --head "$BRANCH_NAME" \
    --title "$COMMIT_MSG" \
    --body "Auto-created PR from local changes" \
    --json url -q .url)

echo "✅ PR created: $PR_URL"

# Try to merge (auto-merge if no conflicts)
echo "🔄 Attempting to merge..."
if gh pr merge "$PR_URL" --merge --delete-branch 2>/dev/null; then
    echo "✅ Merged successfully!"
else
    echo "⚠️  conflicts detected - please resolve manually"
    echo "   PR: $PR_URL"
fi

# Switch back to develop
git checkout develop
git pull origin develop

echo "✅ Done! Back on develop branch"
