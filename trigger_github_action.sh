#!/bin/bash
# Script to trigger GitHub Action manually using gh CLI

echo "🚀 Triggering USPSA Match Auto-Registration GitHub Action..."

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI (gh) is not installed"
    echo "   Install it with: sudo apt install gh"
    echo "   Or visit: https://cli.github.com/"
    exit 1
fi

# Check if authenticated
if ! gh auth status &> /dev/null; then
    echo "🔑 Please authenticate with GitHub CLI first:"
    echo "   Run: gh auth login"
    exit 1
fi

# Get repository info
REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)
echo "📂 Repository: $REPO"

# Trigger the workflow
echo "▶️  Triggering workflow..."
gh workflow run "USPSA Match Auto-Registration" --repo $REPO

if [ $? -eq 0 ]; then
    echo "✅ GitHub Action triggered successfully!"
    echo "🔍 Check status at: https://github.com/$REPO/actions"
    echo ""
    echo "📋 To view logs in real-time:"
    echo "   gh run list --repo $REPO"
    echo "   gh run view --repo $REPO [RUN_ID]"
else
    echo "❌ Failed to trigger GitHub Action"
fi