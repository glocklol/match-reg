# GitHub Secrets Setup Guide

To ensure the automated registration works on Monday, you need to configure these secrets in your GitHub repository:

## Required Secrets

Navigate to your GitHub repository → Settings → Secrets and variables → Actions → New repository secret

### Core Credentials
- **Name:** `PRACTISCORE_USERNAME`  
  **Value:** `a@asg.io`

- **Name:** `PRACTISCORE_PASSWORD`  
  **Value:** `[Glocklol]1532297864`

### Registration Details
- **Name:** `REGISTRATION_FIRST_NAME`  
  **Value:** `Adam`

- **Name:** `REGISTRATION_LAST_NAME`  
  **Value:** `Golko`

- **Name:** `REGISTRATION_EMAIL`  
  **Value:** `a@asg.io`

- **Name:** `REGISTRATION_POWER_FACTOR`  
  **Value:** `minor`

### Optional (Already Configured)
- **Name:** `PHONE_NUMBER`  
  **Value:** `7732312303`

- **Name:** `GITHUB_TOKEN` (Automatically provided by GitHub Actions)

## Verification

After adding the secrets, you can verify the setup by:

1. Go to Actions tab in your GitHub repository
2. Find "USPSA Match Auto-Registration" workflow  
3. Click "Run workflow" to test manually
4. Check the logs to ensure everything works

## Schedule

The workflow runs automatically every day at **10:00 PM Central Time** (3:00 AM UTC).

## Security Notes

- These secrets are encrypted and only accessible to GitHub Actions
- Never commit sensitive credentials to your repository
- The local `.env` file should not be pushed to GitHub (it's already in `.gitignore`)

## Next Steps

1. Add all the secrets listed above to your GitHub repository
2. Test the workflow manually using "Run workflow" 
3. The system will automatically attempt registration on Monday evening

## Troubleshooting

If registration fails:
- Check the Action logs in the GitHub Actions tab
- Look for the uploaded `match-registrar-logs` artifact
- The system will continue trying daily until successful