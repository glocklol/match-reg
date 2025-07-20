# GitHub Actions PWP Registration Setup

## 🚀 Quick Start

### 1. Push to GitHub
```bash
cd /home/glocklol/claude/match-reg
git add .
git commit -m "Add PWP registration workflow"
git push
```

### 2. Set GitHub Secrets
Go to your GitHub repository → Settings → Secrets and variables → Actions

Add these repository secrets:
- `PRACTISCORE_USERNAME`: Your PractiScore email
- `PRACTISCORE_PASSWORD`: Your PractiScore password

### 3. Trigger the Workflow
1. Go to your GitHub repository
2. Click "Actions" tab
3. Click "Register for Practice with Purpose NOW" workflow
4. Click "Run workflow" button
5. Set match date: `07-24-25` (for Thursday)
6. Set power factor: `minor`
7. Click green "Run workflow" button

## 📋 What the Workflow Does

1. **Setup**: Installs Python, Playwright, and dependencies
2. **Login**: Logs into PractiScore with your credentials
3. **Find Match**: Looks for Practice with Purpose match on specified date
4. **Register**: Clicks register button and fills out form with Minor power factor
5. **Verify**: Confirms registration was successful
6. **Report**: Shows final status

## 🔍 Monitoring

- Watch the workflow run in real-time in GitHub Actions
- Check the logs for detailed progress
- Workflow will succeed if registration works
- Workflow will fail if registration fails or already registered

## ⚡ Manual Trigger Commands

If you have GitHub CLI installed:
```bash
gh workflow run "Register for Practice with Purpose NOW" \
  --field match_date=07-24-25 \
  --field power_factor=minor
```

## 🛠️ Troubleshooting

- **Secrets not set**: Add PRACTISCORE_USERNAME and PRACTISCORE_PASSWORD secrets
- **Workflow not found**: Make sure you pushed the .github/workflows folder
- **Still blocked**: GitHub Actions might also be blocked by Cloudflare
- **Registration closed**: Match registration may not be open yet

## 📅 For Future Matches

Change the match_date input to the target date (format: MM-DD-YY)
Examples:
- `07-24-25` for July 24, 2025
- `08-01-25` for August 1, 2025

## 🎯 Success Indicators

✅ Login successful  
✅ Match found  
✅ Registration form filled  
✅ Registration submitted  
✅ Match appears on dashboard  

The workflow should complete in under 5 minutes if successful.