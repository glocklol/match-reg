# USPSA Match Auto-Registration Tool

Automatically registers for "NSPS Run & Gun" matches at North Shore Practical Shooters when registration opens.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your PractiScore credentials
   ```

3. **Required secrets for GitHub Actions:**
   - `PRACTISCORE_USERNAME`: Your PractiScore username
   - `PRACTISCORE_PASSWORD`: Your PractiScore password  
   - `GITHUB_TOKEN`: GitHub token (automatically provided)

## How it works

1. **Scheduled Check**: Runs daily at 10 PM Central Time via GitHub Actions
2. **Match Discovery**: Searches North Shore Practical Shooters club page for "NSPS Run & Gun" matches
3. **Registration Status**: Checks if registration is open for found matches
4. **Auto-Registration**: Attempts to register when a match opens
5. **Duplicate Prevention**: Only registers once per match to avoid roster spam

## Manual Testing

```bash
python match_registrar.py
```

## Safety Features

- **Single Registration**: Prevents multiple registrations for the same match
- **Target Specific**: Only looks for "NSPS Run & Gun" matches at NSPS club
- **Logging**: Full activity logging for troubleshooting
- **Error Handling**: Graceful failure handling

## Files

- `match_registrar.py`: Main registration script
- `requirements.txt`: Python dependencies
- `.github/workflows/match-checker.yml`: GitHub Actions automation
- `.env.example`: Environment variables template