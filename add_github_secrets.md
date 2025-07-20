# Quick GitHub Secrets Setup

Go to: https://github.com/glocklol/match-reg/settings/secrets/actions

## Required Secrets to Add

Based on your .env file, add these secrets:

### Core Credentials (May already exist)
1. **PRACTISCORE_USERNAME**
   - Value: `a@asg.io`

2. **PRACTISCORE_PASSWORD** 
   - Value: `[Glocklol]1532297864`

3. **PHONE_NUMBER**
   - Value: `7732312303`

### Registration Details (Newly needed)
4. **REGISTRATION_FIRST_NAME**
   - Value: `Adam`

5. **REGISTRATION_LAST_NAME**
   - Value: `Golko`

6. **REGISTRATION_EMAIL**
   - Value: `a@asg.io`

7. **REGISTRATION_POWER_FACTOR**
   - Value: `minor`

## How to Add Each Secret

1. Click "New repository secret"
2. Enter the secret name (e.g., `PRACTISCORE_USERNAME`)
3. Enter the secret value
4. Click "Add secret"
5. Repeat for each secret above

## After Adding Secrets

Run this command to test:
```bash
./trigger_github_action.sh
```

The system should then be able to register for Practice with Purpose and will be ready for Monday's Run & Gun registration.